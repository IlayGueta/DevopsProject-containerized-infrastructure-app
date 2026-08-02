import os
import sys
from pathlib import Path

from flask import Flask, jsonify, request
from pydantic import ValidationError

BASE_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(BASE_DIR / "src"))

from automation import InfraAutomation
from exceptions import VMNameError, VMValidationError

app = Flask(__name__)

InfraAutomation.initialize_logger()

config_path = BASE_DIR / "configs" / "instances.json"
infra_automation = InfraAutomation(config_path=str(config_path))

@app.get("/")
def home():
    """Return basic information about the application."""

    return jsonify(
        {
            "application": "Infrastructure Provisioning API",
            "message": "The containerized infrastructure application is running!",
            "endpoints": {
                "health": "GET /health",
                "get_machines": "GET /machines",
                "create_machine": "POST /machines"   
            }
        }
    )


@app.get("/health")
def health():
    """Return the current application health status."""

    return jsonify(
        {
            "status": "healthy"
        }
    )


@app.get("/machines")
def get_machines():
    """Return all machines stored in the configuration file."""

    machines = infra_automation.read_config_file()
    return jsonify(machines)

@app.post("/machines")
def create_machine():
    """Create a new machine from a JSON request."""

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            {
                "error": "Request body must contain valid JSON"
            }
        ), 400

    required_fields = {"name", "os", "cpu", "ram"}
    missing_fields = sorted(required_fields - data.keys())

    if missing_fields:
        return jsonify(
            {
                "error": "Missing required fields",
                "missing_fields": missing_fields
            }
        ), 400

    try:
        machine_data = infra_automation.create_machine(
            name=data["name"],
            os_name=data["os"],
            cpu=data["cpu"],
            ram=data["ram"]
        )

        return jsonify(
            {
                "message": "Machine created successfully",
                "machine": machine_data
            }
        ), 201

    except VMNameError as error:
        return jsonify(
            {
                "error": str(error)
            }
        ), 409

    except VMValidationError as error:
        return jsonify(
            {
                "error": str(error)
            }
        ), 400

    except ValidationError as error:
        return jsonify(
            {
                "error": "Invalid machine data",
                "details": error.errors(include_url=False)
            }
        ), 400

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )