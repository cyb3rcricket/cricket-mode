"""Shared Cricket conformance checks. Adapters import this instead of copying rules."""

from conformance.check import evaluate, load_cases

__all__ = ["evaluate", "load_cases"]
