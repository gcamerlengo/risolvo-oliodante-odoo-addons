from odoo import fields, models


class RisolvoAssistanceSite(models.Model):
    _name = "risolvo.assistance.site"
    _description = "Sede assistenza Olio Dante"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(required=True, tracking=True)
    partner_id = fields.Many2one("res.partner", string="Cliente", tracking=True)
    contact_id = fields.Many2one(
        "res.partner",
        string="Referente operativo",
        domain="[('parent_id', '=', partner_id)]",
        tracking=True,
    )
    plant_area = fields.Selection(
        [
            ("ricevimento", "Ricevimento materie prime"),
            ("produzione", "Produzione"),
            ("confezionamento", "Confezionamento"),
            ("magazzino", "Magazzino"),
            ("qualita", "Qualita"),
            ("uffici", "Uffici"),
        ],
        string="Area",
        tracking=True,
    )
    address = fields.Char(string="Indirizzo")
    notes = fields.Text()
    active = fields.Boolean(default=True)
    asset_ids = fields.One2many("risolvo.assistance.asset", "site_id", string="Asset")
    ticket_ids = fields.One2many("risolvo.assistance.ticket", "site_id", string="Ticket")
