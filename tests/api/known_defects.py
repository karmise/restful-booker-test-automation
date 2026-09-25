"""Narrow expected failures to the observed sandbox behavior."""


class KnownSandboxDefectError(AssertionError):
    """A response reproduced the exact defect documented by a strict xfail."""
