# -*- coding: utf-8 -*-
{
    'name': "Mail Attachment Processor",

    'summary': """Mail Attachment Processor""",

    'description': """Mail Attachment Processor""",

    'author': "Serkan",
    'website': "",

    'category': 'Tools',
    'version': '0.1',

    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        
        #VIEWS
        'views/email_order.xml',
    ],
    'assets': {
        'web.assets_backend': [
        ],
    },
}
