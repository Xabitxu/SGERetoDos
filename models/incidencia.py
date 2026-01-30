from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Incidencia(models.Model):
    _name = 'sge.incidencia'
    _description = 'Gestión de Incidencias'

    name = fields.Char(string='Título')
    description = fields.Text(string='Descripción',required=True)
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

    proyecto = fields.Many2one(comodel_name='project.task', string='Tarea/Proyecto')
    
    # VALIDACIONES USANDO DECORADORES
    @api.onchange('name')
    def _onchange_name_validacion(self):
        """Validación en tiempo real del nombre"""
        if self.name and not self.name.strip():
            raise ValidationError('El título de la incidencia no puede estar vacío')
    
    @api.onchange('description')
    def _onchange_description_validacion(self):
        """Validación en tiempo real de la descripción"""
        if self.description and len(self.description) > 5000:
            raise ValidationError('La descripción no puede exceder 5000 caracteres')
    
    @api.constrains('name')
    def _check_name_not_empty(self):
        """Validación a nivel de base de datos del nombre"""
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError('El título de la incidencia no puede estar vacío')
    
    @api.constrains('description')
    def _check_description_length(self):
        """Validación a nivel de base de datos de la descripción"""
        for record in self:
            if record.description and len(record.description) > 5000:
                raise ValidationError('La descripción no puede exceder 5000 caracteres')
    
    @api.constrains('estado')
    def _check_estado_transitions(self):
        """Validación de transiciones de estado"""
        transiciones_validas = {
            'abierta': ['en_proceso'],
            'en_proceso': ['abierta', 'finalizada'],
            'finalizada': ['en_proceso']
        }
        
        for record in self:
            # Al crear, siempre es válido (estado default es 'abierta')
            if not record.id:
                continue
            
            # Obtener el estado anterior del BD
            estado_anterior = self.env['sge.incidencia'].search([('id', '=', record.id)])
            if estado_anterior:
                estado_anterior_val = estado_anterior[0].estado
                estado_nuevo = record.estado
                
                if estado_anterior_val != estado_nuevo:
                    if estado_nuevo not in transiciones_validas.get(estado_anterior_val, []):
                        raise ValidationError(
                            f'No se puede cambiar de "{estado_anterior_val}" a "{estado_nuevo}". '
                            f'Transiciones válidas: {", ".join(transiciones_validas[estado_anterior_val])}'
                        )
    
    # SOBRECARGA DE FUNCIONES
    @api.model
    def create(self, vals):
        """Sobrecarga de create - Se ejecuta al crear una incidencia"""
        # Aquí puedes agregar validaciones personalizadas
        if 'name' in vals and not vals['name'].strip():
            raise ValidationError('El título de la incidencia no puede estar vacío')
        
        if 'description' in vals and len(vals.get('description', '')) > 5000:
            raise ValidationError('La descripción no puede exceder 5000 caracteres')
        
        # Llamar a la función original de create
        return super().create(vals)
    
    def write(self, vals):
        """Sobrecarga de write - Se ejecuta al modificar una incidencia"""
        # Validaciones al modificar
        if 'name' in vals and not vals['name'].strip():
            raise ValidationError('El título de la incidencia no puede estar vacío')
        
        if 'description' in vals and len(vals.get('description', '')) > 5000:
            raise ValidationError('La descripción no puede exceder 5000 caracteres')
        
        # Validar cambios de estado
        if 'estado' in vals:
            estado_actual = vals['estado']
            for record in self:
                estado_anterior = record.estado
                
                # No permitir cambios inválidos de estado
                transiciones_validas = {
                    'abierta': ['en_proceso'],
                    'en_proceso': ['abierta', 'finalizada'],
                    'finalizada': ['en_proceso']
                }
                
                if estado_actual not in transiciones_validas.get(estado_anterior, []):
                    raise ValidationError(
                        f'No se puede cambiar de {estado_anterior} a {estado_actual}. '
                        f'Transiciones válidas: {transiciones_validas[estado_anterior]}'
                    )
        
        # Llamar a la función original de write
        return super().write(vals)
    
    def copy(self, default=None):
        """Sobrecarga de copy - Agrega 'copy_of_' al nombre al duplicar"""
        if default is None:
            default = {}
        
        if 'name' not in default:
            original_name = self.name or 'Incidencia'
            default['name'] = f"copy_of_{original_name}"
        
        if 'estado' not in default:
            default['estado'] = 'abierta'
        
        return super(Incidencia, self).copy(default)
    
    def action_abierta(self):
        """Cambiar estado a abierta"""
        self.estado = 'abierta'
    
    def action_en_proceso(self):
        """Cambiar estado a en_proceso"""
        self.estado = 'en_proceso'
    
    def action_finalizada(self):
        """Cambiar estado a finalizada"""
        self.estado = 'finalizada'