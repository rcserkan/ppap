{
    "name": "ICA Money Changer",
    "depends": ["base", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/ica_money_changer.xml",
        "views/menus.xml",
        "views/templates.xml",
    ],
    'assets': {
        'ica_money_changer.assets_standalone_app': [
            ('include', 'web._assets_helpers'),
            'web/static/src/scss/pre_variables.scss',
            'web/static/lib/bootstrap/scss/_variables.scss',
            ('include', 'web._assets_bootstrap'),
            ('include', 'web._assets_core'),
            'ica_money_changer/static/src/**/*',
            'ica_money_changer/static/assets/css/app.min.css',
            'ica_money_changer/static/assets/css/style.css',
            'ica_money_changer/static/assets/css/form.min.css',
            'ica_money_changer/static/assets/css/styles/all-themes.css',
            'ica_money_changer/static/assets/js/app.min.js',
            'ica_money_changer/static/assets/js/admin.js',
            'ica_money_changer/static/assets/js/table.min.js',
            'ica_money_changer/static/assets/js/pages/tables/jquery-datatable.js',
        ],
    },
    "license": "LGPL-3"
}
