from odoo import api,fields,models

class Expense(models.Model):
    _name = 'project.expense'
    _description = 'Expense Model For invoices'

    name = fields.Char()
    amount = fields.Float(
        string='Amount',
        required=False)

    description = fields.Char(
        string='Description ',
        required=False)

    expense_id = fields.Many2one(
        comodel_name='res.partner',
        string='Expense_id',
        required=False)
