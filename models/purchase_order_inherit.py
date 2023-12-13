# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _

class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    task_id = fields.Many2one('project.task', string='Carpeta de importación')

    #partner_id = fields.Many2one('res.partner', string='Proveedor', related='task_id.supplier', store=True)
