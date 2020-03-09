# -*- coding: utf-8 -*-

from odoo import models, fields, api
from . import tools
import datetime
class Lead(models.Model):
    _inherit = "crm.lead"

class Quotation(models.Model):
    _inherit = "sale.order"
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('project', 'Project'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')


class Project(models.Model):

    _inherit = "project.project"

    group_id = fields.Many2one('project.groups',string="Project Group")


class ProjectGroup(models.Model):

    _name = "project.groups"

    name = fields.Char(string="Name of Group")
    active = fields.Boolean(string="active", default=True)

class ProjectTask(models.Model):
    _inherit = "project.task"

    azure_id = fields.Char(string="Azure Id",index=True)
    areapath = fields.Char()
    project_id = fields.Many2one('project.project', string="Project", index=True, track_visibility='onchange',default=lambda self: self.env.context.get('default_project_id'),)
    interation_path = fields.Char()
    iteration_id = fields.Char()
    state = fields.Char()
    reason = fields.Char()
    created_date = fields.Date()
    created_by_id = fields.Many2one('res.users', string='Created By')
    priority = fields.Selection([(4, 4), (3, 3), (2, 2), (1, 1), ], default='1', string="Priority")
    changed_date = fields.Date()
    changed_by_id = fields.Many2one('res.users', string='Changed By')
    title = fields.Char()
    remaining_work_hour = fields.Integer()
    original_estimate_hour = fields.Integer()
    complete_work_hour = fields.Integer()
    description = fields.Html()
    parent_task_id = fields.Many2one('project.task', string='Parent')
    #
    timesheet_id = fields.Many2one(
        comodel_name='project.mytimesheet',
        string='Timesheet',
        required=False)
    #
    child_ids = fields.One2many('project.task', 'parent_task_id', string='Tasks', domain=[('active', '=', True)])
    type = fields.Selection(selection=[('Bug', 'Bug'), ('Code Review Request', 'Code Review Request'), ('Code Review Response', 'Code Review Response'),
                                       ('Epic', 'Epic'), ('Feature', 'Feature'), ('Feedback Request', 'Feedback Request'),
                                       ('Feedback Response', 'Feedback Response'), ('Shared Steps', 'Shared Steps'), ('Test Case', 'Test Case'),
                                       ('Test Plan', 'Test Plan'), ('Test Suite', 'Test Suite'), ('User Story', 'User Story'), ('Issue', 'Issue'),
                                       ('Shared Parameter', 'Shared Parameter'), ('Task', 'Task')])

    @api.model
    def create(self, value):
        # connect with project and interatiions
        res = super(ProjectTask, self).create(value)
        print('----parent id----',res.parent_task_id.azure_id,'-----own id-----',res.azure_id)
        if res.parent_task_id.azure_id:
            print('this is parent id :',res.parent_task_id.azure_id)
            timesheet = self.env['project.mytimesheet'].search([('work_item_id','=',res.parent_task_id.id),('user_id','=',res.user_id.id)])
            if timesheet:
                print('-------timesheet exists of this employee-----------')
                print('-----employee name--------------',res.user_id.id)
                print('-----employee name--------------', res.user_id.name)
                timesheet.write({'task_ids': [(4,res.id)]})
                print('-----timesheet--------------', timesheet.task_ids)
            else:
                # work_item_id, task_ids, user_id
                print('----------creating new one-------------------')
                self.env['project.mytimesheet'].create({
                    'user_id': res.user_id.id,
                    'task_ids': [(6,0,[res.id])],
                    'work_item_id':res.parent_task_id.id,
                })
        return res

    def get_azure_data(self):
        def get_emp(ar):
            if not ar:
                return None
            emp = self.env['res.users'].search([('login', '=', ar[1])])
            if emp:
                return emp[0].id
            else:
                emp = self.env['res.users'].create(
                    {'name': ar[0], 'login': ar[1], 'password': '123'})
                return emp.id

        all_workitem = tools.work_items(date="2020-02-01", on="CreatedDate", on2="ChangedDate")
        for workitem in all_workitem:
            # FIND AND SET PERENT IF ANY THERE
            parent_obj = self.env['project.task'].search([('azure_id', '=', workitem['parent_task_id'])])
            if parent_obj:
                workitem['parent_task_id'] = parent_obj[0].id
            else:
                workitem['parent_task_id'] = None

            # FIND AND SET ALL THE CHILDRENS
            childs = []
            for i in workitem['child_ids']:
                child_obj = self.env['project.task'].search([('azure_id', '=', i)])
                if child_obj:
                    childs.append(child_obj.id)
            workitem['child_ids'] = [[6, 0, childs]]

            # setting employee create new is not assigning to RES.USERS
            workitem['user_id'] = get_emp(workitem['user_id'])
            workitem['created_by_id'] = get_emp(workitem['created_by_id'])
            workitem['changed_by_id'] = get_emp(workitem['changed_by_id'])

            # setting the project
            project = self.env['project.project'].search([('name', '=', workitem['project_id'])])
            if project:
                workitem['project_id'] = project[0].id
            else:
                res = self.env['project.project'].create(
                    {'name': workitem['project_id']})
                workitem['project_id'] = res.id

            #create or update the taskes
            odoo_rec = self.env['project.task'].search([('azure_id', '=', workitem['azure_id'])])
            if odoo_rec:
                odoo_rec[0].write(workitem)
            else:
                res = self.env['project.task'].create(workitem)

        # self.timesheet_creation()


    # def timesheet_creation(self):
        #try to fire group by query here and then insert and iterate
        # print(' Came insider --------')
        # [('created_date', '>', datetime.datetime(2020, 1, 1))]
        # data = self.env['project.task'].read_group([('created_date', '>', datetime.datetime(2020, 1, 1))],
        #                                                  ['user_id', 'parent_task_id'], ['user_id'])
        # print('-----*****-----')
        # print(data)
        # result = dict((data['user_id'],
        #                {'user_id': data['user_id'],
        #                 'parent_task_id': data['parent_task_id']
        #                 }) for data in data)
        # print('---------------result---------------')
        # print(result)
        # is_gone_inside = False
        # entries_of_today = self.env['project.task'].search([('created_date','>',datetime.datetime(2020, 1, 1))])
        # print('----en-----',entries_of_today)
        # for rec in entries_of_today:
        #     my_create_dict = {}
        #     list_employee = []
        #     list_azure_ids = []
        #     for child in rec.child_ids:
        #         if(rec.user_id.name not in list_employee):
        #             list_azure_ids = []
        #             list_azure_ids.append(child.id)
        #             list_employee.append(rec.user_id.name)
        #             print(rec.id, rec.user_id.name, '---', list_azure_ids)
        #             my_create_dict = {
        #                 'timesheet_id':rec.id,
        #                 'assigned_employee':rec.user_id.name,
        #                 'task_ids':list_azure_ids
        #             }
        #         else:
        #             list_azure_ids.append(child.id)
        #             my_create_dict.update({'task_ids':list_azure_ids})
        #         print(my_create_dict)





