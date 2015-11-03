# -*- coding: utf-8 -*-
# (c) 2015 Incaser Informatica S.L. - Sergio Teruel
# (c) 2015 Incaser Informatica S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
from openerp.addons.connector.session import ConnectorSession

from openerp.addons.odooconnector_base.unit.import_synchronizer import import_batch


class OdooBackend(models.Model):

    _inherit = 'odooconnector.backend'

    import_project_domain_filter = fields.Char(
        string='Project Domain Filter',
    )
    import_project_task_domain_filter = fields.Char(
        string='Project Task Domain Filter',
    )
    import_project_task_work_domain_filter = fields.Char(
        string='Project Task Work Domain Filter',
    )
    default_export_project = fields.Boolean(
        string='Export Projects'
    )
    default_export_project_domain = fields.Char(
        string='Export Project Domain',
        default='[]'
    )
    default_export_project_task = fields.Boolean(
        string='Export Project Tasks'
    )
    default_export_project_task_domain = fields.Char(
        string='Export Project Task Domain',
        default='[]'
    )
    default_export_project_task_work = fields.Boolean(
        string='Export Project Task Works'
    )
    default_export_project_task_work_domain = fields.Char(
        string='Export Project Task Work Domain',
        default='[]'
    )



    @api.multi
    def import_project(self):
        """ Import projects from external system """
        session = ConnectorSession(self.env.cr, self.env.uid,
                                   context=self.env.context)
        for backend in self:
            filters = self.import_project_domain_filter
            if filters and isinstance(filters, str):
                filters = eval(filters)

            import_batch(session, 'odooconnector.project.project', backend.id,
                         filters)
        return True

    @api.multi
    def import_project_task(self):
        """ Import projects task from external system """
        session = ConnectorSession(self.env.cr, self.env.uid,
                                   context=self.env.context)
        for backend in self:
            filters = self.import_project_task_domain_filter
            if filters and isinstance(filters, str):
                filters = eval(filters)

            import_batch(session, 'odooconnector.project.task', backend.id,
                         filters)
        return True

    @api.multi
    def import_project_task_work(self):
        """ Import projects task work from external system """
        session = ConnectorSession(self.env.cr, self.env.uid,
                                   context=self.env.context)
        for backend in self:
            filters = self.import_project_task_work_domain_filter
            if filters and isinstance(filters, str):
                filters = eval(filters)

            import_batch(
                session, 'odooconnector.project.task.work', backend.id,
                filters)
        return True
