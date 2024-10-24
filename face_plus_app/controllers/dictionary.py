from . import auth_engine
from odoo import http
import random
from datetime import datetime

def get_login_user():
    token_data = auth_engine.validate()
    return token_data.get('user')
