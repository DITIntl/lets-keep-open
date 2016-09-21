# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import base64
import zipfile
import os.path
from openerp.osv import fields, osv
from datetime import datetime
import openerp.netsvc as netsvc


class report_commission_wizard(osv.osv_memory):
    _name = 'report.commission.wizard'
    _description = u'Wizard de Relatório de comissão'

    _columns = {
        'start_date': fields.date('Data de Inicio', required=True),
        'end_date': fields.date('Data Final', required=True),
        'result': fields.binary('Resultado', readonly=True)
    }

    _defaults = {
        'start_date': lambda s, c, u, ctx: datetime.now().replace(day=1).
        strftime('%Y-%m-%d'),
        'end_date': lambda s, c, u, ctx: datetime.now().strftime('%Y-%m-%d'),
    }

    def action_generate_report(self, cr, uid, ids, context=None):
        items = self.browse(cr, uid, ids, context=context)
        cr.execute('select distinct(partner_id) as partner_id from account_analytic_partner_commission where partner_id is not null limit 1')
        partners = cr.fetchall()
        ids = [x[0] for x in partners]
        print ids
        datas = {
             'model': 'res.partner',
             'start_date': items[0].start_date,
             'end_date': items[0].end_date,
        }

        obj = netsvc.LocalService('report.commission.report')
        caminho = '/home/danimar/Documentos/PDF'
        for partner in ids:
            (result, format) = obj.create(cr, uid, [partner], datas, context)
            path = os.path.join(caminho, 'Relatorio-%d.pdf' % partner)
            f = open(path, 'wb')
            f.write(result)
            f.close()

        def zipdir(path, ziph):
            # ziph is zipfile handle
            for root, dirs, files in os.walk(path):
                for file in files:
                    ziph.write(os.path.join(root, file))

        zipf = zipfile.ZipFile('/home/danimar/Documentos/pdf.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir('/home/danimar/Documentos/PDF/', zipf)
        zipf.close()

        zip_file = open('/home/danimar/Documentos/pdf.zip', 'rb').read()

        id_wizard = self.create(cr, uid, {'start_date': items[0].start_date,
                              'end_date': items[0].end_date,
                              'result': base64.b64encode(zip_file)}, context)

        return {
            'type': 'ir.actions.act_window',
            'name': u'Relatório de Comissões',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_id': id_wizard,
            'res_model': 'report.commission.wizard',
            'nodestroy': True,
        }


report_commission_wizard()
