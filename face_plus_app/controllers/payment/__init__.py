# -*- coding: utf-8 -*-
from odoo import http
from . import pay
import json

class Payment(http.Controller):
    pay = pay.pay
    
    def get_pay_to_dict(self, payments:None):
        pay_dict = [{
            'id': pay['id'],
            'message': pay['message'],
            'status': pay['status'],
        } for pay in payments]

        return pay_dict
    