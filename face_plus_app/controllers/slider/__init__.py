# -*- coding: utf-8 -*-
from odoo import http
from . import slider_list
import json

class Slider(http.Controller):
    slider_list = slider_list.slider_list
    
    def get_slider_to_dict(self, sliders:None):
        sliders_dict = [{
            'id': slider.id,
            'name': slider.name,
            'sub_title': slider.sub_title,
            'image': slider.image,
            # 'image': f"data:image/jpeg;base64,{slider.image}",
        } for slider in sliders]

        return sliders_dict
    
    def get_image(self, order):
        return http.request.env['ir.attachment'].sudo().search([('res_model', '=', 'face.plus.order'), ('res_id', '=', order.id)], limit=1).local_url