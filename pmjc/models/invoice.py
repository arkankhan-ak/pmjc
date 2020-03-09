from odoo import api, fields, models, _ 
import re
from odoo.addons import decimal_precision as dp
from datetime import date, datetime
from odoo.exceptions import UserError, ValidationError

# Invoice_line Model
class invoice_line(models.Model):
    _inherit=['account.invoice.line']
    invoice_by = fields.Selection([('workitem','Work Item'),('milestone','Milestone'),('expense','Expense'),('other','Other'),
    ('notselected','Select the type to Invoice')],string="Select to Invoice",default='notselected')
    milestone_id=fields.Many2many('pmjc.milestone', string="Project Milestone")
    other_id=fields.One2many('pmjc.other','other_id', string="Other", store=True)
    subtotal=fields.Float(string="Subtotal",compute="get_subtotal",default=0.00)
 
    @api.one
    @api.depends('milestone_id','invoice_by','other_id')
    def get_subtotal(self):
        print("get_subtotal is called")
        if self.milestone_id and self.invoice_by=='milestone':
            if self.invoice_by=='milestone':
                print("milestone")
                for line in self.milestone_id:
                    self.subtotal=self.subtotal+line.amount
                    print(line.amount)
        elif self.other_id and self.invoice_by=='other':
            if self.invoice_by=='other':
                print("invoice by other")
                for each in self.other_id:
                    print(self.other_id)
                    self.subtotal=self.subtotal+each.amount
                    print(each.amount)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        partner = self.invoice_id.partner_id
        project=self.invoice_id.project_id
        if not partner:
            warning = {
                    'title': _('Warning!'),
                    'message': _('You must first select a partner!'),
                }
            return {'warning': warning}
        elif not project:
             warning = {
                    'title': _('Warning!'),
                    'message': _('You must first select a Project!'),
                }

    @api.onchange('invoice_by')
    def get_name(self):
        for record in self:
            record.name=record.invoice_by
    
class invoice(models.Model):
    _inherit=['account.invoice']
    project_id = fields.Many2one('project.project', string='Project', store=True,required=True)

    @api.onchange('invoice_line_ids')
    def _create_product(self):
        print("create product is called")
        for record in self.invoice_line_ids:
            record.name=record.invoice_by
            record.quantity=1
            record.account_id=1
            record.price_unit=record.subtotal
            vals={
                    'name':self.project_id.name,
                    'type':'service',
                    'lst_price':record.subtotal,
                    'list_price':record.subtotal,
                    'price':record.subtotal,
                    'standard_price':record.subtotal,
                    'categ_id':8,
                    'account_id':1,
                    'product_project_id':self.project_id.id
                }
            self.env['product.product'].create(vals)
            find_product=self.env['product.product'].search([('name','=',self.project_id.name)])
            print("this is find_product")
            print(find_product)
            for each in find_product:
                record.product_id=each
                print(each.categ_id)
            print("this is unit price")
            print(record.price_unit)
            
class ProductProduct(models.Model):
    _inherit = "product.template"
    product_project_id=fields.Many2one('project.project' , string="Project")
   

   
