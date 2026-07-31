import logging
import uuid

from pydantic import BaseModel, Field, field_validator

from constants import AVAL_RAM, MAX_NAME_LENGTH, AVAL_CPUS, OS_OPTIONS, LOGGER_NAME
from exceptions import VMNameError, VMOSError, VMResourceError

logger = logging.getLogger(LOGGER_NAME)


class Machine(BaseModel):
    """Represent and validate a virtual machine configuration."""

    # Generate a unique UUID automatically for every machine
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    os: str
    cpu: str
    ram: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """Normalize and validate the machine name."""

        value = value.strip().lower()
        if not value:
            logger.error("Machine name must not be empty")
            raise VMNameError("VM name cannot be empty")
        if len(value) > MAX_NAME_LENGTH:
            logger.error(f"Machine name must be less than {MAX_NAME_LENGTH} characters")
            raise VMNameError(f"VM name must be {MAX_NAME_LENGTH} characters or less")
        return value

    @field_validator("os")
    @classmethod
    def validate_os(cls, value: str) -> str:
        """Normalize and validate the selected operating system."""

        value = value.strip().lower()
        if value not in OS_OPTIONS:
            logger.error(f"Operating system must be one of: {OS_OPTIONS}")
            raise VMOSError(f"OS must be one of: {', '.join(OS_OPTIONS)}")
        return value

    @field_validator("cpu")
    @classmethod
    def validate_cpu(cls, value: str) -> str:
        """Validate the CPU format and available CPU value."""

        value = value.strip().lower()
        if not value.endswith("vcpu"):
            logger.error("CPU format must be like '4vcpu'")
            raise VMResourceError("CPU format must be like '4vcpu'")

        try:
            # Extract the numeric CPU value from input such as "4vcpu"
            num = int(value.replace("vcpu", ""))
        except ValueError:
            logger.error("CPU must contain a valid number")
            raise VMResourceError("CPU must contain a valid number")

        if num not in AVAL_CPUS:
            logger.error(f"CPU must be one of: {AVAL_CPUS}")
            raise VMResourceError(f"CPU must be one of: {AVAL_CPUS} vCPUs")
        return value

    @field_validator("ram")
    @classmethod
    def validate_ram(cls, value: str) -> str:
        """Validate the RAM format and available RAM value."""

        value = value.strip().lower()
        if not value.endswith("gb"):
            logger.error("RAM format must be like '8gb'")
            raise VMResourceError("RAM format must be like '8gb'")

        try:
            # Extract the numeric RAM value from input such as "8gb"
            num = int(value.replace("gb", ""))
        except ValueError:
            logger.error("RAM must contain a valid number")
            raise VMResourceError("RAM must contain a valid number")

        if num not in AVAL_RAM:
            logger.error(f"RAM must be one of: {AVAL_RAM}")
            raise VMResourceError(f"RAM must be one of: {AVAL_RAM} GB")
        return value

    def log_creation(self):
        """Record the successful creation of the machine."""

        logger.info(f"Machine created: {self.name} (id={self.id})")

    def to_dict(self) -> dict:
        """Convert the Machine model into a dictionary."""

        return self.model_dump()