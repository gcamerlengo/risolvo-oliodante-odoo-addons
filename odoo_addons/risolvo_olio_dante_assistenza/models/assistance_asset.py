from odoo import fields, models


class RisolvoAssistanceAsset(models.Model):
    _name = "risolvo.assistance.asset"
    _description = "Asset assistenza Olio Dante"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "site_id, name"

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(string="Matricola o codice interno", tracking=True)
    site_id = fields.Many2one(
        "risolvo.assistance.site",
        string="Sede/Reparto",
        required=True,
        ondelete="restrict",
        tracking=True,
    )
    partner_id = fields.Many2one(related="site_id.partner_id", store=True, readonly=True)
    asset_type = fields.Selection(
        [
            ("linea", "Linea produttiva"),
            ("macchina", "Macchina"),
            ("impianto", "Impianto"),
            ("software", "Software gestionale"),
            ("postazione", "Postazione"),
            ("altro", "Altro"),
        ],
        default="macchina",
        required=True,
        tracking=True,
    )
    criticality = fields.Selection(
        [
            ("low", "Bassa"),
            ("medium", "Media"),
            ("high", "Alta"),
            ("critical", "Critica"),
        ],
        default="medium",
        required=True,
        tracking=True,
    )
    vendor = fields.Char(string="Fornitore")
    model = fields.Char(string="Modello")
    installation_date = fields.Date(string="Data installazione")
    active = fields.Boolean(default=True)
    ticket_ids = fields.One2many("risolvo.assistance.ticket", "asset_id", string="Ticket")
    notes = fields.Text()
