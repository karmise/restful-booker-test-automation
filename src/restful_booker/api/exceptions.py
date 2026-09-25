class ApiTransportError(RuntimeError):
    """Raised when an HTTP request cannot be completed."""


class KnownSandboxDefectError(AssertionError):
    """An explicitly declared response status reproduced a known sandbox defect."""
