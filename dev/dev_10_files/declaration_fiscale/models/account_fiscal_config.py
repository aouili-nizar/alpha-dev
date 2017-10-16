# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import models, fields, api, _
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
class account_fiscal_config(models.Model):
    """ classe de configuration des taux des taxes et des comptes comptables des taxes   """
    _name ='declaration.fiscal.config'
    _rec_name ='year'
    year = fields.Integer(string='Année')
    taux_loy=fields.Float('Taux Loyer',digits_compute=dp.get_precision('Montant Paie'),help="")
    taux_hon15 = fields.Float(
        'Taux Honoraire ( 15%)', digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_hon5 = fields.Float(
        'Taux Honoraire (5 %)', digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_mar = fields.Float(
        'Taux marché', digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_col6 = fields.Float(
        'Taux Tva Collectée 6', digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_col12 = fields.Float(
        'Taux Tva Collectée 12', digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_col18 = fields.Float(
        'Taux Tva Collectée 18', digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_ded6 = fields.Float(
        'Taux Tva deductible 6', digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_ded12 = fields.Float(
        'Taux Tva deductible 12', digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_ded18 = fields.Float(
        'Taux Tva deductible 18', digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_mmo6 = fields.Float(
        'Taux Tva/Immo6', digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_mmo12 = fields.Float(
        'Taux Tva/Immo12', digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_mmo18=fields.Float('Taux Tva/Immo 18',digits_compute=dp.get_precision('Montant Paie'))    
    taux_retsrc = fields.Float('Taux TVA retenue a la source',
                               digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_tfp = fields.Float(
        'Taux TFP', digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_fps=fields.Float('Taux FOPROLOS',digits_compute=dp.get_precision('Montant Paie'))
    tcl_loc = fields.Float('Taux TCL ( vente locale)',
                           digits_compute=dp.get_precision('Montant Paie'), help="")
    taux_exr = fields.Float('Taux TCL (vente export)',
                            digits_compute=dp.get_precision('Montant Paie'), help="")
    ret_sal = fields.Many2one(
        'account.account', string='IRPP (retenue a la sourcesur salaire)', help="")
    ret_source_loy = fields.Many2one(
        'account.account', string='Loyer (retenue a la source 15%)', help="")
    ret_source_hon = fields.Many2one(
        'account.account', string='Honoraire(retenue a la source 15%)', help="")
    ret_source_hon_5 = fields.Many2one(
        'account.account', string='Honoraire (retenue a la source5%)', help="")
    market = fields.Many2one(
        'account.account', string='Marché (retenue a la source 1,5%)', help="")
    tfp=fields.Many2one('account.account',string='Report TFP', help="")
    tva_col_6 = fields.Many2one(
        'account.account', string='TVA collectée 6%', help="")
    tva_col_12 = fields.Many2one(
        'account.account', string='TVA collectée  12%', help="")
    tva_col_18 = fields.Many2one(
        'account.account', string='TVA collectée 18%', help="")
    tva_ded_6 = fields.Many2one(
        'account.account', string='TVA déductible 6%', help="")
    tva_ded_12 = fields.Many2one(
        'account.account', string='TVA déductible 12%', help="")
    tva_ded_18 = fields.Many2one(
        'account.account', string='TVA déductible 18%', help="")
    tva_mmo_6 = fields.Many2one(
        'account.account', string='TVA IMMO 6%', help="")
    tva_mmo_12 = fields.Many2one(
        'account.account', string='TVA IMMO 12%', help="")
    tva_mmo_18 = fields.Many2one(
        'account.account', string='TVA IMMO 18%', help="")
    tva_ret_src = fields.Many2one(
        'account.account', string='TVA Retenue à la source', help="")
    report_tva = fields.Many2one(
        'account.account', string='Report TVA du mois dernier', help="")
    cpt_fact = fields.Many2one(
        'account.account', string='Droit du timbre', help="")
    taux_dr_fisc = fields.Float(
        'Taux Droit de timbre', digits_compute=dp.get_precision('Montant Paie'), help="")
