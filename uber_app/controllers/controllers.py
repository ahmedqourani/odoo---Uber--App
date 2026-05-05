# -*- coding: utf-8 -*-
# from odoo import http


# class UberApp(http.Controller):
#     @http.route('/uber_app/uber_app', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/uber_app/uber_app/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('uber_app.listing', {
#             'root': '/uber_app/uber_app',
#             'objects': http.request.env['uber_app.uber_app'].search([]),
#         })

#     @http.route('/uber_app/uber_app/objects/<model("uber_app.uber_app"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('uber_app.object', {
#             'object': obj
#         })

