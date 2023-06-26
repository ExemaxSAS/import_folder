# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _
import logging
_logger= logging.getLogger(__name__)

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    task_id = fields.Many2many('project.task', string='Carpeta de importación')