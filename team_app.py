#!/usr/bin/env python
# coding=utf-8
"""
Manage.py commands
"""
import sys

from object_registry import finalize_app_initialization
from app.app import create_app

app = create_app()

if 'db' not in sys.argv:
    finalize_app_initialization()