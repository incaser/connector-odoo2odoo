# -*- coding: utf-8 -*-
# (c) 2015 Incaser Informatica S.L. - Sergio Teruel
# (c) 2015 Incaser Informatica S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import logging
from openerp import models, fields
from openerp.addons.connector.unit.mapper import (mapping, ExportMapper)
from openerp.addons.odooconnector_base.backend import oc_odoo
from openerp.addons.odooconnector_base.unit.backend_adapter import OdooAdapter
from openerp.addons.odooconnector_base.unit.binder import OdooModelBinder
from openerp.addons.odooconnector_base.unit.import_synchronizer import (
    OdooImporter,DirectBatchImporter)
from openerp.addons.odooconnector_base.unit.export_synchronizer import (
    OdooExporter)
from openerp.addons.odooconnector_base.unit.mapper import OdooImportMapper


_logger = logging.getLogger(__name__)


"""

Project Task
============

All implementations specific related to the export / import / mapping etc.
of project task objects.

"""


class OdooConnectorProjectTask(models.Model):
    _name = 'odooconnector.project.task'
    _inherit = 'odooconnector.binding'
    _inherits = {'project.task': 'openerp_id'}
    _description = 'Odoo Connector Project Task'

    openerp_id = fields.Many2one(
        comodel_name='project.task',
        string='Project Task',
        required=True,
        ondelete='restrict'
    )


class ProjectTask(models.Model):
    _inherit = 'project.task'

    oc_bind_ids = fields.One2many(
        comodel_name='odooconnector.project.task',
        inverse_name='openerp_id',
        string='Odoo Binding'
    )


@oc_odoo
class ProjectTaskBatchImporter(DirectBatchImporter):
    _model_name = ['odooconnector.project.task']


@oc_odoo
class ProjectTaskImporter(OdooImporter):
    _model_name = ['odooconnector.project.task']


@oc_odoo
class ProjectTaskImportMapper(OdooImportMapper):
    _model_name = 'odooconnector.project.task'

    direct = [('name', 'name'), ('description', 'description'), ('priority', 'priority'),
              ('kanban_state', 'kanban_state'), ('date_start', 'date_start'), ('date_end', 'date_end'),
              ('date_deadline', 'date_deadline'), ('date_last_stage_update', 'date_last_stage_update'), ('notes', 'notes'),
              ('planned_hours', 'planned_hours'), ('effective_hours', 'effective_hours'), ('remaining_hours', 'remaining_hours'),
              ]

    @mapping
    def project_id(self, record):
        if not record.get('project_id'):
            return
        project = self.env['project.project'].search(
            [('oc_bind_ids.backend_id', '=', self.backend_record.id),
             ('oc_bind_ids.external_id', '=', record['project_id'][0])
             ],
            limit=1
        )
        if project:
            return {'project_id': project.id}


@oc_odoo
class ProjectTaskExporter(OdooExporter):
    _model_name = ['odooconnector.project.task']

    def _get_remote_model(self):
        return 'project.task'

    def _pre_export_check(self, record):
        if not self.backend_record.default_export_project_task:
            return False

        domain = self.backend_record.default_export_project_task_domain
        return self._pre_export_domain_check(record, domain)

    def _after_export(self, record_created):
        # create a ic_binding in the backend, indicating that the project task
        # was exported
        if record_created:
            record_id = self.binder.unwrap_binding(self.binding_id)
            data = {
                'backend_id': self.backend_record.export_backend_id,
                'openerp_id': self.external_id,
                'external_id': record_id,
                'exported_record': False
            }
            self.backend_adapter.create(
                data,
                model_name='odooconnector.project.task',
                context={'connector_no_export': True}
            )


@oc_odoo
class ProjectTaskExportMapper(ExportMapper):
    _model_name = 'odooconnector.project.task'

    direct = [('name', 'name'), ('ref', 'ref'), ('lang', 'lang'),
              ('date', 'date')]


@oc_odoo
class OdooModelBinderProjectTask(OdooModelBinder):
    _model_name = [
        'odooconnector.project.task',
    ]


@oc_odoo
class OdooAdapterProjectTask(OdooAdapter):
    _model_name = [
        'odooconnector.project.task'
    ]
