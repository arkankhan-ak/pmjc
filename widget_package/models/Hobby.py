from odoo import api,models,fields,_
class Hobby(models.Model):
	_name = 'hobby.details'
	_rec_name = 'name'

	name = fields.Char('Hobby name')
