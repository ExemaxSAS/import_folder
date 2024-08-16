# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions, _

import logging

_logger = logging.getLogger(__name__)

class StockMoveInherit(models.Model):
    _inherit = 'stock.move'

    def get_value_dispatch(self):
        for rec in self:
            if len(rec.picking_id.task_ids) == 1:
                rec.dispatch = rec.picking_id.task_ids[0].dispatch
            else:
                rec.dispatch = False

    dispatch = fields.Char(string='Transito picking', compute='get_value_dispatch')


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'


    def compute_is_purchase(self):
        for record in self:
            record.is_purchase = 'P' in (record.origin or '')

    def action_get_purchase_id(self):
        if self.group_id:
            if "P" in self.group_id.name:
                so_reference = self.env['purchase.order'].search([('id', '=', self.purchase_id.id)])
                self.task_ids = so_reference.task_id
            elif "S" in self.group_id.name:
                _logger.info('Es sale ==========================================')
                so_reference = self.env['sale.order'].search([('id', '=', self.sale_id.id)])
                _logger.info(f'sale {so_reference.tasks_ids}')
                for rec in so_reference.tasks_ids:
                    _logger.info(f"TASK ID TEST {rec}")
                self.task_ids = [(4, task.id) for task in so_reference.tasks_ids]

    def get_value_tasks(self):
        for rec in self:
            if rec.purchase_id:

                # Asignar task_id desde la relación con purchase_id
                rec.task_ids = rec.purchase_id.task_id
            else:
                if rec.group_id and rec.group_id.name:
                    # Buscar la orden de venta que corresponde al nombre del grupo
                    sale_order = self.env['sale.order'].search([('name', '=', rec.group_id.name)], limit=1)
                    if sale_order:
                        # Asignar el primer task_id de la lista de tasks_ids
                        rec.task_id = sale_order.tasks_ids[:1].id if sale_order.tasks_ids else False
                    else:
                        rec.task_id = False
                elif rec.origin:
                    # Buscar la orden de compra que corresponde al origen
                    purchase_order = self.env['purchase.order'].search([('name', '=', rec.origin)], limit=1)
                    if purchase_order:
                        _logger.info(purchase_order.task_id[0])
                        # Asignar el task_id desde la relación con la orden de compra
                        rec.task_id = purchase_order.task_id[0]
                    else:
                        rec.task_id = False
                else:
                    rec.task_id = False

    #task_id = fields.Many2one('project.task', string='Carpeta de importación', compute='get_value_task', store=True)
    task_ids = fields.Many2many('project.task', string='Carpeta de importación', compute='get_value_tasks', readonly=False, store=True)



    @api.depends('purchase_id')
    def get_value_task(self):
        for rec in self:
            rec.task_id = rec.purchase_id.task_id
            return rec.task_id

    task_id = fields.Many2one('project.task', string='Carpeta de importación', store=True)
    bultos = fields.Char(string='Bultos')
    is_purchase = fields.Boolean(string='is_purchase', compute='compute_is_purchase')


class StockMoveLineInherit(models.Model):
    _inherit = 'stock.move.line'

    dispatch = fields.Char(string='Transito', compute='_get_dispatch_from_task')

    @api.depends('picking_id.task_ids')
    def _get_dispatch_from_task(self):
        for record in self:
            if len(record.picking_id.task_ids) == 1:
                record.dispatch = record.picking_id.task_ids[0].dispatch
            else:
                record.dispatch = ''

#Gabriel, acá se guarda el nombre del campo dispatch al confirmar las cantidades detro del lot_name
class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        res = super(PurchaseOrderInherit, self).button_confirm()
        self.update_lot_name_in_stock_move_line()
        return res

    def update_lot_name_in_stock_move_line(self):
        for line in self.order_line:
            for move_line in line.move_ids.move_line_ids:
                move_line.lot_name = move_line.move_id.picking_id.task_id.dispatch








