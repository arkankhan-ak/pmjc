from odoo import api, fields, models, _
class Classroom(models.Model):
    _name = 'classroom.details'
    _rec_name = 'name'

    name = fields.Char("Name")
    noOfStudent = fields.Integer("No Of Students")
    student_ids = fields.One2many("student.details",inverse_name="classroom_id",string="Students")

