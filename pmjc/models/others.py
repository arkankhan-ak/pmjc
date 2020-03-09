from odoo import models, fields, api
import re
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError
#invoice  
class Other(models.Model):
    _name='pmjc.other'
    name=fields.Char(string="Name",required=True,default="Other")
    description=fields.Char(string="Description")
    date = fields.Datetime(string="Date")
    amount = fields.Float(string="Amount", default=0.0)
    other_id=fields.Many2one('account.invoice.line', string="Other")
