# prty-fast

**Note: I am not a Python programmer, and this program is primarily AI-generated. The program should never be exposed publicly, and running it is entirely at your own risk. Use caution and discretion when handling sensitive information.**

prty-fast is a FastAPI-based service for sending notifications using configurable templates.

## Introduction

prty-fast allows you to define message templates using Jinja2 syntax and send notifications using those templates. The service is intended for internal use and should not be exposed to the public internet.

## Features

- **Template-based Transformations:** Define message templates using Jinja2 syntax.
- **Configurability:** Easily configure the service through environment variables or a .env file.
- **Notification Channels:** Automatically create endpoints for notification channels based on your templates.
- **Your Way or Who Cares:** Use built-in templates or add your own.

## Requirements

- Python 3.8 or higher
- FastAPI
- Jinja2
- HTTPX
- Decouple
- Prometheus FastAPI Instrumentator (for metrics)

## Configuration

To overwrite configurations, either create environment variables or create a `.env` file with the following structure in the project folder:

```
NTFY_ADDRESS=https://your-notification-service.com
TEMPLATES_FOLDER=templates
INCLUDE_TEMPLATES=grafana;slack
DRY_RUN=false
```

## Installation

1. Install the required dependencies using:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the prty-fast service:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --log-config=log_conf.yaml
   ```

3. Access the service at `http://localhost:8000`.

## Usage

To use prty-fast, follow these steps:

1. Specify the built-in templates you want to use by listing them in the `INCLUDE_TEMPLATES` environment variable, separated by semicolons.
2. If you need additional custom templates, create them in the designated `TEMPLATES_FOLDER`.
3. Access different endpoints for various notification channels based on the template names. For example, if you have a template called `sonarr.j2` in the templates folder, an endpoint `/sonarr` will be created. Any message sent to that endpoint will be transformed and forwarded to the `ntfy` service under the topic `sonarr`. The same applies to built-in templates like `grafana`. Messages sent to `/grafana` will be transformed and passed through to the `grafana` topic.

**Note: Any changes made to the templates will require a restart of the prty-fast service for the changes to take effect.**

## Running with Docker

To run this application using Docker, you have two options:

1. Using the `docker run` command:
    ```bash
    docker run -d \
         -e NTFY_ADDRESS=https://your-notification-service.com \
         -e "INCLUDE_TEMPLATES=grafana;slack" \
         -e DRY_RUN=false \
         -p 8000:8000 \
         -v <host folder with custom templates>:/app/templates \
         ghcr.io/hbdk/prty-fast
    ```

2. Using Docker Compose:
    ```yaml
    version: '3.8'
    services:
       prty-fast:
          image: ghcr.io/hbdk/prty-fast
          environment:
             NTFY_ADDRESS: https://your-notification-service.com
             INCLUDE_TEMPLATES: grafana;slack
             DRY_RUN: false
          ports:
             - "8000:8000"
          volumes:
             - <host folder with custom templates>:/app/templates # Optional
    ```
## Metrics

prty-fast uses Prometheus FastAPI Instrumentator for metrics. Metrics are exposed at `/metrics`.

## HTML Page

To view a simple HTML page that shows project information, loaded templates, and the address and availability of the ntfy service, access the root endpoint (`/`).

## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
