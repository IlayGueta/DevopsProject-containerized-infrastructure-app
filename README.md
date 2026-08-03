# Containerized Infrastructure Provisioning API

A containerized Python REST API that simulates infrastructure machine provisioning.

The application is built with **Flask**, validates machine data with **Pydantic**, stores machine records in a JSON file, and runs inside a **Docker container**.

---

## Features

- Runs as a persistent web service
- Listens on port `5000`
- Returns JSON responses
- Provides a health-check endpoint
- Displays all provisioned machines
- Creates new machines through an HTTP `POST` request
- Validates machine name, operating system, CPU, and RAM
- Prevents duplicate machine names
- Simulates infrastructure provisioning
- Can be built and executed as a Docker image

---

## Technologies

- Python 3.12
- Flask
- Pydantic
- Docker
- Git

---

## Project Structure

```text
.
├── app.py
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── README.md
├── configs/
│   └── instances.json
├── logs/
├── scripts/
│   └── install_nginx.sh
└── src/
    ├── automation.py
    ├── constants.py
    ├── exceptions.py
    ├── infra_simulator.py
    └── machine.py
```

### Main Files

- `app.py` — Flask application and REST API endpoints
- `src/automation.py` — machine creation, validation flow, storage, and provisioning logic
- `src/machine.py` — Pydantic model and machine validation
- `src/infra_simulator.py` — infrastructure provisioning simulation
- `configs/instances.json` — stores created machine records
- `scripts/install_nginx.sh` — installation simulation script
- `Dockerfile` — instructions for building the Docker image
- `.dockerignore` — excludes unnecessary files from the Docker build context

---

## API Endpoints

### Application Information

```http
GET /
```

Example response:

```json
{
  "application": "Infrastructure Provisioning API",
  "message": "The containerized infrastructure application is running!",
  "endpoints": {
    "health": "GET /health",
    "get_machines": "GET /machines",
    "create_machine": "POST /machines"
  }
}
```

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

### Get All Machines

```http
GET /machines
```

Example response:

```json
{
  "machines": [
    {
      "name": "web01",
      "os": "ubuntu",
      "cpu": "2vcpu",
      "ram": "4gb"
    }
  ]
}
```

### Create a Machine

```http
POST /machines
```

Request body:

```json
{
  "name": "web01",
  "os": "ubuntu",
  "cpu": "2vcpu",
  "ram": "4gb"
}
```

Successful response:

```json
{
  "message": "Machine created successfully",
  "machine": {
    "name": "web01",
    "os": "ubuntu",
    "cpu": "2vcpu",
    "ram": "4gb"
  }
}
```

Possible HTTP status codes:

- `201 Created` — machine created successfully
- `400 Bad Request` — missing or invalid data
- `409 Conflict` — machine name already exists
- `500 Internal Server Error` — unexpected application error

---

## Allowed Machine Values

### Operating Systems

```text
ubuntu
centos
```

### CPU

Use the format:

```text
2vcpu
```

Supported values depend on the validation rules defined in the project.

### RAM

Use the format:

```text
4gb
```

Supported values depend on the validation rules defined in the project.

---

## Run Locally Without Docker

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

On Windows, the Python launcher can also be used:

```powershell
py app.py
```

Open the application:

```text
http://localhost:5000
```

---

## Build the Docker Image

From the project root directory, run:

```bash
docker build -t ilay-infrastructure-api .
```

Verify that the image was created:

```bash
docker images
```

---

## Run the Docker Container

Run the container in detached mode:

```bash
docker run -d \
  --name ilay-app \
  --rm \
  -p 5000:5000 \
  ilay-infrastructure-api
```

PowerShell single-line version:

```powershell
docker run -d --name ilay-app --rm -p 5000:5000 ilay-infrastructure-api
```

Open:

```text
http://localhost:5000
```

---

## Test the API

### Browser

```text
http://localhost:5000
http://localhost:5000/health
http://localhost:5000/machines
```

### PowerShell — Create a Machine

```powershell
$body = @{
    name = "web01"
    os   = "ubuntu"
    cpu  = "2vcpu"
    ram  = "4gb"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/machines" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### curl

```bash
curl -X POST http://localhost:5000/machines \
  -H "Content-Type: application/json" \
  -d '{
    "name": "web01",
    "os": "ubuntu",
    "cpu": "2vcpu",
    "ram": "4gb"
  }'
```

---

## Container Management

Show running containers:

```bash
docker ps
```

View application logs:

```bash
docker logs ilay-app
```

Follow logs continuously:

```bash
docker logs -f ilay-app
```

Stop the container:

```bash
docker stop ilay-app
```

Because the container is started with `--rm`, it is removed automatically after it stops. The Docker image remains available locally.

---

## Data Persistence

Machine records are stored in:

```text
configs/instances.json
```

By default, changes made inside the running container are removed when the container is deleted.

For persistent storage, mount the configuration directory as a bind mount:

### PowerShell

```powershell
docker run -d `
  --name ilay-app `
  --rm `
  -p 5000:5000 `
  -v "${PWD}/configs:/home/app/configs" `
  ilay-infrastructure-api
```

### Linux / Git Bash

```bash
docker run -d \
  --name ilay-app \
  --rm \
  -p 5000:5000 \
  -v "$(pwd)/configs:/home/app/configs" \
  ilay-infrastructure-api
```

---

## Docker Hub

After tagging and pushing the image to Docker Hub, another user can run it without building the project locally.

Example format:

```bash
docker pull DOCKERHUB_USERNAME/ilay-infrastructure-api:1.0
docker run -d -p 5000:5000 DOCKERHUB_USERNAME/ilay-infrastructure-api:1.0
```

Replace `DOCKERHUB_USERNAME` with the correct Docker Hub username.

---

## Notes

- The application binds to `0.0.0.0` so it can be accessed outside the container.
- `EXPOSE 5000` documents the container port.
- Port publishing is performed at runtime with `-p 5000:5000`.
- Flask's built-in server is suitable for development and project demonstrations.
- For a production deployment, use a production WSGI server such as Gunicorn.

---

## 👨‍💻 Author

**Ilay Gueta**

- GitHub: [@IlayGueta](https://github.com/IlayGueta)
- Project: [DevopsProject-containerized-infrastructure-app](https://github.com/IlayGueta/DevopsProject-containerized-infrastructure-app)
