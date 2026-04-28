from odoo import fields, models


class RisolvoAssistanceSla(models.Model):
    _name = "risolvo.assistance.sla"
    _description = "Politica SLA assistenza"
    _order = "priority desc, category"

    name = fields.Char(required=True)
    category = fields.Selection(
        [
            ("incident", "Incidente"),
            ("request", "Richiesta"),
            ("change", "Modifica"),
            ("maintenance", "Manutenzione"),
        ],
        required=True,
    )
    priority = fields.Selection(
        [
            ("0", "Bassa"),
            ("1", "Normale"),
            ("2", "Alta"),
            ("3", "Urgente"),
        ],
        required=True,
        default="1",
    )
    response_hours = fields.Float(string="Ore presa in carico", default=4.0)
    resolution_hours = fields.Float(string="Ore risoluzione", default=24.0)
    active = fields.Boolean(default=True)
