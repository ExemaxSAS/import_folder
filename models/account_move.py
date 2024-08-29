# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _
import logging

# Configura el logger para registrar mensajes de depuración y errores
_logger = logging.getLogger(__name__)

# Define una nueva clase que hereda del modelo 'account.move'
class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
     
    # Campo para visualizar el transito picking 
    '''transit_picking_info = fields.Text(
        string='Tránsito Picking Info',
        compute='_compute_transit_picking_info',
        store=True
    )'''
    
    # Define un campo Many2many para asociar varias tareas de proyecto a un movimiento contable
    task_id = fields.Many2many('project.task', string='Carpeta de importación', readonly=False)
    
    # Define un campo Booleano que se calcula automáticamente y se almacena en la base de datos
    is_import_page_visible = fields.Boolean(compute='_compute_is_import_page_visible', store=True)

    # Método para calcular el valor del campo 'is_import_page_visible'
    @api.depends('move_type', 'task_id.project_id.exportation')
    def _compute_is_import_page_visible(self):
        for record in self:
            # Calcula si la pestaña de importación debe ser visible
            # La pestaña es visible si no es una factura de salida (out_invoice) y si la tarea asociada no es de exportación
            record.is_import_page_visible = not (record.move_type == 'out_invoice' or (record.task_id and record.task_id.project_id.exportation))

# Define una nueva clase que hereda del modelo 'account.move.line'
class AccountMoveInheritLine(models.Model):
    _inherit = 'account.move.line'

    # Define un campo Many2one para asociar una orden de venta con una línea de movimiento contable
    sale_id = fields.Many2one('sale.order', string='Sale Order', compute='_compute_sale_id')

    # Método para calcular el valor del campo 'sale_id'
    def _compute_sale_id(self):
        for rec in self:
            # Si la línea de movimiento tiene líneas de venta asociadas
            if rec.sale_line_ids:
                # Asigna la orden de venta correspondiente al campo 'sale_id'
                rec.sale_id = rec.sale_line_ids.order_id.id
            else:
                # Si no hay líneas de venta, asigna False
                rec.sale_id = False


    '''@api.depends('invoice_line_ids')
    def _compute_transit_picking_info(self):
        for move in self:
            transit_info = []
            for line in move.invoice_line_ids:
                # Verifica si el producto es importado y tiene un lote asociado
                if line.product_id.is_imported and line.lot_id:
                    # Obten la información del picking en tránsito basado en el lote
                    pickings = line.lot_id.dispatch_ids.filtered(lambda p: p.state not in ('done', 'cancel'))
                    for picking in pickings:
                        transit_info.append(f"Picking: {picking.name} - Ubicación: {picking.location_dest_id.display_name}")
            move.transit_picking_info = "\n".join(transit_info)'''            
