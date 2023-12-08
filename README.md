# prty-fast

**Note: I am not a Python programmer, and this program is primarily AI-generated. The program should never be exposed publicly, and running it is entirely at your own risk. Use caution and discretion when handling sensitive information.**

prty-fast is a FastAPI-based service for sending notifications using configurable templates.

## Introduction

prty-fast allows you to define message templates using Jinja2 syntax and send notifications using those templates. The service is intended for internal use and should not be exposed to the public internet.

## Features

- **Template-based Notifications:** Define message templates using Jinja2 syntax.
- **Configurability:** Easily configure the service through a JSON configuration file.
- **Notification Channels:** Create endpoints for different notification channels based on your templates.
- **Dry Run Mode:** Test notifications without actually sending requests to the notification endpoint.

## Requirements

- Python 3.8 or higher
- FastAPI
- Jinja2
- HTTPX
- Decouple
- Prometheus FastAPI Instrumentator (for metrics)

## Configuration

Create a `config.json` file with the following structure:

```json
{
  "NTFY_ADDRESS": "https://your-notification-service.com",
  "TEMPLATES_FOLDER": "templates",
  "INCLUDE_TEMPLATES": "grafana;slack",
  "DRY_RUN": false
}
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

- Create Jinja2 templates in the specified `TEMPLATES_FOLDER`.
- Use different endpoints for various notification channels based on template names.

## Metrics

prty-fast uses Prometheus FastAPI Instrumentator for metrics. Metrics are exposed at `/metrics`.

## HTML Page

Access the root endpoint (`/`) to view a simple HTML page displaying project information, loaded templates, and the NTFY_ADDRESS.

## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
