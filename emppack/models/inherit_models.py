from odoo import models,fields,api
from odoo.exceptions import UserError, AccessError, ValidationError

class CustomHolidaysType(models.Model):
	_inherit = "hr.holidays.status"
	is_optional = fields.Boolean("Is optional",groups="hr.group_hr_manager")

	holiday_ids = fields.One2many("hr.holidays","holiday_status_id",string="Holidaysss")

	@api.multi
	def write(self,values):
		for record in self:
			for holiday in record.holiday_ids:
				current_employee = self.env['hr.employee'].search([('id', '=', holiday.employee_id.id)])
				print("current emp name :",current_employee.name)
				if(values.get('is_optional')):
					current_employee.is_mendatory_leave_proceed = False
					current_employee.is_optional_leave_proceed = True
				if(values.get('is_optional') == False):
					current_employee.is_optional_leave_proceed = False
					current_employee.is_mendatory_leave_proceed = True

			res = super(CustomHolidaysType,record).write(values)
			return res
			

class CustomHrholidays(models.Model):
	_inherit = "hr.holidays"

	@api.multi
	def action_approve(self):
		# if double_validation: this method is the first approval approval
		# if not double_validation: this method calls action_validate() below
		super(CustomHrholidays,self).action_approve()
		for holiday in self:
			print("holiday state :",holiday.state)
			if(holiday.state=='validate'):
				current_employee = self.env['hr.employee'].search([('id', '=', holiday.employee_id.id)])
				print("current emp name :",current_employee.name)
				if(holiday.holiday_status_id.is_optional):
					current_employee.is_mendatory_leave_proceed = False
					current_employee.is_optional_leave_proceed = True
				if(holiday.holiday_status_id.is_optional == False):
					current_employee.is_optional_leave_proceed = False
					current_employee.is_mendatory_leave_proceed = True
	@api.multi
	def action_refuse(self):
		super(CustomHrholidays,self).action_refuse()
		for holiday in self:
			if(holiday.state=='refuse'):
				current_employee = self.env['hr.employee'].search([('id', '=', holiday.employee_id.id)])
				current_employee.is_optional_leave_proceed = False
				current_employee.is_mendatory_leave_proceed = False
		return True

class CustomHrEmployee(models.Model):
	_inherit = "hr.employee"

	job_type = fields.Selection([("pt","Part-Time"),("ft","Full-Time")])
	take_lunch_from_office = fields.Boolean("Want to take lunch from Office",default=False)
	joining_date = fields.Date("Joining Date")
	employement_date = fields.Date("Employement Date")

	is_optional_leave_proceed = fields.Boolean("Is Optional Leave Proceed")
	is_mendatory_leave_proceed = fields.Boolean("Is Mendatory leave Proceed")