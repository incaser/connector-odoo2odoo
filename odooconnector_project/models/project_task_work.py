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

Project Task Work
=================

All implementations specific related to the export / import / mapping etc.
of project task works objects.

"""


class OdooConnectorProjectTaskWork(models.Model):
    _name = 'odooconnector.project.task.work'
    _inherit = 'odooconnector.binding'
    _inherits = {'project.task.work': 'openerp_id'}
    _description = 'Odoo Connector Project Task Work'

    openerp_id = fields.Many2one(
        comodel_name='project.task.work',
        string='Project Task Work',
        required=True,
        ondelete='restrict'
    )


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    oc_bind_ids = fields.One2many(
        comodel_name='odooconnector.project.task.work',
        inverse_name='openerp_id',
        string='Odoo Binding'
    )


@oc_odoo
class ProjectTaskWorkBatchImporter(DirectBatchImporter):
    _model_name = ['odooconnector.project.task.work']


@oc_odoo
class ProjectTaskWorkImporter(OdooImporter):
    _model_name = ['odooconnector.project.task.work']


@oc_odoo
class ProjectTaskWorkImportMapper(OdooImportMapper):
    _model_name = 'odooconnector.project.task.work'

    direct = [('name', 'name'), ('hours', 'hours'), ('date', 'date')]

    @mapping
    def task_id(self, record):
        if not record.get('task_id'):
            return
        task = self.env['project.task'].search(
            [('oc_bind_ids.backend_id', '=', self.backend_record.id),
             ('oc_bind_ids.external_id', '=', record['task_id'][0])
             ],
            limit=1
        )
        if task:
            return {'task_id': task.id}


@oc_odoo
class ProjectTaskWorkExporter(OdooExporter):
    _model_name = ['odooconnector.project.task.work']

    def _get_remote_model(self):
        return 'project.task.work'

    def _pre_export_check(self, record):
        if not self.backend_record.default_export_project_task_work:
            return False

        domain = self.backend_record.default_export_project_task_work_domain
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
                model_name='odooconnector.project.task.work',
                context={'connector_no_export': True}
            )


@oc_odoo
class ProjectTaskWorkExportMapper(ExportMapper):
    _model_name = 'odooconnector.project.task.work'

    direct = [('name', 'name'), ('hours', 'hours'), ('date', 'date')]


@oc_odoo
class OdooModelBinderProjectTaskWork(OdooModelBinder):
    _model_name = [
        'odooconnector.project.task.work',
    ]


@oc_odoo
class OdooAdapterProjectTaskWork(OdooAdapter):
    _model_name = [
        'odooconnector.project.task.work'
    ]
