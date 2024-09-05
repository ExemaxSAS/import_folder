from odoo import fields, models

class ProjectTag(models.Model):
    _inherit = 'project.tags'

    #importation_tag_import = fields.Boolean(string="Etiqueta de Importación (Importación)")
    is_import = fields.Boolean(string="Importación", default=True)

