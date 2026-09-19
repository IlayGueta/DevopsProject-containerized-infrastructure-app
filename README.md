# Containerized Infrastructure Provisioning API

A containerized Python REST API that simulates infrastructure machine provisioning.

The application is built with Flask, validates machine data with Pydantic, stores machine records in a JSON file, and can run locally, inside a Docker container, or inside Kubernetes using Helm.

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
- Public Docker image available through Docker Hub
- Kubernetes deployment using Helm
- Configurable replica count
- Configurable Kubernetes resource requests and limits
- Kubernetes readiness and liveness health probes
- Internal Kubernetes Service
- NGINX Ingress support
- Helm upgrade and rollback support

---

## Technologies

- Python 3.12
- Flask
- Pydantic
- Docker
- Docker Hub
- Kubernetes
- Helm
- NGINX Ingress Controller
- Git

---

## Project Structure

```text
.
├── app.py
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
├── README.md
│
├── chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── _helpers.tpl
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       └── NOTES.txt
│
├── configs/
│   └── instances.json
│
├── logs/
│
├── scripts/
│   └── install_nginx.sh
│
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
- `chart/Chart.yaml` — Helm chart metadata
- `chart/values.yaml` — configurable Helm deployment values
- `chart/templates/deployment.yaml` — Kubernetes Deployment
- `chart/templates/service.yaml` — Kubernetes Service
- `chart/templates/ingress.yaml` — Kubernetes Ingress
- `chart/templates/_helpers.tpl` — reusable Helm template helper
- `chart/templates/NOTES.txt` — usage information displayed by Helm after deployment

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

By default, changes made inside a running Docker container are removed when the container is deleted.

For persistent Docker storage, mount the configuration directory as a bind mount.

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

### Kubernetes Note

The current Helm deployment does not configure persistent Kubernetes storage.

The application stores machine data locally inside each Pod. For this reason, the default Helm configuration uses one replica.

Data written inside a Pod may be lost if that Pod is deleted or replaced.

---

## Docker Hub

The application image is publicly available on Docker Hub:

```text
ilaygueta/ilay-infrastructure-api:1.0.0
```

Pull the image:

```bash
docker pull ilaygueta/ilay-infrastructure-api:1.0.0
```

Run it:

```bash
docker run -d -p 5000:5000 ilaygueta/ilay-infrastructure-api:1.0.0
```

The public Docker Hub image also allows Kubernetes nodes to pull the application image automatically during Helm deployment.

---

# Kubernetes Deployment with Helm

The application includes a Helm chart under:

```text
chart/
```

The chart deploys:

- Kubernetes Deployment
- Kubernetes Service
- Kubernetes Ingress
- Readiness probe
- Liveness probe
- Resource requests and limits

---

## Prerequisites

Before deploying with Helm, make sure the following are available:

- Docker
- Kubernetes cluster
- `kubectl`
- Helm
- NGINX Ingress Controller

Verify that Kubernetes is running:

```bash
kubectl get nodes
```

---

## Helm Configuration

Default Helm values are defined in:

```text
chart/values.yaml
```

Current configuration:

```yaml
replicaCount: 1

image:
  repository: ilaygueta/ilay-infrastructure-api
  tag: "1.0.0"
  pullPolicy: IfNotPresent

app:
  port: 5000

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  host: infrastructure.local
  path: /
  pathType: Prefix

resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "256Mi"
```

The Flask application listens inside the container on:

```text
5000
```

The Kubernetes Service exposes:

```text
80
```

and forwards traffic to the application on port `5000`.

The traffic flow is:

```text
Ingress
   |
   v
Service :80
   |
   v
