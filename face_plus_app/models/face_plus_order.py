
import requests
import openai
import json
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
        ], default="character"
    )
    chat_gpt_result = fields.Text(string='Gpt Result')

    @api.model
    def create(self, vals):
        templates = super(FacePlusOrder,self).create(vals)
        seq = self.env['ir.sequence'].get('face.plus.order')
        templates.name = seq
        return templates

    def run_face_plus_report(self):
        ConfigModel = self.env['ir.config_parameter'].sudo()
        api_key = ConfigModel.get_param('face_plus_app.face_plus_key')
        api_secret = ConfigModel.get_param('face_plus_app.face_plus_secret')
        base_url = ConfigModel.get_param('face_plus_app.face_plus_url') # 

        attachment_id = self.env['ir.attachment'].search([('res_model', '=', 'face.plus.order'), ('res_id', '=', self.id)], limit=1)
        if attachment_id:
            
            base_data = {
                'api_key': api_key,
                'api_secret': api_secret,
                'image_base64': attachment_id.datas.decode('utf-8'),
            }
            
            endpoints = {
                'character': [
                    {
                        'url': f"{base_url}/facepp/v1/skinanalyze",
                        'fields': [],
                        'result': 'faces',
                        'return_attributes': 'age,gender,emotion'
                    }
                ],
                'skin': [
                    {
                        'url': f"{base_url}/facepp/v1/skinanalyze",
                        'fields': [],
                        'result': 'result',
                        'return_attributes': ''
                    }
                ],
                'mood': [
                    {
                        'url': f"{base_url}/facepp/v3/detect",
                        'fields': [],
                        'result': 'faces',
                        'return_attributes': 'age,gender,emotion'
                    }
                ],
                'dream': [
                    {
                        'url': f"{base_url}/facepp/v1/face/thousandlandmark",
                        'fields': [
                            { 
                                'return_landmark': 'face' 
                            }
                        ],
                        'result': 'face',
                        'return_attributes': ''
                    }
                ],
            }

            selected_endpoints = endpoints.get(self.type, [])
            if not selected_endpoints:
                print(f"Uyarı: {self.type} için bir endpoint tanımlı değil.")
                return
            
            results = []
            for endpoint in selected_endpoints:
                try:
                    request_data = base_data.copy()
                    for field in endpoint.get('fields', []):
                        request_data.update(field)
                    
                    if endpoint.get('return_attributes', False):
                        request_data['return_attributes'] = endpoint['return_attributes']

                    response = requests.post(endpoint["url"], data=request_data)
                    if response.status_code == 200:
                        result = response.json()
                        results = result[endpoint["result"]]
                    else:
                        print(f"Hata: {endpoint['url']} isteği başarısız. Kod: {response.status_code}")
                except Exception as e:
                    print(f"Hata oluştu: {str(e)}")

            self.update({
                'summary': results
            })

    def run_chat_gpt_report(self):
        ConfigModel = self.env['ir.config_parameter'].sudo()

        # API anahtarını al
        openai_key = ConfigModel.get_param('face_plus_app.openai_key')
        if not openai_key:
            raise ValueError("API anahtarı bulunamadı. Lütfen 'face_plus_app.openai_key' ayarını kontrol edin.")

        openai.api_key = openai_key

        props = ConfigModel.get_param('face_plus_app.openai_props_karakter')
        if self.type == 'skin': 
            props = ConfigModel.get_param('face_plus_app.openai_props_skin')
        elif self.type == 'mood': 
            props = ConfigModel.get_param('face_plus_app.openai_props_mood')
        elif self.type == 'dream': 
            props = ConfigModel.get_param('face_plus_app.openai_props_dream')
        elif self.type == 'style': 
            props = ConfigModel.get_param('face_plus_app.openai_props_style')
        elif self.type == 'wish': 
            props = ConfigModel.get_param('face_plus_app.openai_props_wish')
        elif self.type == 'nutrition': 
            props = ConfigModel.get_param('face_plus_app.openai_props_nutrition')
        elif self.type == 'personal': 
            props = ConfigModel.get_param('face_plus_app.openai_props_personal')
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