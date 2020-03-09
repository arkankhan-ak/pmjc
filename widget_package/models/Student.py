from odoo import api, fields, models, _
class Student(models.Model):
    _name = 'student.details'
    _rec_name = 'name'
    _description = 'Model decribing student information'

    # studentYearStatus = fields.Selection([('fy','First year'),('sy','Second year'),('ty','Third year')])
    name = fields.Char(string = "Student name")
    behaviourRating = fields.Float("Rating")
    rollNumber = fields.Integer("Roll number")
    status = fields.Selection([('1','First'),('2','Second'),('3','Third'),('4','Fourth')],string="Status")
    classroom_id = fields.Many2one("classroom.details",string="Classroom")
    subject_ids = fields.Many2many("subject.details","rel_suject_student","subject_name","name",string="Subjects")
    monthly_progres = fields.Float("Student Progress")
    seq = fields.Integer("sequence")
    gender = fields.Selection([('1','Male'),('2','Female')],string="Gender")
    average_present_time = fields.Float("Avg Present time")
    student_profile_pic = fields.Binary('Student Image')
    student_email = fields.Char('student_email')
    student_phone = fields.Char('student phone no')
    student_website = fields.Char('website')
    dob = fields.Date('dob')
    your_code = fields.Char('HTML snippet')
    is_active_student = fields.Boolean('is Active')
    