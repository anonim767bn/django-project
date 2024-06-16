"""Custom template filters."""
from typing import Any

from django import template

register = template.Library()


@register.filter
def get_attribute(just_object: Any, attr: str) -> Any | str:
    """Retrieve an attribute from an object.

    Args:
        just_object (Any): Any object.
        attr (str): An attribute.

    Returns:
        Any | str: attribute or 'неизвестно'
    """
    return getattr(just_object, attr) or 'неизвестно'
