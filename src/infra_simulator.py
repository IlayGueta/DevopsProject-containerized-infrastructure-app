import subprocess
import logging

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
        """Execute the Bash script used to install the required service."""

        logger.info(f"Running installation script for Machine - {self.machine.name}...")
        try:
            # Execute the Bash script and raise an error if it fails
            subprocess.run(["sh", "scripts/install_nginx.sh"], check=True)
            logger.info("Installation script completed successfully")
        except subprocess.CalledProcessError as e:
            # Record the failure without crashing the entire application
            logger.warning(f"Script failed with return code {e.returncode}, output: {e.output}")