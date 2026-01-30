from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Comentario(models.Model):
    _name = 'sge.comentario'
    _description = 'Comentarios de incidencias'

    incidencia_id = fields.Many2one('sge.incidencia', string='Incidencia', required=True, ondelete='cascade')
    usuario_id = fields.Many2one('res.users', string='Usuario')
    contenido = fields.Text(string='Comentario', required=True)
    fecha = fields.Datetime(string='Fecha', default=fields.Datetime.now)
    
    # VALIDACIONES USANDO DECORADORES
    @api.onchange('contenido')
    def _onchange_contenido_validacion(self):
        """Validación en tiempo real del contenido"""
        if self.contenido and not self.contenido.strip():
            raise ValidationError('El contenido del comentario no puede estar vacío')
        if self.contenido and len(self.contenido) > 10000:
            raise ValidationError('El comentario no puede exceder 10000 caracteres')
    
    @api.constrains('contenido')
    def _check_contenido_not_empty(self):
        """Validación a nivel de base de datos del contenido"""
        for record in self:
            if not record.contenido or not record.contenido.strip():
                raise ValidationError('El contenido del comentario no puede estar vacío')
    
    @api.constrains('contenido')
    def _check_contenido_length(self):
        """Validación de longitud máxima del contenido"""
        for record in self:
            if record.contenido and len(record.contenido) > 10000:
                raise ValidationError('El comentario no puede exceder 10000 caracteres')
    
    @api.constrains('incidencia_id')
    def _check_incidencia_required(self):
        """Validación: debe estar asociado a una incidencia"""
        for record in self:
            if not record.incidencia_id:
                raise ValidationError('Un comentario debe estar asociado a una incidencia')
    
    # SOBRECARGA DE FUNCIONES
    @api.model
    def create(self, vals):
        """Sobrecarga de create - Se ejecuta al crear un comentario"""
        # Validación: el contenido no puede estar vacío
        if 'contenido' in vals and not vals['contenido'].strip():
            raise ValidationError('El contenido del comentario no puede estar vacío')
        
        # Validación: máximo de caracteres
        if 'contenido' in vals and len(vals.get('contenido', '')) > 10000:
            raise ValidationError('El comentario no puede exceder 10000 caracteres')
        
        # Validación: debe estar asociado a una incidencia
        if 'incidencia_id' not in vals or not vals['incidencia_id']:
            raise ValidationError('Un comentario debe estar asociado a una incidencia')
        
        # Llamar a la función original
        return super().create(vals)
    
    def write(self, vals):
        """Sobrecarga de write - Se ejecuta al modificar un comentario"""
        # Validación: el contenido no puede estar vacío
        if 'contenido' in vals and not vals['contenido'].strip():
            raise ValidationError('El contenido del comentario no puede estar vacío')
        
        # Validación: máximo de caracteres
        if 'contenido' in vals and len(vals.get('contenido', '')) > 10000:
            raise ValidationError('El comentario no puede exceder 10000 caracteres')
        
        # Llamar a la función original
        return super().write(vals)
    
    def copy(self, default=None):
        """Sobrecarga de copy - Agrega 'copy_of_' al contenido al duplicar"""
        if default is None:
            default = {}
        
        if 'contenido' not in default:
            original_contenido = self.contenido or 'Comentario'
            default['contenido'] = f"copy_of_{original_contenido}"
        
        return super(Comentario, self).copy(default)