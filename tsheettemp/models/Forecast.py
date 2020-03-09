from odoo import api,fields, models,_
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as obtained_system_date_format
import datetime
class Forecasting(models.Model):
    _name = 'project.forecasting'
    _description = 'Forecasting'

    from_date = fields.Date(
        string='From Date',
        required=False)
    to_date = fields.Date(
        string='ToDate',
        required=False)
    billing_percentage = fields.Float(
        string='Billing Percentage',
        required=False)
    employee_name = fields.Char(
        string='Employee Name',
        required=False)

