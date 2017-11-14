# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import models, fields, api, _

class deliv(models.Model):
    	_inherit="hr.employee"

	deliv = fields.Date('Date delivrance Cin')

#-------------------------------------------------------------------------------
# signataire
#-------------------------------------------------------------------------------


class boss(models.Model):
    _inherit = "res.company"

    signataire = fields.Many2one('hr.employee', string="Signataire")
    fctsign = fields.Char('Fonction de signataire')

    @api.one
    @api.onchange('signataire')
    def init_fct(self):
        if self.signataire:
            self.fctsign = self.signataire.job_id.name
#-------------------------------------------------------------------------------
# les stagiaires
#-------------------------------------------------------------------------------


class stagiaires(models.Model):
    _name = "hr.stagiaires"
    _description = "liste des stagiaires"
    _rec_name = "nom"
    image = fields.Binary('Image')
    nom = fields.Char("Nom du stagiaire")
    adresse_pro = fields.Char("Adresse Professionelle")
    tel_pro = fields.Char('Tél. portable professionel')
    user_id = fields.Many2one('res.users', string="Utilisateur lié")
    departement = fields.Many2one('hr.department', string="Département")
    job = fields.Many2one('hr.job', string="Titre de poste")
    responsa = fields.Many2one('hr.employee', string="Responsable")
    date_entre = fields.Date('Date debut')
    date_fin = fields.Date('Date fin de stage')
    nationalite = fields.Many2one('res.country', string="Nationalité")
    cin = fields.Integer('CIN')
    deliv = fields.Date('Date delivrance CIN')
    naiss = fields.Date('Date naissance')
    naisslieux = fields.Many2one(
        'res.country.state', string="Lieux de naissance")
    pers_addr = fields.Char('Adresse personnelle')
    gender = fields.Selection(
        selection=[('Masculin', 'Masculin'), ('Feminin', 'Feminin')], string="Genre")
    etciv = fields.Selection(selection=[('Divorcé', 'Divorcé'), ('Marié', 'Marié'), (
        'Celibataire', 'Celibataire'), ('Voeuf', 'Voeuf')], string="etat Civil")
    actif = fields.Boolean('Active')
    theme = fields.Char('Théme de stage')


#-------------------------------------------------------------------------------
# ajout champ brut a hr_contract
#-------------------------------------------------------------------------------
class contract_inh(models.Model):
     _inherit = 'hr.contract'

     salaire_b = fields.Float('Salaire Brut', digits=(10, 3), required=True)
