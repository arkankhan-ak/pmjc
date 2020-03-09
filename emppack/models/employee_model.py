# -*- coding: utf-8 -*-
from asyncore import file_dispatcher

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
from logging import _loggerClass
import types
from functools import reduce
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as obtained_system_date_format

class InheritedSaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    is_discount_allow = fields.Boolean(default=False)

    @api.model
    def create(self,vals):
        if(vals.get("order_id")):
            current_sale_order = self.env['sale.order'].search([('id', '=', vals.get("order_id"))])
            vals.update({"is_discount_allow":current_sale_order.partner_id.is_discount_allow})
        return super(InheritedSaleOrderLine, self).create(vals)


    #it will check if price is > 100 and if it is it will deduct 100 and if not it won't perfoorm any action on it 
    # @api.onchange('is_discount_allow')
    # def _calculate_price_(self):
    #     print("-----PRICE SUBTOT BEFORE-------->")
    #     if(self.is_discount_allow):
    #         if(self.price_subtotal > 100):
    #             self.price_subtotal = self.price_subtotal - 100
    #     if(not self.is_discount_allow and self.price_subtotal > 100):
    #             self.price_subtotal = self.price_subtotal + 100
                
    #     print("-----PRICE SUBTOT AFTER-------->",self.price_subtotal)
    
    
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id','is_discount_allow')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if(line.is_discount_allow and line.price_subtotal > 100):
                line.price_subtotal = line.price_subtotal - 100


class CustomResPartner(models.Model):
    _inherit = 'res.partner'
    is_discount_allow = fields.Boolean("Allow Discount :")

class CustomSalesOrder(models.Model):
    _inherit = 'sale.order'
    
    c_street = fields.Char(string="street",compute="_compute_customer_address_")
    c_street2 = fields.Char(string="Street 2",compute="_compute_customer_address_")
    c_city = fields.Char(string="City",compute="_compute_customer_address_")
    c_state = fields.Char(string="State",compute="_compute_customer_address_")
    c_country = fields.Char(string="Country",compute="_compute_customer_address_")
    c_zip = fields.Integer(string="Zip Code",compute="_compute_customer_address_")

    #it will override create method of sale.order and fetch flag of discount from res.partner and set it in all order line 
    # @api.model
    # def create(self, vals):
    #     if(vals.get("partner_id")):
    #         p_id = self.env['res.partner'].search([('id', '=', vals.get("partner_id"))])
    #         for order_line in vals.get('order_line'):
    #             order_line[2]['is_discount_allow'] = p_id.is_discount_allow
    #         result = super(CustomSalesOrder, self).create(vals)
    #         return result
    
    @api.multi
    def _compute_customer_address_(self):
        for order in self:
            current_customer = order.env['res.partner'].search([('id', '=', order.partner_id.id)])
            order.c_street = str(current_customer.street)
            order.c_street2 = str(current_customer.street2)
            order.c_city = str(current_customer.city)
            order.c_state = str(current_customer.state_id.name)
            order.c_zip = str(current_customer.zip)
            order.c_country = str(current_customer.country_id.name)

