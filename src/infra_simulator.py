import logging
import shutil
import subprocess
from pathlib import Path

from constants import LOGGER_NAME

# Create a logger using the shared logger name
logger = logging.getLogger(LOGGER_NAME)


class InfrastructureProvisioner:
    """Simulate the provisioning and configuration of a virtual machine."""

    def __init__(self, machine):
        """Store the machine that will be provisioned."""

        self.machine = machine

    def create_vm(self):
        """Simulate the creation of a virtual machine."""

        logger.info(f"Creating virtual machine: {self.machine.name}")

    def install_os(self):
        """Simulate the installation of the selected operating system."""

        logger.info(f"Installing operating system: {self.machine.os}")

    def configure_resources(self):
        """Simulate the configuration of CPU and RAM resources."""

        logger.info(f"Configuring CPU: {self.machine.cpu}")
        logger.info(f"Configuring RAM: {self.machine.ram}")

    def configure_network(self):
        """Simulate the configuration of the machine network."""

        logger.info(f"Configuring network settings for {self.machine.name}...")

    def finish(self):
        """Record the successful completion of the provisioning process."""

        logger.info(f"Provisioning completed successfully for Machine - {self.machine.name}.")

    def provision(self):
        """Run all infrastructure provisioning steps in the correct order."""

        logger.info("Starting infrastructure provisioning...")
        self.create_vm()
        self.install_os()
        self.configure_resources()
        self.configure_network()
        self.run_install_script()
        self.finish()

    def run_install_script(self):
        """Run the Bash installation script when a shell is available."""

        script_path = (
            Path(__file__).resolve().parent.parent
            / "scripts"
            / "install_nginx.sh"
        )

        shell_path = shutil.which("sh")

        if shell_path is None:
            logger.warning(
                "The 'sh' command is unavailable. "
                "Skipping the Bash script on this operating system."
            )
            return

        logger.info(
        f"Running installation script for Machine - {self.machine.name}..."
    )

        try:
            result = subprocess.run(
            [shell_path, str(script_path)],
            check=True,
            capture_output=True,
            text=True
        )

            logger.info(result.stdout.strip())
            logger.info("Installation script completed successfully")

        except subprocess.CalledProcessError as error:
            logger.warning(
            "Installation script failed with return code "
            f"{error.returncode}: {error.stderr}"
        )