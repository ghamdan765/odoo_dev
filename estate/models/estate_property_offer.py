# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare

# A property offer is an amount a potential buyer offers to the seller.
#عرض العقار هو العرض الذي يقدمه المشتري المحتمل للبائع وقد يكون أقل أو أكثر من السعر المتوقع

class EstatePropertyOffer(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be strictly positive"),
    ]

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    price = fields.Float("Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)


    # Special
    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
        default=False,
    )


    # Relational
    partner_id = fields.Many2one('res.partner', ondelete='cascade', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', ondelete='cascade', string='Property', required=True)

    # For stat button:
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.proerty_type_id", string="Property Type", store=True
    )

    # Computed
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # ---------------------------------------- Compute methods ------------------------------------

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    # ------------------------------------------ CRUD Methods -------------------------------------

    @api.model
    def create(self, vals):
        #ensure from required fields
        if vals.get("property_id") and vals.get("price"):
            #then we instantiate an estate.property object
            prop = self.env["estate.property"].browse(vals["property_id"])
            # We check if the offer is higher than the existing offers
            if prop.offer_ids:
                max_offer = max(prop.mapped("offer_ids.price"))
                if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError("The offer must be higher than %.2f" % max_offer)
            prop.state = "offer received"
        return super().create(vals)


    # ---------------------------------------- Action Methods -------------------------------------
    def action_accept(self):
        if "accepted" in self.mapped("property_id.offer_ids.state"):
            raise UserError("An offer as already been accepted.")
        self.write(
            {
                "state": "accepted",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "offer accepted",
                "selling_price": self.price,
                "buyer": self.partner_id.id,
            }
        )

    def action_refuse(self):
        return self.write(
            {
                "state": "refused",
            }
        )

    # def action_refuse(self):
    #     if self.state == "refused":
    #         raise UserError("An offer as already been refused.")
    #     self.write(
    #         {
    #             "state": "refused",
    #         }
    #     )
    #     return self.mapped("property_id").write(
    #         {
    #
    #             "selling_price": False,
    #             "buyer": False,
    #         }
    #     )


