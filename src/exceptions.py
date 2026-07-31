"""Custom exceptions for VM validation."""


class VMValidationError(Exception):
    """Base exception for all VM validation errors."""
    pass


class VMNameError(VMValidationError):
    """VM name validation errors."""
    pass


class VMResourceError(VMValidationError):
    """VM resource (CPU/RAM) validation errors."""
    pass


class VMOSError(VMValidationError):
    """VM operating system validation errors."""
    pass