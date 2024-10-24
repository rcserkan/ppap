# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import JsonRPCDispatcher, Response
from . import auth
from . import order
import json
from odoo.tools import date_utils

old_response = JsonRPCDispatcher._response


def _response(self:JsonRPCDispatcher, result=None, error=None):
    if isinstance(result, Response):
        return result
    return old_response(self, result, error)

JsonRPCDispatcher._response = _response
