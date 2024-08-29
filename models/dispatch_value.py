# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime

class DispatchInfo(models.Model):
    _name = 'dispatch.info'
    _description = 'Dispatch Information'

    name = fields.Char(string='Dispatch Number')
    move_line_id = fields.Many2one('stock.move.line', string='Move Line')


class StockMoveLineInheritDispatch(models.Model):
    _inherit = 'stock.move.line'
    sale_order_line_id = fields.Many2one('sale.order.line', string='Sale Order Line', compute='_get_sale_order_line', store=True)

    @api.depends('move_id', 'product_id')
    def _get_sale_order_line(self):
        for move_line in self:
            sale_order_line = self.env['sale.order.line'].search([
                ('product_id', '=', move_line.product_id.id),
            ], limit=1)

            move_line.sale_order_line_id = sale_order_line


    @api.onchange("product_id")
    def _onchange_product_id_set_lot_domain(self):
        available_lot_ids = []
        if self.product_id:
            quants = self.env["stock.quant"].read_group(
                [
                    ("product_id", "=", self.product_id.id),
                    ("location_id", "child_of", self.location_id.id),
                    ("quantity", ">", 0),
                    ("lot_id", "!=", False),
                ],
                ["lot_id"],
                "lot_id",
            )

            available_lot_ids = [quant["lot_id"][0] for quant in quants]
            self.lot_id = False
            return {"domain": {"lot_id": [("id", "in", available_lot_ids)]}}

    dispatch_from_lot = fields.Char(string='Transito de Ventas', compute='_compute_dispatch_from_lot')
    #para que sea Transito, este difiere del de las task.

    # anular de la parte de ventas, que traiga el lote por defecto y replique el de "transito"
    def _compute_dispatch_from_lot(self):
        for picking in self:
            move_line = self.env['stock.move.line'].search([('lot_id', '=', picking.lot_id.id)], limit=1)
            if move_line:
                picking.dispatch_from_lot = move_line.dispatchs
            else:
                picking.dispatch_from_lot = False


'''# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

# Configuración del logger
_logger = logging.getLogger(__name__)

class DispatchInfo(models.Model):
    _name = 'dispatch.info'
    _description = 'Información de Despacho'

    name = fields.Char(string='Número de Despacho')
    move_line_id = fields.Many2one('stock.move.line', string='Línea de Movimiento')

class StockMoveLineInheritDispatch(models.Model):
    _inherit = 'stock.move.line'

    sale_order_line_id = fields.Many2one('sale.order.line', string='Línea de Pedido de Venta', compute='_get_sale_order_line', store=True)

    @api.depends('move_id', 'product_id')
    def _get_sale_order_line(self):
        for move_line in self:
            _logger.info("Calculando línea de pedido de venta para la línea de movimiento ID: %s", move_line.id)
            sale_order_line = self.env['sale.order.line'].search([
                ('product_id', '=', move_line.product_id.id),
            ], limit=1)
            move_line.sale_order_line_id = sale_order_line
            _logger.info("Se ha establecido sale_order_line_id a %s para la línea de movimiento ID: %s", sale_order_line.id, move_line.id)

    @api.onchange("product_id")
    def _onchange_product_id_set_lot_domain(self):
        available_lot_ids = []
        if self.product_id:
            _logger.info("ID del Producto: %s", self.product_id.id)
            quants = self.env["stock.quant"].read_group(
                [
                    ("product_id", "=", self.product_id.id),
                    ("location_id", "child_of", self.location_id.id),
                    ("quantity", ">", 0),
                    ("lot_id", "!=", False),
                ],
                ["lot_id"],
                "lot_id",
            )
            available_lot_ids = [quant["lot_id"][0] for quant in quants]
            _logger.info("IDs de lotes disponibles: %s", available_lot_ids)
            self.lot_id = False
            return {"domain": {"lot_id": [("id", "in", available_lot_ids)]}}

    dispatch_from_lot = fields.Char(string="Número de despacho", readonly=False, compute='_compute_dispatch_from_lot')

    @api.depends('lot_id')
    def _compute_dispatch_from_lot(self):
        for move_line in self:
            move_line.dispatch_from_lot = False
            if move_line.lot_id:
                related_proyect_task = self.env['project.task'].search([('name', '=', move_line.lot_id.name)])
                if related_proyect_task:
                    move_line.dispatch_from_lot = related_proyect_task.dispatch
                else:
                    move_line.dispatch_from_lot = False
            else:
                move_line.dispatch_from_lot = False'''
