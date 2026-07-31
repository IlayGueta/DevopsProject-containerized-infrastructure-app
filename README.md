# DevOps Infrastructure Automation — User Guide

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Pydantic](https://img.shields.io/badge/Pydantic-2.0+-green)
![Status](https://img.shields.io/badge/Status-Active-success)

> ⚠️ **Recommended environment:** Linux, WSL, or Git Bash on Windows. The provisioning process executes a Bash (`.sh`) script.

---

## 📖 Overview

This project is a command-line infrastructure automation tool written in Python. It accepts virtual machine specifications from the user, validates them with Pydantic, saves them in a JSON configuration file, simulates the provisioning process, executes a Bash installation script, and records activity in a log file.

The current provisioning process is simulated. Future versions can integrate Terraform and AWS to create real infrastructure resources.

---

## ✨ Features

- **Automated VM Provisioning** — Define and provision virtual machines through a CLI
- **Pydantic Validation** — Validate all machine specifications automatically
- **Configuration Management** — Store VM configurations persistently in JSON
- **Unique Identifiers** — Generate a UUID for every machine
- **Duplicate Protection** — Prevent machines from using an existing name
- **Custom Exceptions** — Provide clear, structured validation errors
- **Bash Automation** — Execute a service installation script with Python
- **Logging System** — Record machine creation and provisioning activity
- **Modular Design** — Separate models, validation, provisioning, constants, and exceptions

---

## 🛠️ Technologies

- **Python 3.8+** — Core programming language
- **Pydantic 2.0+** — Data modelling and validation
- **UUID** — Unique machine identifiers
- **JSON** — Persistent configuration storage
- **Logging** — Operation and error tracking
- **Bash** — Service installation automation
- **Git** — Version control

### Future Enhancements

- Docker containerization
- Terraform integration
- AWS deployment
- Web API with FastAPI
- Database support with SQLite or PostgreSQL

---

## 📁 Project Structure

```text
infrastracture-provisioning/
├── configs/
│   └── instances.json
├── logs/
│   └── provisioning.log
├── scripts/
│   └── install_nginx.sh
├── src/
│   ├── automation.py
│   ├── constants.py
│   ├── exceptions.py
│   ├── infra_simulator.py
│   └── machine.py
├── README.md
└── requirements.txt
```

---

## 🧱 Architecture

- **`automation.py`** — Application entry point, user input, JSON reading and writing, and workflow management
- **`machine.py`** — Pydantic `Machine` model and VM specification validation
- **`infra_simulator.py`** — Simulates infrastructure provisioning and runs the Bash script
- **`constants.py`** — Stores allowed resources, file paths, and shared constant values
- **`exceptions.py`** — Defines the project’s custom exceptions
- **`install_nginx.sh`** — Bash script used to simulate the Nginx installation process

---

## ✅ Prerequisites

Before installing the project, make sure the following tools are available:

- Python 3.8 or newer
- Git
- Bash through Linux, WSL, or Git Bash
- `pip`

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/IlayGueta/infrastracture-provisioning.git
cd infrastracture-provisioning
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

If your system uses `python3`, run:

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

#### Linux or WSL

```bash
source venv/bin/activate
```

#### Windows with Git Bash

```bash
source venv/Scripts/activate
```

#### Windows Command Prompt

```cmd
venv\Scripts\activate
```

#### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Give the Bash script execution permission

Run this command in Linux, WSL, or Git Bash:

```bash
chmod +x scripts/install_nginx.sh
```

---

## ▶️ Run the Application

Run the application from the project’s root directory.

### Linux or WSL

```bash
python3 src/automation.py
```

### Windows with Git Bash

```bash
python src/automation.py
```

Both commands launch the same application. The command depends on how Python is installed on the operating system.

---

## 💻 How to Use

The application prompts you to define virtual machines one at a time.

### 1. Machine Name

- Maximum of 10 characters
- Must not be empty
- Must be unique
- Enter `done` to finish and exit

### 2. Operating System

Choose one of the following values:

```text
ubuntu, centos
```

### 3. CPU

Choose one of the following values:

```text
1vcpu, 2vcpu, 4vcpu, 8vcpu, 16vcpu
```

### 4. RAM

Choose one of the following values:

```text
2gb, 4gb, 8gb, 16gb, 32gb, 64gb
```

---

## 📋 Example Session

```text
Welcome to Infra Automation!

Enter machine name (or 'done' to finish): web
Enter OS ['ubuntu', 'centos']: ubuntu
Enter CPU (e.g., 2vCPU): Available resources [1, 2, 4, 8, 16] vCPUs : 4vcpu
Enter RAM (e.g., 4GB): Available resources in GB [2, 4, 8, 16, 32, 64] : 8gb

Enter machine name (or 'done' to finish): done

Created machines: [{'id': '7db4308f-...', 'name': 'web', 'os': 'ubuntu', 'cpu': '4vcpu', 'ram': '8gb'}]
```

---

## ⚙️ How It Works

1. The application collects the machine name, operating system, CPU, and RAM from the user.
2. Pydantic validates the values through the `Machine` model.
3. The application checks that the machine name does not already exist.
4. A UUID is generated automatically for the machine.
5. The machine configuration is appended to `configs/instances.json`.
6. `InfrastructureProvisioner` simulates the provisioning steps.
7. Python uses `subprocess` to execute `scripts/install_nginx.sh`.
8. Provisioning activity and errors are written to `logs/provisioning.log`.

---

## ❌ Failure Examples

### Name too long

```text
Enter machine name (or 'done' to finish): verylongname

VMNameError: VM name must be 10 characters or less
```

### Empty name

```text
Enter machine name (or 'done' to finish):

VMNameError: VM name cannot be empty
```

### Duplicate machine name

```text
Enter machine name (or 'done' to finish): web

VMNameError: Machine name already exists
```

### Invalid operating system

```text
Enter OS ['ubuntu', 'centos']: windows

VMOSError: OS must be one of: ubuntu, centos
```

### Wrong CPU format

```text
Enter CPU (e.g., 2vCPU): Available resources [1, 2, 4, 8, 16] vCPUs : 4 cores

VMResourceError: CPU format must be like '4vcpu'
```

### Invalid CPU value

```text
Enter CPU (e.g., 2vCPU): Available resources [1, 2, 4, 8, 16] vCPUs : 3vcpu

VMResourceError: CPU must be one of: [1, 2, 4, 8, 16] vCPUs
```

### Wrong RAM format

```text
Enter RAM (e.g., 4GB): Available resources in GB [2, 4, 8, 16, 32, 64] : 8

VMResourceError: RAM format must be like '8gb'
```

### Invalid RAM value

```text
Enter RAM (e.g., 4GB): Available resources in GB [2, 4, 8, 16, 32, 64] : 10gb

VMResourceError: RAM must be one of: [2, 4, 8, 16, 32, 64] GB
```

---

## 📁 Output

### Configuration File

Created machines are stored in `configs/instances.json`:

```json
{
    "machines": [
        {
            "id": "7db4308f-4978-46d3-90fc-49bd5b4702f1",
            "name": "web",
            "os": "ubuntu",
            "cpu": "4vcpu",
            "ram": "8gb"
        }
    ]
}
```

New machines are appended to the `machines` list so existing records remain available.

### Log File

Provisioning operations are recorded automatically in:

```text
logs/provisioning.log
```

---

## 🔧 Troubleshooting

### `python3: command not found`

Try the Windows-style Python command:

```bash
python src/automation.py
```

### `python: command not found`

Try the Linux-style Python command:

```bash
python3 src/automation.py
```

### Bash is not available on Windows

Install Git Bash or run the project through WSL. Make sure the command is executed from the project’s root directory.

### Permission denied when running the installation script

```bash
chmod +x scripts/install_nginx.sh
```

### `ModuleNotFoundError: No module named 'pydantic'`

Activate the virtual environment and install the dependencies:

```bash
pip install -r requirements.txt
```

### Machine name already exists

Use a different machine name or review the existing records in `configs/instances.json`.

---

## 📝 Development Notes

- Run the program from the repository’s root directory so relative file paths work correctly.
- Do not delete the `configs` or `logs` directories.
- The project currently simulates VM provisioning and does not create real cloud resources.
- The Bash script requires an environment that supports Bash commands.

---

## 👨‍💻 Author

**Ilay Gueta**

- GitHub: [@IlayGueta](https://github.com/IlayGueta)
- Project: [Infrastructure Provisioning](https://github.com/IlayGueta/infrastracture-provisioning)