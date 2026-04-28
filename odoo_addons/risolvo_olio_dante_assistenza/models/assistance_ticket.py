from datetime import timedelta

from odoo import api, fields, models


class RisolvoAssistanceTicket(models.Model):
    _name = "risolvo.assistance.ticket"
    _description = "Ticket assistenza Olio Dante"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "priority desc, create_date desc"

    name = fields.Char(default="New", readonly=True, copy=False)
    title = fields.Char(required=True, tracking=True)
    partner_id = fields.Many2one("res.partner", string="Cliente", tracking=True)
    site_id = fields.Many2one(
        "risolvo.assistance.site",
        string="Sede/Reparto",
        ondelete="restrict",
        tracking=True,
    )
    asset_id = fields.Many2one(
        "risolvo.assistance.asset",
        string="Asset",
        domain="[('site_id', '=', site_id)]",
        tracking=True,
    )
    requester_id = fields.Many2one("res.partner", string="Richiedente", tracking=True)
    assigned_user_id = fields.Many2one(
        "res.users",
        string="Responsabile Risolvo",
        default=lambda self: self.env.user,
        tracking=True,
    )
    category = fields.Selection(
        [
            ("incident", "Incidente"),
            ("request", "Richiesta"),
            ("change", "Modifica"),
            ("maintenance", "Manutenzione"),
        ],
        default="incident",
        required=True,
        tracking=True,
    )
    channel = fields.Selection(
        [
            ("email", "Email"),
            ("phone", "Telefono"),
            ("portal", "Portale"),
            ("internal", "Interno"),
            ("whatsapp", "WhatsApp"),
        ],
        default="email",
        required=True,
        tracking=True,
    )
    priority = fields.Selection(
        [
            ("0", "Bassa"),
            ("1", "Normale"),
            ("2", "Alta"),
            ("3", "Urgente"),
        ],
        default="1",
        required=True,
        tracking=True,
    )
    state = fields.Selection(
        [
            ("new", "Nuovo"),
            ("qualified", "Qualificato"),
            ("planned", "Pianificato"),
            ("in_progress", "In lavorazione"),
            ("waiting_customer", "In attesa cliente"),
            ("resolved", "Risolto"),
            ("closed", "Chiuso"),
            ("cancelled", "Annullato"),
        ],
        default="new",
        tracking=True,
    )
    description = fields.Html(string="Descrizione")
    impact = fields.Text(string="Impatto operativo")
    workaround = fields.Text(string="Workaround")
    root_cause = fields.Text(string="Causa radice")
    resolution = fields.Text(string="Soluzione")
    sla_id = fields.Many2one("risolvo.assistance.sla", string="SLA")
    sla_deadline = fields.Datetime(string="Scadenza SLA", tracking=True)
    is_sla_late = fields.Boolean(compute="_compute_is_sla_late", search="_search_is_sla_late")
    planned_datetime = fields.Datetime(string="Intervento pianificato", tracking=True)
    first_response_datetime = fields.Datetime(string="Prima risposta", readonly=True)
    resolved_datetime = fields.Datetime(string="Data risoluzione", readonly=True)
    closed_datetime = fields.Datetime(string="Data chiusura", readonly=True)
    intervention_ids = fields.One2many(
        "risolvo.assistance.intervention",
        "ticket_id",
        string="Interventi",
    )
    intervention_count = fields.Integer(compute="_compute_intervention_count")
    color = fields.Integer()

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"]
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = sequence.next_by_code("risolvo.assistance.ticket") or "New"
        tickets = super().create(vals_list)
        tickets._apply_default_sla()
        return tickets

    def write(self, vals):
        result = super().write(vals)
        if {"category", "priority", "sla_id"} & set(vals):
            self._apply_default_sla()
        if vals.get("state") == "resolved":
            self.filtered(lambda ticket: not ticket.resolved_datetime).resolved_datetime = fields.Datetime.now()
        if vals.get("state") == "closed":
            self.filtered(lambda ticket: not ticket.closed_datetime).closed_datetime = fields.Datetime.now()
        return result

    @api.depends("sla_deadline", "state")
    def _compute_is_sla_late(self):
        now = fields.Datetime.now()
        for ticket in self:
            ticket.is_sla_late = bool(
                ticket.sla_deadline
                and ticket.sla_deadline < now
                and ticket.state not in ("resolved", "closed", "cancelled")
            )

    def _search_is_sla_late(self, operator, value):
        is_positive = (operator in ("=", "==") and value) or (operator in ("!=", "<>") and not value)
        late_domain = [
            ("sla_deadline", "<", fields.Datetime.now()),
            ("state", "not in", ("resolved", "closed", "cancelled")),
        ]
        if is_positive:
            return late_domain
        return [
            "|",
            "|",
            ("sla_deadline", "=", False),
            ("sla_deadline", ">=", fields.Datetime.now()),
            ("state", "in", ("resolved", "closed", "cancelled")),
        ]

    def _compute_intervention_count(self):
        for ticket in self:
            ticket.intervention_count = len(ticket.intervention_ids)

    def _apply_default_sla(self):
        for ticket in self:
            sla = ticket.sla_id or self.env["risolvo.assistance.sla"].search(
                [
                    ("category", "=", ticket.category),
                    ("priority", "=", ticket.priority),
                    ("active", "=", True),
                ],
                limit=1,
            )
            if sla:
                ticket.sla_id = sla
                if not ticket.sla_deadline:
                    ticket.sla_deadline = ticket.create_date + timedelta(hours=sla.resolution_hours)

    def action_qualify(self):
        self.write({"state": "qualified"})

    def action_plan(self):
        self.write({"state": "planned"})

    def action_start(self):
        self.write({"state": "in_progress"})
        self.filtered(lambda ticket: not ticket.first_response_datetime).write(
            {"first_response_datetime": fields.Datetime.now()}
        )

    def action_wait_customer(self):
        self.write({"state": "waiting_customer"})

    def action_resolve(self):
        self.write({"state": "resolved"})

    def action_close(self):
        self.write({"state": "closed"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_view_interventions(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Interventi",
            "res_model": "risolvo.assistance.intervention",
            "view_mode": "tree,form",
            "domain": [("ticket_id", "=", self.id)],
            "context": {"default_ticket_id": self.id},
        }
