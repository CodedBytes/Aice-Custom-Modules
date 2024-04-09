# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Agreement Management',
    'version': '1.0.0',
    'category': 'Agreements',
    'summary': '',
    'description': 'AICE Agreement Management',
    'live_test_url': '',
    'sequence': '1',
    'website': 'https://codedbytes.vercel.app/',
    'author': 'João Victor',
    'maintainer': '',
    'license': 'LGPL-3',
    'support': '',
    'depends': ['mail','product', 'account', 'web', 'sale', 'base', 'product'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/agreements.xml',
        'data/data.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