class EmployeeModel(models.Model):
    _name = 'employee.detail'
    _description = 'Employee information'
    _rec_name = 'first_name'
    _inherit = 'mail.thread'

    user_list = fields.Many2one('res.users',string="Users",default=lambda self: self.env.user)
    country = fields.Char(string="user's country",compute="_compute_user_country_")
    wage = fields.Float(string="Wage")
    profile_pic = fields.Binary(string="Profile pic",track_visibility="always")
    first_name = fields.Char(string="First name",required=True)
    last_name = fields.Char(string="Last name",required=True)
    middle_name = fields.Char(string="Middle name")
    dob =  fields.Date()
    status = fields.Selection([('draft','Draft'),('interview_one','Interview one'),('interview_two','Interview two'),('hired','Hired'),('enrolled','enrolled')],string="Status")
    contact_number = fields.Char(string="contact number",required=True)
    date_of_joining =  fields.Date()
    wages_type = fields.Selection([('salary', 'Salary'),('hour','Hour')],string="wages type", default='salary')
    Wages_or_salary = fields.Selection([('wages', 'Wages'),('salary','Salary')],default='salary')
    gender = fields.Selection([('male','Male'), ('felame','Female')],default='male')
    hobbies = fields.Many2many('employee.hobby','rel_employee_hobby','first_name','name',string="Hobbies")
    job_position = fields.Many2one('employee.jobposition',string="Job Position")
    certificate = fields.One2many('employee.certificate',inverse_name="employee_id",string="certificate")
    guardian_ids = fields.Many2many('guardian.detail','rel_employee_guardian','first_name','name',string="Guardians")
    first_guardian_address = fields.Char(compute="_compute_guardian_address_",string="First Guradian Address")
    second_guardian_address = fields.Char(compute="_compute_guardian_address_",string="Second Guardian Address")

    

    @api.multi
    def _compute_user_country_(self):
        for record in self:
            record.country = record.user_list.country_id.name
    #will compute guardian address for first 2 guardian of employee
    @api.multi
    @api.depends('guardian_ids')
    def _compute_guardian_address_(self):
        for record in self:
            if(len(record.guardian_ids)>0):
                record.first_guardian_address = record.guardian_ids[0].street + ',' + record.guardian_ids[0].street2 + ',' + record.guardian_ids[0].city + ',' + record.guardian_ids[0].state + ',' + record.guardian_ids[0].country + ',' + str(record.guardian_ids[0].zipcode )
            if(len(record.guardian_ids)>1):
                record.second_guardian_address = record.guardian_ids[1].street + ',' + record.guardian_ids[1].street2 + ',' + record.guardian_ids[1].city + ',' + record.guardian_ids[1].state + ',' + record.guardian_ids[1].country + ',' + str(record.guardian_ids[1].zipcode )

    toggle_active = fields.Boolean(default=True)
    
    # computed field
    computed_name = fields.Char(compute='_compute_name_')

    alise_name = fields.Char()
    

    #short_code
    short_code = fields.Char(compute='_compute_short_code_',store=True)

    hobby_code = fields.Char()

    matching_hobbies = fields.Many2one("employee.hobby")



    @api.multi
    @api.depends('first_name','middle_name','last_name')
    def _compute_name_(self):
        print("-- in compute field --- ")
        for record in self:
            print("----record------->",record)
            record.computed_name =str(record.first_name)+' '+str(record.middle_name)+' '+str(record.last_name)
            # record.alise_name = record.computed_name

    
    docs_count = fields.Integer(compute="_compute_doc_count_",track_visibility="always")

    archive_certificate_count = fields.Integer(compute="_compute_archive_certificate_count_")

    @api.onchange('first_name','middle_name','last_name')
    def _compute_onchange_(self):
        self.computed_name =str(self.first_name)+' '+str(self.middle_name)+' '+str(self.last_name)
        self.alise_name = self.computed_name
    
    @api.multi
    @api.depends('first_name','middle_name','last_name')
    def _compute_short_code_(self):
        print("-------------)came in compute short code(----------------")
        for record in self:
            temp_str = ""
            if(not isinstance(record.first_name,bool)):
                temp_str += str(record.first_name)
            if(not isinstance(record.middle_name,bool)):
                temp_str += str(record.middle_name)
            if(not isinstance(record.last_name,bool)):
                temp_str += str(record.last_name)
            temp_str = temp_str.replace(' ', '')
            record.short_code = temp_str[0:8].upper()

    # get only that hobby whose code is entered by employee on form view
    @api.onchange('hobby_code')
    def _compute_hobby_tags_(self):
        cur_hobby_id = None
        all_hobbies = self.env['employee.hobby'].search([])
        for h in all_hobbies:
            if(h.h_code == self.hobby_code):
                # self.matching_hobbies = h.id
                cur_hobby_id = h.id
                return {
                'domain':{
                    'matching_hobbies':[('id','=',cur_hobby_id)]
                    }
                }

    #on change of booelan button record
    def toggle_start(self):
        if(self.toggle_active == True):
            self.toggle_active = False
            self.matching_hobbies = None
        elif(self.toggle_active == False):
            self.toggle_active = True
            all_hobbies = self.env['employee.hobby'].search([])
            for h in all_hobbies:
                if(h.h_code == self.hobby_code):
                    self.matching_hobbies = h.id
    #tocount total no of document
    @api.multi
    def _compute_doc_count_(self):
        for record in self:
            record.docs_count = record.env['employee.certificate'].search_count([('employee_id', '=', record.id)])
    
    @api.multi
    def _compute_archive_certificate_count_(self):
        for record in self:
            record.archive_certificate_count = self.env['employee.certificate'].search_count([('active', '=', False),('employee_id', '=', self.id)])

    # @api.multi
    # @api.depends('hobbies')
    # def _compute_hobby_code_(self):
    #     for record in self:
    #         for hobby_object in record.hobbies:
    #             print("------hex code--->",hobby_object.name)
    #             print("-->",self.generate_hobby_code(hobby_object.name))


    #method to calculate hobby code
    def generate_hobby_code(self,hobby_name):
        #below line will generate ascii of each chars (of hobby name string) and will do sum of all asci values and will convert it into string and store that value  in generated code
        genrated_code = str(reduce(lambda a,b: a +b ,list(map(ord,hobby_name))))
        if(len(genrated_code)<3):
            genrated_code = "0" + genrated_code
        return genrated_code[0:3]


        
    #remaining with functionality of date if user change date format from setting it will give error 
    #or it will misbehave that functionality
    @api.model
    def create(self,values):
        #dob validation 
        date_of_birth = values.get("dob")
        is_object_has_required_info = False
        if date_of_birth:
            current_date = datetime.today()
            comparing_date = datetime.strptime(date_of_birth,obtained_system_date_format)
            if(comparing_date>=current_date):
                print("You can't adddddddd")
                is_object_has_required_info =False
                raise ValidationError(_('Enter date less than today"s date was %s'%date_of_birth))
            else:
                is_object_has_required_info = True
        else:
            is_object_has_required_info =False
            raise ValidationError(_('Enter date of Birth Please'))


        if(values.get("job_position")):
            print("------------------>came here")
            job_id = self.env['employee.jobposition'].search([("id","=",values.get("job_position"))])
            wage = job_id.job_category_id.wages
            print("####################",wage)
            print("#########certificate###########",values.get("certificate"))
            values.update({'wage':wage})
            is_object_has_required_info = True
            
        else:
            is_object_has_required_info = False
            raise ValidationError(_('Select Job Position Please'))

        if(is_object_has_required_info):
            res = super(EmployeeModel,self).create(values)
            # print("----------------------->",Certificate.all_certificates)
            for i in Certificate.all_certificates:
                # auto creation of certificate
                self.env['employee.certificate'].create({
                    "c_type":i[0],
                    "employee_id": res.id
                    })
        else:
            raise ValidationError(_('Problem in DOB and Job Validation Provide appropriate info'))
        return res
    @api.multi
    def write(self,values):
        for record in self:
            if(values.get("job_position")):
                job_id = record.env['employee.jobposition'].search([("job_category_id","=",values.get("job_position"))])
                wage = job_id.job_category_id.wages
                values.update({'wage':wage})
            else:
                print("else stat called")
            res = super(EmployeeModel,self).write(values)
            return res

    @api.multi
    def unlink(self):
        item_certificate = self.env['employee.certificate'].search([('employee_id','in',self.ids)])
        # print("Iteeeeeeeeeeeeeeeem : ",item_certificate)
        item_certificate.unlink()
        # self.env['employee.certificate'].unlink(item_certificate.id)
        return super(EmployeeModel, self).unlink()

