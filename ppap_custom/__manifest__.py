# -*- coding: utf-8 -*-
{
    'name': "PPAP Custom",

    'summary': """PPAP Custom""",

    'description': """PPAP Custom""",

    'author': "Serkan",
    'website': "",

    'category': 'Tools',
    'version': '0.1',

    'depends': ['base', 'sale', 'purchase'],

    # always loaded
    'data': [
        'security/ppap_security.xml',
        'security/ir.model.access.csv',
        
        #VIEWS
        'views/offer_views.xml',
        'views/vendor_product_views.xml',
        'views/sales_order_views.xml',
        
        #REPORTS
        # 'views/reports/.xml',
        
        #MAILS
        # 'views/mails/.xml',
    ],
}
