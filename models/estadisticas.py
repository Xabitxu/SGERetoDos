from odoo import models, fields, api
from datetime import date
from odoo.exceptions import UserError
from stdnum.exceptions import ValidationError


class Estadisticas(models.Model):
    _name = 'sge.estadisticas'
    _description = 'Estadísticas de incidencias'

    name = fields.Char(string='Nombre')
    fecha = fields.Date(string='Fecha', required=True)
    total_incidencias = fields.Integer(string='Total de incidencias', compute= 'calcularTotal', readonly=True, store=True)
    incidencias_finalizadas = fields.Integer(string='Incidencias finalizadas', compute='calcularTotal', readonly=True)
    tiempo_promedio_resolucion = fields.Float(string='Tiempo promedio de resolución (horas)', compute='calcularTotal', readonly=True)
    proyecto = fields.Many2one(comodel_name='project.task', string= 'Tarea/Proyecto')

    @api.onchange('fecha')
    def _onchange_fecha_validacion(self):
        if self.fecha and self.fecha > date.today():
            raise UserError("No puedes seleccionar una fecha futura.")

    @api.constrains('fecha')
    def _check_estadisticas_con_incidencias(self):
        incidencia_model = self.env['sge.incidencia']

        for record in self:
            if not record.fecha:
                continue

            incidencias = incidencia_model.search_count([
                ('fecha_creacion', '>=', f"{record.fecha} 00:00:00"),
                ('fecha_creacion', '<=', f"{record.fecha} 23:59:59")
            ])

            if incidencias == 0:
                raise ValidationError(
                    "No se pueden guardar estadísticas sin incidencias para ese día."
                )

    @api.model
    def create(self, vals):
        if not vals.get('name') and vals.get('fecha'):
            vals['name'] = f"Estadísticas del {vals['fecha']}"
        return super().create(vals)

    @api.depends('fecha')
    def calcularTotal(self):
        incidencia_model = self.env['sge.incidencia']

        for record in self:
            if not record.fecha:
                record.total_incidencias = 0
                record.incidencias_finalizadas = 0
                record.tiempo_promedio_resolucion = 0
                continue

            # Incidencias creadas ese día
            incidencias = incidencia_model.search([
                ('fecha_creacion', '>=', f"{record.fecha} 00:00:00"),
                ('fecha_creacion', '<=', f"{record.fecha} 23:59:59")
            ])
            total = len(incidencias)

            # Incidencias finalizadas ese día
            finalizadas = incidencia_model.search([
                ('fecha_creacion', '>=', f"{record.fecha} 00:00:00"),
                ('fecha_creacion', '<=', f"{record.fecha} 23:59:59"),
                ('estado', '=', 'finalizada')
            ])
            finalizadas_total = len(finalizadas)

            record.total_incidencias = total
            record.incidencias_finalizadas = finalizadas_total

            if total > 0:
                record.tiempo_promedio_resolucion = finalizadas_total / total
            else:
                record.tiempo_promedio_resolucion = 0