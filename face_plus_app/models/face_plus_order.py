
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
    type = fields.Selection(
        [
            ('character', 'Karakter Analizi'),
            ('skin', 'Cilt ve Güzellik Analizi'),
            ('mood', 'Ruh Hali ve Bilinçaltı Analizi'),
            ('dream', 'Rüya Analizi'),
            ('style', 'Görünüm ve Stil Önerileri'),
            ('wish', 'Dilek ve Sorun Çözme Modülü'),
            ('nutrition', 'Beslenme ve Sağlıklı Yaşam Modülü'),
            ('personal', 'Kişisel Gelişim ve Hedef Modülü'),
        ]
    )
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
        # api_key = "PHfsBXJr2VjNJcgZCKTqOroWg3a6n5GU"
        # api_secret = "v-IUIvlHCqohu_tCLoRs84nMRKi0ON7T"
        # url = "https://api-us.faceplusplus.com/facepp/v1/skinanalyze"

        attachment_id = self.env['ir.attachment'].search([('res_model', '=', 'face.plus.order'), ('res_id', '=', self.id)], limit=1)
        if attachment_id:
            
            data = {
                'api_key': api_key,
                'api_secret': api_secret,
                'image_base64': attachment_id.datas.decode('utf-8')
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

        # API anahtarını al
        openai_key = ConfigModel.get_param('face_plus_app.openai_key')
        if not openai_key:
            raise ValueError("API anahtarı bulunamadı. Lütfen 'face_plus_app.openai_key' ayarını kontrol edin.")

        openai.api_key = openai_key

        props = ConfigModel.get_param('face_plus_app.openai_props_karakter') or ""
        if self.type == 'skin': 
            props = ConfigModel.get_param('face_plus_app.openai_props_skin') or ""
        elif self.type == 'mood': 
            props = ConfigModel.get_param('face_plus_app.openai_props_mood') or ""
        elif self.type == 'dream': 
            props = ConfigModel.get_param('face_plus_app.openai_props_dream') or ""
        elif self.type == 'style': 
            props = ConfigModel.get_param('face_plus_app.openai_props_style') or ""
        elif self.type == 'wish': 
            props = ConfigModel.get_param('face_plus_app.openai_props_wish') or ""
        elif self.type == 'nutrition': 
            props = ConfigModel.get_param('face_plus_app.openai_props_nutrition') or ""
        elif self.type == 'personal': 
            props = ConfigModel.get_param('face_plus_app.openai_props_personal') or ""
        else:
            pass

        content = f"{self.summary} {props}"

        try:
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": content}]
            )

            if chat_completion.choices and chat_completion.choices[0].message:
                self.update({
                    'chat_gpt_result': chat_completion.choices[0].message['content']
                })
            else:
                raise ValueError("Geçerli bir yanıt alınamadı. Yanıt formatı beklenenden farklı.")
        except openai.error.OpenAIError as e:
            raise ValueError(f"OpenAI API hatası: {str(e)}")
        except Exception as e:
            raise ValueError(f"Beklenmedik bir hata oluştu: {str(e)}")