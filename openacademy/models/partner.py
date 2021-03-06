# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
     _inherit = 'res.partner'

# Add a new column to the res.partner model, by default partners are not instructor
     instructor = fields.Boolean(string='Instructor', default=False)
     session_ids = fields.Many2many('openacademy.session',string="Attended Session",readonly=True)

