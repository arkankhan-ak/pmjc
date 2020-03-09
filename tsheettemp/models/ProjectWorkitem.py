from odoo import api,fields,models,_
class ProjectWorkitems(models.Model):
    _name = "project.myworkitem"
    _rec_name = 'azure_id'

    azure_id = fields.Char(string="Azure Id",)
    areapath = fields.Char()
    project = fields.Char()
    interation_path = fields.Char()
    iteration_id = fields.Char()
    state = fields.Char()
    reason = fields.Char()
    assigned_to = fields.Char()
    created_date = fields.Date()
    created_by = fields.Char()
    changed_date = fields.Date()
    changed_by = fields.Char()
    title = fields.Char()
    priority = fields.Integer()
    remaining_work_hour = fields.Integer()
    original_estimate_hour = fields.Integer()
    complete_work_hour = fields.Integer()
    active = fields.Boolean(default=True)
    parent_id = fields.Many2one('project.myworkitem', string='Parent', index=True)
    child_ids = fields.One2many('project.myworkitem', 'parent_id', string='Tasks', domain=[('active', '=', True)])
    type = fields.Selection(selection=[('Bug', 'Bug'), ('Code Review Request', 'Code Review Request'), ('Code Review Response', 'Code Review Response'),
                                       ('Epic', 'Epic'), ('Feature', 'Feature'), ('Feedback Request', 'Feedback Request'),
                                       ('Feedback Response', 'Feedback Response'), ('Shared Steps', 'Shared Steps'), ('Test Case', 'Test Case'),
                                       ('Test Plan', 'Test Plan'), ('Test Suite', 'Test Suite'), ('User Story', 'User Story'), ('Issue', 'Issue'),
                                       ('Shared Parameter', 'Shared Parameter'), ('Task', 'Task')])

    timesheet_id = fields.Many2one(
        comodel_name='project.mytimesheet',
        string='timesheet id',
        required=False)

    # @api.multi
    # def write(self, values):
    #     # Add code here to add tsheet workitem and employee wise for perticular date
    #     res = super(ProjectWorkitems, self).write(values)
    #     if (values.get('child_ids') and len(values.get('child_ids')) > 0):
    #         timesheet_values = {
    #             't_id': values.get('azure_id'),
    #             'emp_name': values.get('assigned_to'),
    #             'work_item_ids': values.get('child_ids')
    #         }
    #         # self.env['project.mytimesheet'].write(timesheet_values)
    #     return res
    @api.model
    def create(self, values):
        # will create dict per employee and will store all w item assigned to that employee
        list_emp = {}
        create_dict={}
        list_child_ids=[]
        res = super(ProjectWorkitems, self).create(values)
        for child in res.child_ids:
            print(child.id)
            if(child.assigned_to not in list_emp):
                list_child_ids = []
                print("-----",list_child_ids)
                list_child_ids.append(child.id)
                list_emp[child.assigned_to] = {}
                create_dict = {
                    't_id': res.azure_id,
                    'emp_name': child.assigned_to,
                    # 'work_item_ids': list_child_ids
                }
                a = create_dict.get('emp_name')
                list_emp[a] = create_dict
            else:
                list_child_ids.append(child.id)
                # create_dict.update({'work_item_ids' :[6,0,[]]})
                a = create_dict.get('emp_name')
                list_emp[a] = create_dict
        print(list_emp)
        for rec in list_emp.values():
            print(rec)
            self.env['project.mytimesheet'].create(rec)




                # timesheet_values.update({'work_item_ids': list_child_ids})




            # if (values.get('assigned_to') not in list_emp):
            #     list_emp.append(values.get('assigned_to'))
            #     timesheet_values = {
            #         't_id':values.get('azure_id'),
            #         'emp_name':values.get('assigned_to'),
            #         'work_item_ids':values.get('child_ids')
            #     }
            #

            # for child_id in values.get('child_ids'):
            #
            # self.env['project.mytimesheet'].create(timesheet_values)
        return res

    #this is server action method to count hours of workitems:
    #it will do group by on empname and will create dict to store data in timesheet entries
    #group by functionality of sql in odoo
    def _make_timesheet_entry(self):
        data = self.env['project.myworkitem'].read_group([('assigned_to', '!=', "")], ['assigned_to','complete_work_hour','remaining_work_hour','original_estimate_hour'], ['assigned_to'])
        # print(data)
        result = dict((data['assigned_to'],
                        {   'complete_work_hour'    :data['complete_work_hour'],
                            'original_estimate_hour':data['original_estimate_hour'],
                            'remaining_work_hour'   :data['remaining_work_hour']
                        }) for data in data)
        print(result)

        # print('Server Action called')
        # all_record = self.env['project.myworkitem'].search([])
        # print(all_record)
        # for single_record in all_record:
        #     sum=0
        #     if(single_record.child_ids):
        #         for child in single_record.child_ids:
        #             print(child.azure_id,child.assigned_to,child.azure_id,child.complete_work_hour)
        #             sum+=child.complete_work_hour
        #         print('For',single_record.azure_id,single_record.assigned_to,'completed hour is',sum)


    my_compute_field = fields.Integer(
        string='compute field',compute='_compute_hours_',
        required=False)

    def _compute_hours_(self):
        print(self)
