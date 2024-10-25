
from PIL import Image
import io
import base64
import requests
import openai
import os

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError

class FacePlusSlider(models.Model):
    _name = "face.plus.slider"
    _description = "Face Plus Slider"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id'

    name = fields.Char(string='Title')
    sub_title = fields.Char(string='Sub Title')
    image = fields.Image(string='Image', attachment=True)
    