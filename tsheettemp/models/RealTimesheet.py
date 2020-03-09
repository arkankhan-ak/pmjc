from odoo import api,fields,models
class RealTimesheet(models.Model):

    _name='project.mytimesheet'
    _description = 'RealTimesheet'

    t_id = fields.Integer(
        string='Timesheet ID',
        required=False)
    emp_name = fields.Char(
        string='Emp_name',
        required=False)

    work_item_ids  = fields.One2many(
        comodel_name='project.myworkitem',
        inverse_name='parent_id',
        string='Work Items',
        required=False)


    parent_id = fields.Many2one(
        comodel_name='project.myworkitem',
        string='Parent id',
        required=False)

