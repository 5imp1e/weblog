# !/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint

#下一行的位置很重要。。。。
main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
