# -*- coding: utf-8 -*-
{
    'name': "Face Plus App",
    'summary': """Face Plus App""",
    'description': """Face Plus App""",
    'author': "Serkan",
    'website': "",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #VIEWS
        'views/face_plus_order_views.xml',
        'views/res_config_settings_views.xml',
        'views/res_users_views.xml',
    ],
}
