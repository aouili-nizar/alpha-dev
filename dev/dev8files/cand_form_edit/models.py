# -*- coding: utf-8 -*-

from openerp import models, fields, api

class cand_form_edit(models.Model):
    _inherit="hr.applicant"

    adress = fields.Char("Adresse de l'entretien")

    gmap = fields.Char('Emplacement Géographique')