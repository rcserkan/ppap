# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: PayTR iFrame',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': "A Türkiye payment provider.",
    "author": "Kıta Yazılım",
    "website": "https://kitayazilim.com",
    'depends': ['payment', 'account_payment', 'sale'],
    'data': [
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
    ],
    'application': False,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'assets': {
        'web.assets_frontend': [
            'payment_paytr_kt/static/src/js/payment_form.js',
        ],
    },
    'license': 'LGPL-3',
}
