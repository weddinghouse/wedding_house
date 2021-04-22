# -*- coding: utf-8 -*-
{
    'name': 'Wedding House',
    'description': 'Wedding House Technical Modifications',
    'version': '0.0.1',
    'author': 'EffVision',
    'category': 'POS',

    'depends': ['stock', 'purchase', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/product_data.xml',
        'views/product.xml',
    ],
    'application': True,
}
