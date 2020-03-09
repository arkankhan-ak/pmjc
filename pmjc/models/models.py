# -*- coding: utf-8 -*-

from odoo import models, fields, api
import re
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError
#invoice  
class invoice(models.Model):
    _name='pmjc.invoice'
    _inherit=['account.invoice']
# class pmjc(models.Model):
#     _name = 'pmjc.pmjc'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


   
   
    
  