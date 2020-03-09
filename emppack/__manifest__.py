{
    'name': "Employee",
    'version': '1.0',
    'depends': ['base','sale','account','hr','product','point_of_sale'],
    'author': "Arkankhan Pathan",
    
    'description': """
    This module is for employee package
    """,
    # data files always loaded at installation
    'data': [
        'views/category_view.xml',
        'views/guardian_view.xml',
        'security/security.xml',
        'views/emp_view.xml',
        'views/inherit_view_action.xml',
        'security/ir.model.access.csv',
        
    ],
        'installable': True,
        'application':True
}