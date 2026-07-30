"""Safe Allure steps that do not serialize wrapped function arguments."""

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

import allure

P = ParamSpec("P")
R = TypeVar("R")


def report_step(title: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Wrap a framework operation in a fixed-title Allure step.

    The standard ``@allure.step`` decorator records function arguments as step
    parameters. Framework actions can receive credentials, tokens, or complete
    DTOs, so this adapter intentionally uses the context API and exposes only
    the curated title.
    """

    def decorator(function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            with allure.step(title):
                return function(*args, **kwargs)

        return wrapper

    return decorator
