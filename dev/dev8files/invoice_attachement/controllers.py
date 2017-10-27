# -*- coding: utf-8 -*-
from openerp import http

# class InvoiceAttachement(http.Controller):
#     @http.route('/invoice_attachement/invoice_attachement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_attachement/invoice_attachement/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_attachement.listing', {
#             'root': '/invoice_attachement/invoice_attachement',
#             'objects': http.request.env['invoice_attachement.invoice_attachement'].search([]),
#         })

#     @http.route('/invoice_attachement/invoice_attachement/objects/<model("invoice_attachement.invoice_attachement"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_attachement.object', {
#             'object': obj
#         })