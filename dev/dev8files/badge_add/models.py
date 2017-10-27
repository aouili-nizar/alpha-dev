# -*- coding: utf-8 -*-

from openerp import models, fields, api

# class badge_add(models.Model):
#     _name = 'badge_add.badge_add'

#     name = fields.Char()

class inh_emp(models.Model):
    _inherit="hr.employee"

    badge_id = fields.Integer(string='Badge ID',help="l'id de badge du pointeuse")