# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions
from odoo.exceptions import ValidationError


class Session(models.Model):
     _name = 'openacademy.session'
     _description = 'Openacademy Sessions'

     name = fields.Char(string='Session', required=True, help="Name of Session")
     start_date = fields.Date(default=fields.Date.today())
     duration = fields.Float(digits=(6,2),help="Duration in Days")#1111.11
     seats = fields.Integer(string="Number of Seats")
     active = fields.Boolean(default=True)

     instructor_id = fields.Many2one('res.partner',string='Instructor',domain="[('instructor','=',True)]")
     course_id = fields.Many2one('openacademy.course', ondelete='cascade',string='Course',required=True)
     attendees = fields.Many2many('res.partner',string="Attendees")

     taken_seats = fields.Float(string="Taken Seats",compute="_taken_seats")
     @api.depends('seats','attendees')
     def _taken_seats(self):
          for record in self:
               if not record.seats:
                    record.taken_seats=0.0
               else:
                    record.taken_seats = 100*(len(record.attendees))/(record.seats)

     @api.onchange('seats','attendees')
     def verify_valid_seats(self):
          if self.seats<0:
               return {
                    'warning':{
                         'title': "Incorrect 'seats' value",
                         'message': "The number of available seats may not be negative"
                    },
               }
          if self.seats<len(self.attendees):
               return {
                    'warning': {
                         'title': "Too many attendees",
                         'message': "Increase seats or remove excess attendees"
                    },
               }
     @api.constrains('instructor_id','attendees')
     def check_instructor_not_in_attendees(self):
          for r in self:
               if r.instructor_id and r.instructor_id in r.attendees:
                    raise exceptions.ValidationError("A session's instructor can't be an attendee")



