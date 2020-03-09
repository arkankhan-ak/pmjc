from odoo import api, models, fields, _
class Subject(models.Model):
    _name = 'subject.details'
    _rec_name = 'subject_name'
    
    subject_name = fields.Char("Name Of Subject")
    credit = fields.Float("Credit of Subject")