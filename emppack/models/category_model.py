from odoo import api ,fields , models,_
class Category(models.Model):
    _name = "category.detail"
    _rec_name = 'wages'
    _decription = "This is category module "
    wages = fields.Float(string = "Wage")