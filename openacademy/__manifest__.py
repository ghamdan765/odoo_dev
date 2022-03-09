# -*- coding: utf-8 -*-
{
    'name': "Open Academy",

        # Short (1 phrase/line) summary of the module's purpose, used as
        # subtitle on modules listing or apps.openerp.com
    'summary': """
        Manage courses easily
        """,


    # Long description of module's purpose
    'description': """
            Manage courses in our University
            ==============
             Description related to library.
       
        """,


    'author': "Ghamdan Alnaggar",
    'website': "https://www.ghamdan.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    'license': "AGPL-3",

    # always loaded
    'data': [

         'security/ir.model.access.csv',
         'views/course_view.xml',
         'views/session_views.xml',
         'views/partner_views.xml'
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo_course.xml',
        # 'demo/demo.xml',
    ],
    'application': True,
}
