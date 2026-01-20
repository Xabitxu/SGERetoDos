# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Grupo2_Estadisticas',
    'version': '1.0',
    'summary': 'Gestión de incidencias y estadísticas',
    'author': 'xabi',
    'category': 'Estadisticas',
    'depends': ['project'],
    'data': [
        'security/estadisticas_security.xml',
        'security/ir.model.access.csv',
        'view/menu_estadisticas.xml',
        'view/estadisticas.xml',
    ],
    'installable': True,
    'application': True,
}