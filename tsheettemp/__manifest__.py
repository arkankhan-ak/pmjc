{
    'name': "Tsheet",
    'version': '1.0',
    'depends': ['base','account'],
    'author': "Arkankhan Pathan",
    
    'description': """
    This module is for temp understnding of project
    """,
    # data files always loaded at installation
    'data': [
        'views/forecast_output.xml',
        'views/forecast.xml',
        'views/invoice_view.xml',
        'views/expense.xml',
        'views/project_workitem.xml',
        'views/real_timesheet.xml'
    ],
        'installable': True,
        'application':True
}