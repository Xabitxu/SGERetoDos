from odoo import models, fields

class Etiqueta(models.Model):
    _name = 'sge.tag'
    _description = 'Etiqueta para clasificar incidencias'

    name = fields.Char(string='Nombre', required=True)