Pod / Flask :5000
```

---

## Validate the Helm Chart

Before deploying, validate the chart:

```bash
helm lint ./chart
```

Render the Kubernetes manifests without installing them:

```bash
helm template flask-monitor ./chart
```

A successful lint should report:

```text
1 chart(s) linted, 0 chart(s) failed
```

---

## Install NGINX Ingress Controller

The Helm chart is configured to use the NGINX Ingress Controller.

Install it with Helm:

```bash
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace
```

Verify the controller:

```bash
kubectl get pods -n ingress-nginx
```

---

## Install the Application

Deploy the application:

```bash
helm install flask-monitor ./chart
```

Verify the Kubernetes resources:

```bash
kubectl get pods,svc,ingress
```

The application Pod should reach:

```text
READY 1/1
STATUS Running
```

---

## Health Checks

The Kubernetes Deployment uses both readiness and liveness probes.

Both probes use:

```text
/health
```

on the application port:

```text
5000
```

### Readiness Probe

Determines whether the application is ready to receive traffic.

If the probe fails, Kubernetes stops sending Service traffic to the Pod until it becomes ready again.

### Liveness Probe

Determines whether the application is still healthy.

If the application repeatedly fails the liveness check, Kubernetes can restart the container.

---

## Access Through Ingress

The default Ingress host is:

```text
infrastructure.local
```

The host can be customized through `values.yaml`.

For example:

```bash
helm upgrade flask-monitor ./chart \
  --set ingress.host=myapp.example.com
```

---

## Local kind / Docker Desktop Access

When Kubernetes is running through kind or Docker Desktop, the external IP assigned to the NGINX Ingress Controller may belong to an internal Docker network and may not be directly reachable from the host machine.

In that case, forward a local port to the Ingress Controller:

```bash
kubectl port-forward \
  -n ingress-nginx \
  service/ingress-nginx-controller \
  8080:80
```

Then test the application:

```bash
curl -H "Host: infrastructure.local" http://localhost:8080/
```

Test the health endpoint:

```bash
curl -H "Host: infrastructure.local" http://localhost:8080/health
```

---

## Customize the Deployment

The Helm chart can be customized without modifying the Kubernetes templates.

For example, change the replica count:

```bash
helm upgrade flask-monitor ./chart \
  --set replicaCount=2
```

Verify the Pods:

```bash
kubectl get pods
```

Values can also be overridden using another values file:

```bash
helm upgrade flask-monitor ./chart -f my-values.yaml
```

---

## Helm Upgrade

After changing `values.yaml`, apply the new configuration:

```bash
helm upgrade flask-monitor ./chart
```

View release history:

```bash
helm history flask-monitor
```

---

## Helm Rollback

Rollback to a previous revision:

```bash
helm rollback flask-monitor <revision>
```

Example:

```bash
helm rollback flask-monitor 1
```

Verify the deployment afterward:

```bash
kubectl get pods,svc,ingress
```

---

## Helm Notes

After installation or upgrade, Helm displays deployment information from:

```text
chart/templates/NOTES.txt
```

The release notes include useful commands for checking the deployment and accessing the application.

They can also be displayed later with:

```bash
helm get notes flask-monitor
```

---

## Uninstall the Helm Release

Remove the application:

```bash
helm uninstall flask-monitor
```

To also remove the NGINX Ingress Controller:

```bash
helm uninstall ingress-nginx -n ingress-nginx
```

---

## Notes

- The application binds to `0.0.0.0` so it can be accessed outside the container.
- `EXPOSE 5000` documents the application container port.
- Docker port publishing is performed at runtime with `-p 5000:5000`.
- Kubernetes exposes the application internally through a `ClusterIP` Service on port `80`.
- The Service forwards traffic to the Flask application on port `5000`.
- NGINX Ingress routes external HTTP traffic to the Kubernetes Service.
- The Docker image used by Kubernetes is hosted publicly on Docker Hub.
- Flask's built-in server is suitable for development and project demonstrations.
- For a production deployment, use a production WSGI server such as Gunicorn.
- Kubernetes persistent storage is not configured in the current version.

---

## 👨‍💻 Author

Ilay Gueta

- GitHub: @IlayGueta
- Project: DevopsProject-containerized-infrastructure-app