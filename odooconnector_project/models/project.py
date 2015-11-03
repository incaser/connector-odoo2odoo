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

Project
=======

All implementations specific related to the export / import / mapping etc.
of project objects.

"""


class OdooConnectorProjectProject(models.Model):
    _name = 'odooconnector.project.project'
    _inherit = 'odooconnector.binding'
    _inherits = {'project.project': 'openerp_id'}
    _description = 'Odoo Connector Project'

    openerp_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        required=True,
        ondelete='restrict'
    )


class ProjectProject(models.Model):
    _inherit = 'project.project'

    oc_bind_ids = fields.One2many(
        comodel_name='odooconnector.project.project',
        inverse_name='openerp_id',
        string='Odoo Binding'
    )


@oc_odoo
class ProjectBatchImporter(DirectBatchImporter):
    _model_name = ['odooconnector.project.project']


@oc_odoo
class ProjectImporter(OdooImporter):
    _model_name = ['odooconnector.project.project']


@oc_odoo
class ProjectImportMapper(OdooImportMapper):
    _model_name = 'odooconnector.project.project'

    direct = [('name', 'name')]


@oc_odoo
class ProjectExporter(OdooExporter):
    _model_name = ['odooconnector.project.project']

    def _get_remote_model(self):
        return 'project.project'

    def _pre_export_check(self, record):
        if not self.backend_record.default_export_project:
            return False

        domain = self.backend_record.default_export_project_domain
        return self._pre_export_domain_check(record, domain)

    def _after_export(self, record_created):
        # create a ic_binding in the backend, indicating that the project
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
                model_name='odooconnector.project.project',
                context={'connector_no_export': True}
            )


@oc_odoo
class ProjectExportMapper(ExportMapper):
    _model_name = 'odooconnector.project.project'

    direct = [('name', 'name'), ('ref', 'ref'), ('lang', 'lang'),
              ('date', 'date')]


@oc_odoo
class OdooModelBinderProject(OdooModelBinder):
    _model_name = [
        'odooconnector.project.project',
    ]


@oc_odoo
class OdooAdapterProject(OdooAdapter):
    _model_name = [
        'odooconnector.project.project'
    ]
