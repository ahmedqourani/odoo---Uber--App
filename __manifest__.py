# -*- coding: utf-8 -*-
{
    'name': "Uber_app",
    'version': '1.0',

    'summary': 'Uber Ride Management System',

    'description': """
Uber Application built with Odoo.

Features:
- Manage Passengers
- Manage Drivers
- Manage Rides
- Automatic Fare Calculation
- Payment Management

GitHub Project:
https://github.com/ahmedqourani/odoo---Uber--App
    """,

    'author': 'Ahmed Qourani',
    'website': 'https://github.com/ahmedqourani/odoo---Uber--App',

    'category': 'Services',
    'license': 'LGPL-3',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/uber.passenger.csv',
        'views/views.xml',
    ],

    'application': True,

    'icon': '/uber_app/static/description/icon.png',
}