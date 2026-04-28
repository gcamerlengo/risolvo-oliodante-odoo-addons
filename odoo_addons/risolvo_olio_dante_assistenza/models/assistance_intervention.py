from odoo import api, fields, models


class RisolvoAssistanceIntervention(models.Model):
    _name = "risolvo.assistance.intervention"
    _description = "Intervento tecnico"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "start_datetime desc, id desc"

    name = fields.Char(required=True, default="Nuovo intervento", tracking=True)
    ticket_id = fields.Many2one(
        "risolvo.assistance.ticket",
        required=True,
        ondelete="cascade",
        tracking=True,
    )
    site_id = fields.Many2one(related="ticket_id.site_id", store=True, readonly=True)
    asset_id = fields.Many2one(related="ticket_id.asset_id", store=True, readonly=True)
    technician_id = fields.Many2one(
        "res.users",
        string="Tecnico",
        default=lambda self: self.env.user,
        tracking=True,
    )
    intervention_type = fields.Selection(
        [
            ("remote", "Remoto"),
            ("onsite", "Presso sede"),
            ("phone", "Telefonico"),
            ("analysis", "Analisi"),
        ],
        default="remote",
        required=True,
        tracking=True,
    )
    state = fields.Selection(
        [
            ("planned", "Pianificato"),
            ("running", "In corso"),
            ("done", "Completato"),
            ("cancelled", "Annullato"),
        ],
        default="planned",
        tracking=True,
    )
    start_datetime = fields.Datetime(string="Inizio")
    end_datetime = fields.Datetime(string="Fine")
    duration_hours = fields.Float(compute="_compute_duration_hours", store=True)
    work_done = fields.Text(string="Attivita svolta")
    parts_used = fields.Text(string="Materiali/Ricambi")
    customer_feedback = fields.Text(string="Feedback cliente")

    @api.depends("start_datetime", "end_datetime")
    def _compute_duration_hours(self):
        for record in self:
            if record.start_datetime and record.end_datetime:
                delta = record.end_datetime - record.start_datetime
                record.duration_hours = delta.total_seconds() / 3600
            else:
                record.duration_hours = 0.0

    def action_start(self):
        for record in self:
            record.state = "running"
            if not record.start_datetime:
                record.start_datetime = fields.Datetime.now()

    def action_done(self):
        for record in self:
            record.state = "done"
            if not record.end_datetime:
                record.end_datetime = fields.Datetime.now()
