from odoo import models, fields,  api
from odoo.exceptions import ValidationError

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


    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError("El título de la encuesta es obligatorio")
            if len(record.name.strip()) < 3:
                raise ValidationError("El título debe tener al menos 3 caracteres")
    @api.constrains('incidencia_id')
    def _check_incidencia(self):
        for record in self:
            if not record.incidencia_id:
                raise ValidationError("Debe seleccionar una incidencia asociada")
    @api.constrains('task_id')
    def _check_task_id(self):
        for record in self:
            if not record.task_id:
                raise ValidationError("Debe seleccionar una tarea asociada")

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

    imagen_adjunta = fields.Binary(
        string='Imagen Adjunta',
        help='Adjunta una imagen relacionada con la encuesta'
    )

    nombre_imagen = fields.Char(
        string='Nombre de la imagen',
        help='Nombre del archivo de imagen'
    )

    def copy(self, default=None):
        if default is None:
            default = {}

        if 'name' not in default:
            original_name = self.name or 'Encuesta'
            default['name'] = f"copy_of_{original_name}"

        if 'estado' not in default:
            default['estado'] = 'borrador'

        return super(Encuesta, self).copy(default)