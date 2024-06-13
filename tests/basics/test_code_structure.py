import importlib
import inspect
import os
import pkgutil

import pytest
from fastapi import APIRouter

from app import database, main, models, routers

# List of expected modules and their expected submodules or classes
EXPECTED_STRUCTURE = {
    "models": [
        "common",
        "users",
        "products",
        "orders",
        "subscriptions",
        "promotions",
        "pricing",
        "authentication",
    ],
    "models.common": [
        "BaseMixin",
        "BulkActionsMixin",
        "CachingMixin",
        "SearchMixin",
    ],
    # ... add more expectations for users, products, orders, etc.
    "routers": [
        "users",  # 'products', 'orders', etc. - as needed
    ],
    "database": [
        "get_db",
        "app_lifespan",
        "engine",
    ],
}


def test_module_structure():
    """Test if the project has the expected module structure."""
    for module_name, expected_submodules in EXPECTED_STRUCTURE.items():
        module = importlib.import_module("app." + module_name)

        # Check if submodules exist
        if isinstance(expected_submodules, list):
            for submodule_name in expected_submodules:
                assert hasattr(
                    module, submodule_name
                ), f"Module 'app.{module_name}' is missing submodule '{submodule_name}'"

        # Check if classes exist
        elif isinstance(expected_submodules, dict):
            for class_name in expected_submodules:
                assert hasattr(
                    module, class_name
                ), f"Module 'app.{module_name}' is missing class '{class_name}'"


def test_routers_have_prefix():
    """Test if all routers have a prefix defined."""
    for _, module_name, _ in pkgutil.iter_modules(routers.__path__):
        module = importlib.import_module(f"app.routers.{module_name}")
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, APIRouter):
                assert (
                    obj.prefix
                ), f"Router '{name}' in module 'app.routers.{module_name}' is missing a prefix"
