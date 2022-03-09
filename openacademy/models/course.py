# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Course(models.Model):
     _name = 'openacademy.course'
     _description = 'Openacademy Courses'

     name = fields.Char(string='Title', required=True, help="Name of Course")
     description = fields.Text()
     responsible_id = fields.Many2one('res.users',ondelete='set null',string='Responsible',index=True)
     session_ids = fields.One2many('openacademy.session','course_id',string="Session")

     _sql_constraints = [
          ('name_unique',
           'UNIQUE (name)',
           "The course title must be unique "),
          ('name_description_check',
           'CHECK(name != description)',
           "The title of the course should not be the description ")
          ]
     # if you delete this constraints from here don't delete from database
     # if you want delete this constaints from data base change conditions
     # above to CHECK(1=1) this is like delete constraints


