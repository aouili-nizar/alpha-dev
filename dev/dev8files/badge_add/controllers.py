# -*- coding: utf-8 -*-
from openerp import http

# class BadgeAdd(http.Controller):
#     @http.route('/badge_add/badge_add/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/badge_add/badge_add/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('badge_add.listing', {
#             'root': '/badge_add/badge_add',
#             'objects': http.request.env['badge_add.badge_add'].search([]),
#         })

#     @http.route('/badge_add/badge_add/objects/<model("badge_add.badge_add"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('badge_add.object', {
#             'object': obj
#         })