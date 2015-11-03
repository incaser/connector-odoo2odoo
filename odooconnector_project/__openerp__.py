# -*- coding: utf-8 -*-
# (c) 2015 Incaser Informatica S.L. - Sergio Teruel
# (c) 2015 Incaser Informatica S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Odoo Connector - Project',
    'summary': 'Technical base for project related Odoo Connector scenarios',
    'version': '8.0.1.0.0',
    'category': 'Connector',
    'website': 'https://odoo-community.org/',
    'author': 'Incaser Informatica S.L., Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'project',
        'odooconnector_base',
    ],
    'data': [
        'views/project.xml',
        'views/odooconnector_backend.xml',
    ],
}
