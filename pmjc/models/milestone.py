from odoo import models, fields, api
import re
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError
#invoice  
class milestone(models.Model):
    _name='pmjc.milestone'
    name=fields.Char(string="Name",required=True,default="Milestone")
    start_date = fields.Datetime(string="Start Date")
    expected_end_date = fields.Datetime(string="Expected End Date")
    actual_end_date = fields.Datetime(string="Actual End Date")
    amount = fields.Float(string="Amount", default=0.0)
    approval_date = fields.Datetime(string="Approval Date")
    milestone_invoice_id= fields.Many2one('pmjc.invoice')
    status = fields.Selection([('invoiced', 'Invoiced'), ('notinvoiced', 'Not Invoiced')], string='Status', required=True, copy=False, default='notinvoiced')