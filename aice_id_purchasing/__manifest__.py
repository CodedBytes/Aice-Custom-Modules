# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Aice Indonesia Purchasing Customization',
    'version': '1.0.0',
    'category': 'Purchasing',
    'summary': '',
    'description': 'Custom Module for Purchasing Management Aice Indonesia',
    'live_test_url': '',
    'sequence': '1',
    'website': 'https://wwww.example.com',
    'author': 'William Sanjaya',
    'maintainer': '',
    'license': 'LGPL-3',
    'support': '',
    'depends': ['purchase','mail', 'account', 'report_xlsx', 'web', 'sale', 'base', 'product'],
    'demo': [],
    'data': [
        #'security/ir.model.access.csv',
        #'views/templates.xml',
        'views/views.xml',
        #'views/orders.xml',
        #'views/products.xml',
        #'views/resourceTypeView.xml',
        #'views/resourceView.xml',
        #'views/storeType.xml',
        #'views/terminalMgmt.xml',
        #'views/takebackReason.xml',
        #'data/data.xml',
        #'report/report.xml',
        #'report/fom_report_template.xml'],
    ],
    'qweb': ['static/src/xml/dropdown_filter.xml'],
    'js': ['static/src/js/dropdown_filter.js'],
    'installable': True,
    'auto_install': False,
}
