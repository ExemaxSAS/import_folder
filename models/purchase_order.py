# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _

class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    task_id = fields.Many2many('project.task', string='Número de tránsito')
