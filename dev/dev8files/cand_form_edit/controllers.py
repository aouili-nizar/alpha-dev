# -*- coding: utf-8 -*-
from openerp import http

# class CandFormEdit(http.Controller):
#     @http.route('/cand_form_edit/cand_form_edit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cand_form_edit/cand_form_edit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cand_form_edit.listing', {
#             'root': '/cand_form_edit/cand_form_edit',
#             'objects': http.request.env['cand_form_edit.cand_form_edit'].search([]),
#         })

#     @http.route('/cand_form_edit/cand_form_edit/objects/<model("cand_form_edit.cand_form_edit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cand_form_edit.object', {
#             'object': obj
#         })