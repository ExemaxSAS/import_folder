# -*- coding: utf-8 -*-
{
    "name": "Carpeta de Importaciones",
    'version': '15.0',
    'author': "Exemax (Brenda Gauto) / Israel Perez - EXEMAX",
    'website': "http://www.exemax.com.ar",
    'category': 'Project',
    'version': '15.0.1',
    'depends': [
        'base',
        'project',
        'stock',
        'purchase',
        'account',
        'purchase_stock',
        # 'stock_landed_costs',
        'stock_account',
        #'project_enterprise',
    ],
    'installable': True,
    'license': 'AGPL-3',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/account_move_inherit.xml',
        'views/project_project_inherit.xml',
        'views/project_task_inherit.xml',
        'views/purchase_order_inherit.xml',
        'views/stock_views_inherit.xml',
    ]
}
