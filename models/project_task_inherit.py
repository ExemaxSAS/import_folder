# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError
import logging
_logger= logging.getLogger(__name__)

class ProjectTaskInherit(models.Model):
    _inherit = 'project.task'

    purchase_order_ids = fields.One2many('purchase.order','task_id', string='Pedidos de compras')
    stock_picking_ids = fields.One2many('stock.picking','task_id', string='Remitos')  
    invoice_ids = fields.One2many('account.move','task_id', string='Facturas proveedor')
    purchase_count = fields.Integer(compute='_compute_task_data_purchase', string="Pedidos de compras")
    invoice_count = fields.Integer(store=True,readonly=False)   
    stock_count = fields.Integer(compute='_compute_task_data_stock', string="Remitos")
    importation_task = fields.Boolean(compute='get_value_project')
   
    supplier = fields.Many2one('res.partner', string='Proveedor') # ok
    instructor_id = fields.Many2one('res.partner', string='Agente de carga') # ok
    dispatch = fields.Char(string='Despacho') # ok
    import_license = fields.Char(string='Licencia de importación') # ok
    divisa = fields.Many2one('res.currency', string='Divisa',domain="[('active', '=', True)]") # ok  
    ncm = fields.Char(string='NCM') # ok
    shipping = fields.Selection([('mar','Marítimo'),('air','Aéreo'),('ground','Terrestre'),],string='Embarque')# ok
    incoterm = fields.Char(string='INCOTERM') # ok            
    etd = fields.Date(string='ETD') # ok
    eta = fields.Date(string='ETA') # ok
    closing_date = fields.Date(string='Fecha de cierre de importación') # ok

    @api.depends('purchase_order_ids.task_id')
    def _compute_task_data_purchase(self):
        for rec in self:
            purchase_cnt = 0
            for task_purchase in rec.purchase_order_ids:
                purchase_cnt += 1
            rec.purchase_count = purchase_cnt

            #queda acá el contador de invoices porque que al ser many2many la relacion en el modelo account_move no entra en su compute
            count_invoices= self.env['account.move'].search_count([('task_id','in',rec.id),('state','=','posted')])
            rec.invoice_count= count_invoices

    @api.depends('stock_picking_ids.task_id')
    def _compute_task_data_stock(self):
        for rec in self:
            stock_cnt = 0
            for task_stock in rec.stock_picking_ids:
                stock_cnt += 1
            rec.stock_count = stock_cnt

    @api.depends('project_id')
    def get_value_project(self):
        for rec in self:
            rec.importation_task = rec.project_id.importation
            return rec.importation_task

    def action_view_project_stock(self):
        action = self.env["ir.actions.act_window"]._for_xml_id("import_folder.stock_picking_action_list_view")
        action['domain'] = [('task_id', '=', self.id)]
        return action

    def action_view_project_account(self):
        action = self.env["ir.actions.act_window"]._for_xml_id("import_folder.account_move_action_list_view")
        action['domain'] = [('task_id', '=', self.id)]
        return action

    def action_view_project_purchase(self):
        action = self.env["ir.actions.act_window"]._for_xml_id("import_folder.purchase_order_action_list_view")
        action['domain'] = [('task_id', '=', self.id)]
        return action