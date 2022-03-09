# -*- coding: utf-8 -*-
{
    'name': "My Library",

    'summary': "Manage books easily",
     #summary:Short (1 phrase/line) summary of the module's purpose, used as
     #subtitle on modules listing or apps.openerp.com"""

    'description': """
         Manage Library
         ==============
         Description related to library.
    """,
    #description:Long description of module's purpose

    'author': "Tahwol Co.",
    'website': "https://www.tahawol.co",

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
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_member_views.xml',
        'views/library_book.xml',
        'views/library_book_categ_views.xml',
        'views/library_book_menus.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'application': True,
}
