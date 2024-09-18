# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)

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
                    # Si hay múltiples tareas, usamos la operación (4, task.id) para agregar a la lista de tareas
                    picking.task_id = [(4, task.id) for task in order.task_id]

                # Ejecutar lógica adicional, si es necesario
                picking.action_get_purchase_id()

        return res

    def action_create_invoice(self):
        # Llamar al método original para crear las facturas
        res = super(PurchaseOrderInherit, self).action_create_invoice()

        for order in self:
            # Si 'res' es un diccionario (posible acción), obtener los ids de las facturas
            if isinstance(res, dict) and res.get('res_id'):
                invoice_ids = [res['res_id']]
            else:
                # Obtener todas las facturas asociadas a la orden
                invoice_ids = self.env['account.move'].search([
                    ('purchase_id', '=', order.id),
                    ('move_type', '=', 'in_invoice')
                ]).ids

            # Filtrar las facturas para asegurarnos de que solo tratamos con las facturas recientes
            invoices = self.env['account.move'].browse(invoice_ids)

            # Asociar la tarea solo a las facturas recién creadas
            for invoice in invoices:
                if order.task_id:
                    invoice.task_id = [(4, order.task_id.id)]

        return res



