
from PIL import Image
import io
import base64
import requests
import openai
import os

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError

class FacePlusOrder(models.Model):
    _name = "face.plus.order"
    _description = "Face Plus Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id'

    name = fields.Char(string='Name')
    summary = fields.Html(string='Summary')
    chat_gpt_result = fields.Text(string='Gpt Result')

    @api.model
    def create(self, vals):
        templates = super(FacePlusOrder,self).create(vals)
        seq = self.env['ir.sequence'].get('face.plus.order')
        templates.name = seq
        return templates

    def run_face_plus_report(self):
        # https://console.faceplusplus.com/documents/129100210
        ConfigModel = self.env['ir.config_parameter'].sudo()
        api_key = ConfigModel.get_param('face_plus_app.face_plus_key')
        api_secret = ConfigModel.get_param('face_plus_app.face_plus_secret')
        url = ConfigModel.get_param('face_plus_app.face_plus_url')


        attachment_id = self.env['ir.attachment'].search([('res_model', '=', 'face.plus.order'), ('res_id', '=', self.id)], limit=1)
        if attachment_id:
            image_base64_data = attachment_id.datas.decode('utf-8').strip().replace("dataimage/jpegbase64","")
            image_base64 = f"data:image/jpeg;base64,{image_base64_data}"

            data = {
                'api_key': api_key,
                'api_secret': api_secret,
                'image_base64': image_base64
            }
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                result = response.json()
                self.update({
                    'summary': result['result']
                })
            else:
                print("Hata oluştu:", response.status_code, response.text) 

    def run_chat_gpt_report(self):
        ConfigModel = self.env['ir.config_parameter'].sudo()

        os.environ["OPENAI_API_KEY"] = ConfigModel.get_param('face_plus_app.openai_key')
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

        openai.api_key = api_key
        content = "%s %s" % (self.summary, ConfigModel.get_param('face_plus_app.openai_props')) 

        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": content}
            ]
        )
        
        self.update({
            'chat_gpt_result': chat_completion.choices[0].message['content']
        })