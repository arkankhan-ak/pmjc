{
    'name': "Aproject",
    'summary': """
        PROJECT MANAGMENT AND JOB COSTING  AT BIZNOVARE""",
    'description': """
        Long description of module's purpose 
    """,

    'author': "kevin",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
                'sale',
                'base',
                'web',
                'crm',
                'project'
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/groups.xml',
        'views/views.xml',
        'views/views_workitem.xml',
        'views/templates.xml',
        'widget/views/views.xml',
        'views/crone_job.xml',
        'views/my_timesheet.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application' : True,
    'installable' : True,
}
# -*- coding: utf-8 -*-
