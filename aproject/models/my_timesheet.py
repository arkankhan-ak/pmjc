from odoo import api,fields,models
class MyTimesheet(models.Model):
    _name = 'project.mytimesheet'
    _description = 'MyTimesheet'

    name = fields.Char()

    work_item_id = fields.Many2one(
        comodel_name='project.task',
        string='Workitem Parent',
        required=False)

    task_ids = fields.One2many(
        comodel_name='project.task',
        inverse_name='timesheet_id',
        string='TImesheet Id',
        required=False)

    user_id = fields.Many2one(
        comodel_name='res.user',
        string='Employe Name',
        required=False)