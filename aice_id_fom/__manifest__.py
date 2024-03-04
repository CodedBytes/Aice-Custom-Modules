# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Aice Indonesia Freezer Order Management',
    'version': '1.0.0',
    'category': 'Freezer Asset Management',
    'summary': '',
    'description': 'Custom Module for Freezer Order Management Aice Indonesia',
    'live_test_url': '',
    'sequence': '1',
    'website': 'https://wwww.example.com',
    'author': 'William Sanjaya',
    'maintainer': '',
    'license': 'LGPL-3',
    'support': '',
    'depends': ['mail','product', 'account', 'report_xlsx', 'web', 'sale', 'base', 'product'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        #'views/views.xml',
        'views/orders.xml',
        'views/products.xml',
        'views/resourceTypeView.xml',
        'views/qtyTypeView.xml',
        'views/orderTypeView.xml',
        'views/resourceView.xml',
        'views/storeType.xml',
        'views/terminalMgmt.xml',
        'views/salesDepartmentView.xml',
        'views/takebackReason.xml',
        'data/data.xml',
        'report/fom_report_template.xml',
        'report/report.xml'
    ],
    'qweb': ['static/src/xml/dropdown_filter.xml'],
    'js': ['static/src/js/dropdown_filter.js'],
    'installable': True,
    'auto_install': False,
}
