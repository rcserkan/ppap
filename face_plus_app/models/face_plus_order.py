
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

    def download_image(self, url):
        local_filename = 'temp_image.jpg'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename

    def run_face_plus_report(self):
        # https://console.faceplusplus.com/documents/129100210
        ConfigModel = self.env['ir.config_parameter'].sudo()
        api_key = ConfigModel.get_param('face_plus_app.face_plus_key')
        api_secret = ConfigModel.get_param('face_plus_app.face_plus_secret')
        url = ConfigModel.get_param('face_plus_app.face_plus_url')

        data = {
            'api_key': api_key,
            'api_secret': api_secret,
        }

        attachment_id = self.env['ir.attachment'].search([('res_model', '=', 'face.plus.order'), ('res_id', '=', self.id)], limit=1)
        if attachment_id:
            local_image_path = self.download_image("https://cabinetra.com/wp-content/uploads/2024/10/pexels-reafonbgates-1498337-scaled.jpg") 
            with open(local_image_path, 'rb') as image_file:
                files = {
                    'image_file': image_file,  # Dosyayı doğrudan ekleyin
                }
                
                response = requests.post(url, data=data, files=files)
                
                # Yanıtı kontrol et
                if response.status_code == 200:
                    result = response.json()
                    self.update({
                        'summary': result['result']
                    })
                else:
                    print("Hata oluştu:", response.status_code, response.text) 

    def run_beatiful_score_report(self):
        ConfigModel = self.env['ir.config_parameter'].sudo()
        api_key = ConfigModel.get_param('face_plus_app.face_plus_key')
        api_secret = ConfigModel.get_param('face_plus_app.face_plus_secret')
        url = ConfigModel.get_param('face_plus_app.face_plus_url')

        data = {
            'api_key': api_key,
            'api_secret': api_secret,
        }

        attachment_id = self.env['ir.attachment'].search([('res_model', '=', 'face.plus.order'), ('res_id', '=', self.id)], limit=1)
        if attachment_id:
            local_image_path = self.download_image("https://cabinetra.com/wp-content/uploads/2024/10/pexels-reafonbgates-1498337-scaled.jpg") 
            with open(local_image_path, 'rb') as image_file:
                files = {
                    'image_file': image_file,  # Dosyayı doğrudan ekleyin
                }
                
                response = requests.post('https://api.faceplusplus.com/facepp/v3/beauty', data=data, files=files)
                
                # Yanıtı kontrol et
                if response.status_code == 200:
                    result = response.json()
                    print("Başarılı oldu:", result['result']) 
                else:
                    print("Hata oluştu:", response.status_code, response.text) 

    def run_chat_gpt_report(self):
        os.environ["OPENAI_API_KEY"] = "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"
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

        # API anahtarını ayarlayın
        openai.api_key = api_key

        content = "%s" % ("{'pores_left_cheek': {'confidence': 0.67987937, 'value': 1}, 'nasolabial_fold': {'confidence': 0.95555943, 'value': 1}, 'eye_pouch': {'confidence': 0.99999905, 'value': 0}, 'forehead_wrinkle': {'confidence': 0.0018991657, 'value': 0}, 'skin_spot': {'confidence': 0.010272887, 'value': 0}, 'acne': {'confidence': 0.08375722, 'value': 0}, 'pores_forehead': {'confidence': 0.63364816, 'value': 0}, 'pores_jaw': {'confidence': 0.9997265, 'value': 0}, 'left_eyelids': {'confidence': 0.9999547, 'value': 2}, 'eye_finelines': {'confidence': 0.03921648, 'value': 0}, 'dark_circle': {'confidence': 0.9999802, 'value': 0}, 'crows_feet': {'confidence': 0.00026611457, 'value': 0}, 'pores_right_cheek': {'confidence': 0.9593316, 'value': 0}, 'blackhead': {'confidence': 0.005912708, 'value': 0}, 'glabella_wrinkle': {'confidence': 0.28278217, 'value': 0}, 'mole': {'confidence': 0.9988098, 'value': 1}, 'skin_type': {'details': {'0': {'confidence': 0.027613295, 'value': 0}, '1': {'confidence': 0.04851514, 'value': 0}, '2': {'confidence': 0.9205354, 'value': 1}, '3': {'confidence': 0.0033361781, 'value': 0}}, 'skin_type': 2}, 'right_eyelids': {'confidence': 0.99987555, 'value': 2}} bu bilgileri fizyognomiye göre ve ilmi simaya göre analiz ederek kişinin karakteristik özelliklerini , fal yorumu şeklinde yüz özelliklerinden bahsetmeden öyküleyici bir metin gibi yazar mısın?") 

        # İstek gönderin
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # veya kullanmak istediğiniz başka bir model
            messages=[
                {"role": "user", "content": content}
            ]
        )
        
        self.update({
            'chat_gpt_result': chat_completion.choices[0].message['content']
        })