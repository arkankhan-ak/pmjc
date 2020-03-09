from odoo import api, fields, models

class StudentModel(models.Model):
    _name = 'student.student'
    _rec_name = 'name'

    name = fields.Char(string="Enter your name",required=True)
    marks = fields.Float(string="Marks",required=True)
    gender = fields.Selection([('m','Male'),('f','Female')],string="Gender")
    
    