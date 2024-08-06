from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError
import base64
import json
import pandas as pd

class IrAttachment(models.Model):
    _inherit = "ir.attachment"


    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res.order_attachment_to_json_converter()
        return res
    
    def order_attachment_to_json_converter(self):
        if self.res_model == 'email.order':
            email_order_id = self.env[self.res_model].search([('id', '=', self.res_id)])
            if email_order_id:
                # Base64 veriyi çöz
                file_content = base64.b64decode(self.datas)

                # Excel verisini oku
                excel_data = pd.read_excel(file_content, engine='openpyxl')

                # Verileri temizle
                excel_data.columns = [col.strip() for col in excel_data.columns]  # Kolon adlarını temizle
                excel_data = excel_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)  # Hücre verilerini temizle

                # JSON formatına dönüştür
                json_data = excel_data.to_json(orient='records', force_ascii=False)

                # JSON verilerini Python dict formatın
                json_records = json.loads(json_data)
                email_order_id.update({
                    'file_name': self.description,
                    'order_date': self.create_date,
                    'order_json': json.dumps(json_records, ensure_ascii=False)
                })
