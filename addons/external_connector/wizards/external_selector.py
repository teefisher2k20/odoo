from odoo import models, fields, api, _

class ExternalSelector(models.TransientModel):
    _name = 'external.selector'
    _description = 'Select External Database'

    connection_id = fields.Many2one('external.connection', string='Select Connection', required=True)

    def action_connect(self):
        self.ensure_one()
        columns, data = self.connection_id.fetch_preview_data()

        # We need a way to display this.
        # We will open a separate transient view that holds the result.

        viewer = self.env['external.data.viewer'].create({
            'connection_id': self.connection_id.id,
            'data_content': self._format_data_html(columns, data)
        })

        return {
            'name': f'Data from {self.connection_id.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'external.data.viewer',
            'res_id': viewer.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def _format_data_html(self, columns, data):
        if isinstance(columns, str): # Error message
            return f"<div class='alert alert-danger'>{columns}</div>"

        html = "<table class='table table-bordered table-striped'><thead><tr>"
        for col in columns:
            html += f"<th>{col}</th>"
        html += "</tr></thead><tbody>"

        for row in data:
            html += "<tr>"
            for cell in row:
                html += f"<td>{cell}</td>"
            html += "</tr>"
        html += "</tbody></table>"
        return html


class ExternalDataViewer(models.TransientModel):
    _name = 'external.data.viewer'
    _description = 'External Data Viewer'

    connection_id = fields.Many2one('external.connection', string='Connection', readonly=True)
    data_content = fields.Html(string='Data Preview', readonly=True)
