from odoo import api ,fields , models,_
class Guardian(models.Model):
	_name = "guardian.detail"
	_rec_name = 'name'
	_decription = "This is Guardian module"
	name = fields.Char(string="guardian name")
	street = fields.Char(string="street")
	street2 = fields.Char(string="Street 2")
	city = fields.Char(string="City")
	state = fields.Char(string="State")
	country = fields.Char(string="Country")
	zipcode = fields.Integer(string="Zip Code")