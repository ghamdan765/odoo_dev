# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Real Estate',
    'description': "",
    'depends': [
        'base'
    ],
    'license': "AGPL-3",
# always loaded
    'data': [

        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'

    ],
    'application': True

}
