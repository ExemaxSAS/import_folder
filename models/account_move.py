# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _
import logging
_logger= logging.getLogger(__name__)

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    task_id = fields.Many2many('project.task', string='Carpeta de importación', readonly=False)

class AccountMoveInherit(models.Model):
    _inherit = 'account.move.line'

    sale_id = fields.Many2one('sale.order', string='Sale Order', compute='_compute_sale_id')

    def _compute_sale_id(self):
        for rec in self:
            if rec.sale_line_ids:
                rec.sale_id = rec.sale_line_ids.order_id.id
            else:
                rec.sale_id = False


