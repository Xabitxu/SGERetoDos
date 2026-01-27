from odoo import fields, models

class project_task(models.Model):
    _inherit = "project.task"

    incidencia_id= fields.One2many(comodel_name="sge.incidencia",inverse_name="proyecto",string= "Incidencias")

    estadistica_id= fields.One2many(comodel_name="sge.estadisticas",inverse_name="proyecto",string= "Estadisticas")