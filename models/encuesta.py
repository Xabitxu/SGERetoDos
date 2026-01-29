from odoo import models, fields

class Encuesta(models.Model):
    _name = 'sge.encuesta'
    _description = 'Encuesta de satisfacción sobre la incidencia'
    _order = 'create_date desc'

    name = fields.Char(
        string='Título',
        required=True
    )

    task_id = fields.Many2one(
        'project.task',
        string='Tarea asociada',
        ondelete='cascade'
    )

    incidencia_id = fields.Many2one(
        'sge.incidencia',
        string='Incidencia asociada',
        ondelete='cascade',
        required=True
    )

    puntuacion = fields.Selection([
        ('1', '😠 Muy mala'),
        ('2', '😕 Mala'),
        ('3', '😐 Normal'),
        ('4', '😊 Buena'),
        ('5', '😄 Excelente')
    ], string='Puntuación', required=True, default='3')

    emoticono_puntuacion = fields.Char(
        string='Emoticono',
        compute='_compute_emoticono',
        store=False
    )

    observaciones = fields.Text(string='Observaciones')

    fecha = fields.Date(
        string='Fecha',
        default=fields.Date.today,
        readonly=True
    )

    estado = fields.Selection([
        ('borrador', '📝 Borrador'),
        ('completada', '✅ Completada')
    ], string='Estado', default='borrador')

    def _compute_emoticono(self):
        emoticonos = {
            '1': '😠',
            '2': '😕',
            '3': '😐',
            '4': '😊',
            '5': '😄'
        }
        for record in self:
            record.emoticono_puntuacion = emoticonos.get(record.puntuacion, '😐')

    def action_completar(self):
        self.estado = 'completada'

    def action_borrador(self):
        self.estado = 'borrador'