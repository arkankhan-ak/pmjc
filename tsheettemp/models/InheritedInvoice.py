from odoo import api,fields, models,_
class InheritedInvoice(models.Model):
    _inherit = 'account.invoice.line'

    # @api.model
    # def create(self, values):
    #     # Add code here
    #     print('called invoice-line create method')
    #     # self.write({'price_subtotal': self.line_subtotal})
    #     # values.update('{"price_subtotal"}')
    #
    #     res =  super(InheritedInvoice, self).create(values)
    #     values['price_subtotal'] = self.line_subtotal
    #     print()
    #     print(values)
    #     print()
    #     return res


    expense_ids = fields.Many2many(
        comodel_name='project.expense',
        string='Expense_ids')

    invoice_by  = fields.Selection(
        string='Invoice By',
        selection=[('by_expense', 'By Expense'),
                   ('by_workitem', 'By Work Item')],
        required=False,default='by_expense')

    line_subtotal  = fields.Float(
        string='line subtotal',
        required=False,compute='_compute_line_subtotal_')


    @api.depends('expense_ids')
    def _compute_line_subtotal_(self):
         print("function called with value :",self.expense_ids)
         for rec in self.expense_ids:
            self.line_subtotal += rec.amount

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        super(InheritedInvoice)._compute_price()
        self.price_subtotal = price_subtotal_signed = self.line_subtotal
        print('calllllllllllllled with :',self.price_subtotal,self.line_subtotal)

    # @api.onchange('invoice_by')
    # def _check_by_invoice_(self):
    #     if(self.invoice_by == 'by_expense'):
    #         print('kjskjadfjds')
    #     elif(self.invoice_by == 'by_workitem'):
    #         print('By Workitem')

    # expense_ids  = fields.One2many(
    #     comodel_name='project.expense',
    #     inverse_name='expense_id',
    #     string='Expense',
    #     required=False)
    #


class InheritedRes(models.Model):
    _inherit = 'res.partner'
    _description = ''

    invoice_ids = fields.One2many(
        comodel_name='project.expense',
        inverse_name='expense_id',
        string='Invoice Ids',
        required=False)
# class InheritedInvoiceModel(models.Model):
#     _inherit = 'account.invoice'
#     _description = 'This is Inherited invoice model'
#
#     @api.model
#     def create(self, values):
#         print('on create of invoice model')
#         print(values)
#         return super(InheritedInvoiceModel, self).create(values)
#
    @api.onchange('invoice_line_ids')
    def _compute_onchange_of_inoice_line_ids(self):
        pass
