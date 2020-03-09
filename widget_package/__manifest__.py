{
    'name': "WidgetExample",
    'version': '1.0',
    'depends': ['base'],
    'author': "Arkankhan Pathan",
    
    'description': """
    This module is for understaing widget usage
    """,
    # data files always loaded at installation
    'data': [
        'views/student_view.xml',
        'views/classroom_view.xml',
        'views/subject_view.xml',
        'views/hobby_view.xml',
        'views/menu.xml',
    ],
        'installable': True,
        'application':True
}