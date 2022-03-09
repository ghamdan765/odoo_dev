# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero #we use this methods when working with floats

class EstateProperty(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The offer price must be positive"),
    ]

    # ---------------------------------------- Default Methods ------------------------------------

    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    name = fields.Char(string='Title', required=True, help="The type name of property.")  # index=True
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(string='Available From', copy=False, default=lambda self: self._default_date_availability())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms",default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer(string='Garden Area (sqm)')




    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )

    # Special
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default='new',
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ]
    )

    # Relational
    proerty_type_id = fields.Many2one('estate.property.type', ondelete='set null',string='Property Type')
    salesman = fields.Many2one('res.users', ondelete='set null', string='Salesperson',default=lambda self: self.env.user,index=True)
    buyer = fields.Many2one('res.partner', ondelete='set null', string='Buyer', readonly=True, copy=False)
    tag_ids = fields.Many2many('estate.property.tag',string="Tags")
    offer_ids = fields.One2many('estate.property.offer','property_id',string="Offers")

    # Computed
    total_area = fields.Integer(
        "Total Area (sqm)",
        compute="_compute_total_area",
        help="Total area computed by summing the living area and the garden area",
    )
    best_price = fields.Float("Best Offer", compute="_compute_best_price", help="Best offer received")

    # ---------------------------------------- Compute methods ------------------------------------

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped("price")) if prop.offer_ids else 0.0



    # ----------------------------------- Constrains and Onchanges --------------------------------

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                    not float_is_zero(prop.selling_price, precision_rounding=0.01)
                    and float_compare(prop.selling_price, prop.expected_price * 90.0 / 100.0,
                                      precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )
            # float precision_rounding: decimal number
            # representing the minimum non - zero value at the desired precision
            # (for example, 0.01 for a 2-digit precision).

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False


    # ------------------------------------------ CRUD Methods -------------------------------------
    #
    # def unlink(self):
    #     if not set(self.mapped("state")) <= {"new", "canceled"}:
    #         raise UserError("Only new and canceled properties can be deleted.")
    #     return super().unlink()

    def unlink(self):
        for record in self:
            if record.state not in {"new", "canceled"}:
                raise UserError("Only new and canceled properties can be deleted.")
            return super().unlink()


    # ---------------------------------------- Action Methods -------------------------------------

    def action_set_property_to_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def action_set_property_to_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})








