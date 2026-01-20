from odoo import models, fields


class Comentario(models.Model):
    _name = 'sge.comentario'
    _description = 'Comentarios de incidencias'

    incidencia_id = fields.Many2one('sge.incidencia', string='Incidencia', required=True, ondelete='cascade')
    usuario_id = fields.Many2one('res.users', string='Usuario')
    contenido = fields.Text(string='Comentario', required=True)
    fecha = fields.Datetime(string='Fecha', default=fields.Datetime.now)