class Certificate(models.Model):
    _name = 'employee.certificate'
    _rec_name = 'employee_id'
    certificate = fields.Binary(string="certificate")
    all_certificates = [('10','10th Marksheet'),('12','12th Marksheet'),('g','Graduation certificate'), ('p','ID Card')]
    c_type = fields.Selection(all_certificates,string="Type")
    employee_id = fields.Many2one('employee.detail',string="Employee Detail")
    active = fields.Boolean(default=True)

class JobPosition(models.Model):
    _name = 'employee.jobposition'
    _description = 'Employee Job Position'
    _rec_name = 'job_position_name'

    job_position_name = fields.Char(string="job_position_name",required=True)
    sequence = fields.Integer(string="sequence",default=1)
    job_category_id = fields.Many2one("category.detail",string="job_category_id")

    @api.model
    def create(self,values):
        last_record = self.search([],order='sequence desc',limit=1)
        if last_record.sequence == 0:
            inserting_seq = last_record.sequence + 1
            values['sequence'] = inserting_seq 
        res = super(JobPosition,self).create(values)
        return res

class Hobbies(models.Model):
    _name = 'employee.hobby'

    name = fields.Char(string="name",required=True)
    is_selected = fields.Integer()

    h_code = fields.Char(compute="_c_h_code_")

    #method to calculate hobby code
    def generate_hobby_code(self,hobby_name):
        genrated_code = str(reduce(lambda a,b: a +b ,list(map(ord,hobby_name))))
        if(len(genrated_code)<3):
            genrated_code = "0" + genrated_code
        return genrated_code[0:3]

    @api.multi
    def _c_h_code_(self):
        for record in self:
            record.h_code = self.generate_hobby_code(record.name)

