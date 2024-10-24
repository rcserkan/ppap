# -*- coding: utf-8 -*-
from odoo import http
from . import signin
from . import user_get
from . import user_create
from .. import auth_engine

class PlatformAuth(http.Controller):
    signin = signin.signin
    user_get = user_get.user_get
    user_create = user_create.user_create

    def get_user_to_dict(self, users: None):
        user_dict = [{
            'id': user.id,
            'name': user.name,
            'email': user.login,
            'gender': user.gender,
            'phone': user.phone,
            'user_type': 'customer',
            'image': user.image_1920,
        } for user in users]

        return user_dict
    
    def get_login_user():
        token_data = auth_engine.validate()
        return token_data.get('user')
