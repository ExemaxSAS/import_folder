# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _

class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    task_id = fields.Many2many('project.task', string='Número de tránsito')

    def button_confirm(self):
        res = super(PurchaseOrderInherit, self).button_confirm()

        # Lógica para asociar tareas a los pickings generados
        for order in self:
            # Buscar todos los pickings asociados a esta orden de compra
            pickings = self.env['stock.picking'].search([('origin', '=', order.name)])

            # Asociar la tarea a los pickings
            for picking in pickings:
                if order.task_id:
                    picking.task_ids = [(4, order.task_id.id)]
                picking.action_get_purchase_id()

        return res

    def action_create_invoice(self):
        # Llamar al método original para crear las facturas
        res = super(PurchaseOrderInherit, self).action_create_invoice()

        # Buscar facturas generadas para cada pedido de compra
        for order in self:
            # Buscar todas las facturas de compra asociadas al pedido
            invoices = self.env['account.move'].search([
                ('purchase_id', '=', order.id),
                ('move_type', '=', 'in_invoice')
            ])

            # Asociar las tareas a las facturas
            for invoice in invoices:
                if order.task_id:
                    invoice.task_id = [(4, task.id) for task in order.task_id]

        return res
