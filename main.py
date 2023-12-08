import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from jinja2 import Template
import httpx
from decouple import config
import logging
import sys
from prometheus_fastapi_instrumentator import Instrumentator, metrics

logger = logging.getLogger(__name__)

app = FastAPI()

# Load configuration from file if provided as a command-line argument
config_file_path = os.environ.get("CONFIG_FILE_PATH", "config.json")
if os.path.exists(config_file_path):
    config.read(config_file_path)

PROJECT_NAME = "prty-fast"
HEALTHCHECK_PATH = "/v1/health"
NTFY_ADDRESS = config("NTFY_ADDRESS", default="https://ntfy.example.me")
TEMPLATES_FOLDER = config("TEMPLATES_FOLDER", default="templates")
DRY_RUN = config("DRY_RUN", default=False, cast=bool)

# Prometheus Instrumentator
instrumentator = Instrumentator()
instrumentator.add(
    metrics.request_size(),
    metrics.response_size(),
    metrics.latency(),
    metrics.requests("app"),
)
instrumentator.expose(app).instrument(app)

def load_templates():
    templates = {}

    # Load templates from the 'defaults' folder based on the INCLUDE_TEMPLATES configuration
    include_templates = config("INCLUDE_TEMPLATES", default="", cast=str).split(";")
    include_templates = [template for template in include_templates if template]

    for template_name in include_templates:
        template_path = os.path.join("defaults", f"{template_name}.j2")

        # Check if the template file exists
        if not os.path.exists(template_path):
            raise ValueError(f"Template file not found for '{template_name}'. Please check your configuration.")

        with open(template_path) as template_file:
            template_content = template_file.read()
            templates[template_name] = Template(template_content)

    # Load templates from the 'templates' folder
    for filename in os.listdir(TEMPLATES_FOLDER):
        if filename.endswith(".j2"):
            template_name = os.path.splitext(filename)[0]
            with open(os.path.join(TEMPLATES_FOLDER, filename)) as template_file:
                template_content = template_file.read()
                templates[template_name] = Template(template_content)

    return templates

TEMPLATES = load_templates()

def get_template(template_name):
    template = TEMPLATES.get(template_name)
    if template is None:
        raise HTTPException(status_code=400, detail=f"Template not found for '{template_name}'. Please check your configuration.")
    return template

async def send_notification(template_name, data):
    template = get_template(template_name)

    transformed_message = template.render(message=data)
    json_message = json.loads(transformed_message)

    body = json_message.get("body")
    headers = {key: value for key, value in json_message.items() if key != "body"}

    # Log the request details
    logger.info(f"Sending request to {NTFY_ADDRESS}/{template_name}")
    logger.info(f"Channel: {template_name}")
    logger.info(f"Body: {body}")
    logger.info(f"Headers: {headers}")

    if DRY_RUN:
        return 200, "Yeah!"

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{NTFY_ADDRESS}/{template_name}", data=body, headers=headers)

    return response.status_code, response.text

def create_endpoint(template_name):
    async def endpoint(data: dict):
        try:
            status_code, response_text = await send_notification(template_name, data)
            if status_code == 200:
                return JSONResponse(content={"status": "success", "response_text": response_text})
            else:
                return JSONResponse(content={"status": "error", "response_text": response_text}, status_code=status_code)
        except Exception as e:
            return JSONResponse(content={"status": "error", "error_message": str(e)}, status_code=500)

    return endpoint

# Create endpoints for each template
for template_name in TEMPLATES:
    app.post(f"/{template_name}")(create_endpoint(template_name))

def check_ntfy_health():
    try:
        response = httpx.get(f"{NTFY_ADDRESS}{HEALTHCHECK_PATH}")
        return response.status_code == 200 and response.json().get("healthy", False)
    except Exception:
        return False

# Root endpoint for HTML page
@app.get("/", response_class=HTMLResponse)
def read_root():
    is_ntfy_healthy = check_ntfy_health()

    # Define emoji based on NTFY health status
    health_emoji = "✅" if is_ntfy_healthy else "❌"

    template = """
    <html>
    <head>
        <title>{{project_name}}</title>
    </head>
    <body>
        <h1>{{project_name}}</h1>
        <h2>Loaded Templates:</h2>
        <ul>
            {% for template_name in templates %}
                <li>{{ template_name }}</li>
            {% endfor %}
        </ul>
        <h2><a href="{{ ntfy_address }}" target="_blank">{{ ntfy_address }} {{ health_emoji }}</a></h2>
    </body>
    </html>
    """
    return HTMLResponse(content=Template(template).render(project_name=PROJECT_NAME, templates=list(TEMPLATES.keys()), ntfy_address=NTFY_ADDRESS, health_emoji=health_emoji))