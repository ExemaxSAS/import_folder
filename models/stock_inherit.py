# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _

class StockMoveInherit(models.Model):
    _inherit = 'stock.move'

    @api.depends('picking_id','move_line_ids')#product_id')
    def get_value_dispatch(self):
        dispatch_num_imp = ''
        dispatch_num = ''
        #lot_num = ''

        for rec in self:

            #Trae el numero de despacho de la carpeta de importación
            dispatch_num_imp = rec.picking_id.task_id.dispatch

            if dispatch_num_imp != False:
                dispatch_num = dispatch_num_imp
            else:
                dispatch_num = ''
            
            # for move in rec.move_line_ids:
            #     if move.lot_name != False:
            #         lot_num = move.lot_name
            #     else:
            #         lot_num = ''

            #rec.dispatch = str(dispatch_num) + '-' + str(lot_num)
            rec.dispatch = dispatch_num
        return rec.dispatch

    dispatch = fields.Char(string='Despacho' , compute='get_value_dispatch')


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    @api.depends('purchase_id')
    def get_value_task(self):
        for rec in self:
            rec.task_id = rec.purchase_id.task_id
            return rec.task_id

    task_id = fields.Many2one('project.task', string='Carpeta de importación' , compute='get_value_task' , store=True)
    bultos = fields.Char(string='Bultos')


class StockMoveLineInherit(models.Model):
    _inherit = 'stock.move.line'

    dispatchs = fields.Char(string='Despacho', related='move_id.dispatch')


