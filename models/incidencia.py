from odoo import models, fields

class Incidencia(models.Model):
    _name = 'sge.incidencia'
    _description = 'Gestión de Incidencias'

    name = fields.Char(string='Título', required=True)
    description = fields.Text(string='Descripción')
    fecha_creacion = fields.Datetime(string='Fecha de creación', default=fields.Datetime.now)
    estado = fields.Selection([
        ('abierta', 'Abierta'),
        ('en_proceso', 'En proceso'),
        ('finalizada', 'Finalizada')
    ], string='Estado', default='abierta')

    # Usuario que crea la incidencia
    usuario_id = fields.Many2one('res.users', string='Creado por')

    # Relación con comentarios
    comentario_ids = fields.One2many('sge.comentario', 'incidencia_id', string='Comentarios')

    # Relación One2one con encuesta
    encuesta_id = fields.Many2one('sge.encuesta', string='Encuesta (1-1)')

    # Many2many: Etiquetas
    tag_ids = fields.Many2many('sge.tag', string="Etiquetas")

    proyecto = fields.Many2one('project.task', string='Tarea/Proyecto')