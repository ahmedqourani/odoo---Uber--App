# -*- coding: utf-8 -*-
{
    'name': "Uber_app",
    'version': '1.0',
    'depends': ['base'],

    'data': [
        # Security
        'security/ir.model.access.csv',

        # Data (CSV + XML)
        'data/demo.xml',
        'data/uber.passenger.csv',

        # Views
        'views/views.xml',
    ],

    'application': True,
    'images': ['static/description/icon.png'],
}