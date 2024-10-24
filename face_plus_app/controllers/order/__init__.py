# -*- coding: utf-8 -*-
from odoo import http
from . import order_list
from . import order_create
import json

class Order(http.Controller):
    order_list = order_list.order_list
    order_create = order_create.order_create
    
    def get_order_to_dict(self, orders:None):
        orders_dict = [{
            'id': order.id,
            'name': order.name,
            'chat_gpt_result': order.chat_gpt_result,
            'image': self.get_image(order)
        } for order in orders]

        return orders_dict
    
    def get_image(self, order):
        return http.request.env['ir.attachment'].sudo().search([('res_model', '=', 'face.plus.order'), ('res_id', '=', order.id)], limit=1).local_url