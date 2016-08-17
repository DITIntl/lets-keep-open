# Embedded file name: /opt/openerp/producao/addons-extra/bank_transaction/res_partner.py
import time
import netsvc
from tools.translate import _
from osv import osv, fields


class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _columns = {
        'payment_type_default': fields.one2many(
            'partner.payment.type.default', 'partner_id',
            'Payment Type Default'),
        'send_payment_slip': fields.boolean('Send Payment Slip by Email')
    }


class partner_payment_type_default(osv.osv):
    _name = 'partner.payment.type.default'
    _columns = {
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'payment_type': fields.many2one(
            'payment.type', 'Payment Type', required=True),
        'partner_id': fields.many2one('res.partner', 'Partner', required=True)
    }
