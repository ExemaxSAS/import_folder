from odoo import fields, models

class ProjectTag(models.Model):
    _inherit = 'project.tags'

    importation_tag = fields.Boolean(string="Etiqueta de Importación")
    exportation_tag = fields.Boolean(string="Etiqueta de Exportación")
