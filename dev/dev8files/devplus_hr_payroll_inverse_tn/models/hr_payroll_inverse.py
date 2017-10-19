# -*- coding: utf-8 -*-
import time
from odoo.osv import fields, osv
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp

class hr_payroll_inverse(osv.osv):
    _name = 'hr.payroll_inverse'
    _description='payroll.inverse'

    def calculer(self, cr, uid, ids,field_names,arg,context=None):
        vals={}
        print '****dic**',vals
        for rs in self.browse(cr,uid,ids,context=context):
            basic = 0.0
            sf = 0.0
            neta = 0.0
            irpp = 0.0
            imp = 0.0
            charge = 0.0
            chargem = 0.0
            primea = 0.0
            prime = 0.0
            salprime = 0.0
            charget = 0.0
            charge_ticket = 0.0
            mois_t = 12
            impot = 0.0
            cnss = 0.0
            if rs.type == 'chef' and rs.enfant == '0' :
                sf += 150
            if rs.type == 'chef' and rs.enfant == '1':
                sf += 240
            elif rs.type == 'chef' and rs.enfant == '2':
                sf += 315
            elif rs.type == 'chef' and rs.enfant == '3':
                sf += 375
            elif rs.type == 'chef' and rs.enfant == '4':
                sf += 420
            elif rs.type == 'celibataire':
                sf = 0.0

            mois_t = rs.mois
            neta += rs.net * mois_t

            if ((neta/0.7)*0.817) > 50000:
                imp += (neta + 13025 - (50000 + sf) * 0.35 ) / 0.685
            elif ((neta/0.75)*0.817)>20000 and ((neta/0.7)*0.817)< 50000:
                imp += ( ( neta - (20000 + sf) *0.3) + 4025) / 0.73
            elif ((neta/0.8)*0.817)>10000 and ((neta/0.75)*0.817)< 20000:
                imp =( (neta - (10000 + sf) * 0.25) + 1525) / 0.775
            elif ((neta/0.85)*0.817)>5000 and ((neta/0.8)*0.817)< 10000:
                imp = ( (neta - (5000 + sf) * 0.20) + 525) / 0.82
            elif ((neta/0.85)*0.817)>1500 and ((neta/0.85)*0.817)< 5000:
                imp = (neta - (1500 + sf) * 0.15) / 0.865
            else:
                imp = neta

            impot += neta + (rs.prime_net * mois_t)

            if ((impot/0.7)*0.817) > 50000:
                salprime = (( impot -(50000 + sf) * 0.35 )+ 13025) / 0.685
            elif ((impot/0.75)*0.817) >20000 and ((impot/0.7)*0.817)< 50000:
                salprime = ( ( impot - (20000 + sf) *0.3) + 4025) / 0.73
            elif ((impot/0.8)*0.817)>10000 and ((impot/0.75)*0.817)< 20000:
                salprime =( (impot - (10000 + sf) * 0.25) + 1525) / 0.775
            elif ((impot/0.85)*0.817)>5000 and ((impot/0.8)*0.817)< 10000:
                salprime = ( (impot - (5000 + sf) * 0.20) + 525) / 0.82
            elif ((impot/0.85)*0.817)>1500 and ((impot/0.85)*0.817)< 5000:
                salprime = (impot - (1500 + sf) * 0.15) / 0.865
            else:
                salprime = impot

            primea += salprime - imp

            charge += impot + (rs.ticket * mois_t )


            if ((charge/0.7)*0.817) > 50000:
                chargem = ( (charge - (50000 + sf) * 0.35) + 13025) / 0.685
            elif ((charge/0.75)*0.817) >20000 and ((charge/0.7)*0.817)< 50000:
                chargem = ( ( charge - (20000 + sf) *0.3) + 4025) / 0.73
            elif  ((charge/0.8)*0.817)>10000 and ((charge/0.75)*0.817)< 20000:
                chargem = ( (charge - (10000 + sf) * 0.25) + 1525) / 0.775
            elif ((charge/0.85)*0.817)>5000 and ((charge/0.8)*0.817)< 10000:
                chargem = ( (charge - (5000 + sf) * 0.20) + 525) / 0.82
            elif ((charge/0.85)*0.817)>1500 and ((charge/0.85)*0.817)< 5000:
                chargem = (charge - (1500 + sf) * 0.15) / 0.865
            else:
                chargem = charge

            charget += chargem - salprime

            if rs.cnss == 0:
                basic += imp / mois_t
                prime = primea / mois_t
            else:
                cnss += (100-rs.cnss)/100
                basic += (imp/cnss) / mois_t
                prime = (primea/cnss) / mois_t

                charge_ticket = charget / mois_t

            record = {
                    'basic':basic,
                    'prime_base':prime,

                    'charge_ticket':charge_ticket,
                    }
            vals[rs.id] = record
        return vals

    def action_terminer(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids[0],{'state': 'done'},context)
        return True

    def button_dummy(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {}, context=context)

    _columns = {
                'net':fields.float('Salaire Net', required=True),
                'mois':fields.float('Mois de travails'),
                'cnss':fields.float('Taux CNSS'),
                #'basic':fields.float('Salaire de base'),
                'basic': fields.function(calculer, method=True, type='float', store=True, multi='dc', string='Salaire de base', digits=(16, 3)),
                'enfant':fields.selection([
                    ('0','0'),
                    ('1','1'),
                    ('2','2'),
                    ('3','3'),
                    ('3','4'),
                ],'Enfant', select=True, required=True),
                'type':fields.selection([
                    ('celibataire','Celibataire'),
                    ('chef','Chef de famille'),
                ],'Type', select=True, required=True),
                'state':fields.selection([('new','Brouillon'), ('done','Validé'),], 'Etat'),
                #'prime_base':fields.float('Prime de base'),
                'ticket':fields.float('Ticket restaurant'),
                'prime_net':fields.float('Prime Net'),
                #'charge_ticket':fields.float('Charge ticket restaurant'),
                'charge_ticket': fields.function(calculer, method=True, type='float',store=True, multi='dc', string='Charge ticket restaurant', digits=(16, 3)),
                'prime_base': fields.function(calculer, method=True, type='float',multi='dc', string='Prime de mission', digits=(16, 3)),

                }



    _defaults = {
        'enfant': lambda *a: 0,
        'ticket': lambda *a: 0,
        'mois': 12,
        'cnss': 9.18,
        'state': 'new',
    }
hr_payroll_inverse()
