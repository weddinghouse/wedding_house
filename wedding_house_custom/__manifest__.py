# -*- coding: utf-8 -*-
{
    'name': 'Wedding House',
    'description': 'Wedding House Technical Modifications',
    'version': '0.0.1',
    'author': 'EffVision',
    'category': 'POS',

    'depends': ['stock', 'hr', 'purchase', 'point_of_sale', 'purchase_product_matrix'],
    'data': [
        'security/ir.model.access.csv',
        'templates/templates.xml',
        'data/product_data.xml',
        'views/assets.xml',
        'views/hr_employee.xml',
        'views/pos_order.xml',
        'views/purchase_order.xml',
        'views/product.xml',
        'views/stock_inventory.xml',
        'views/pos_session.xml',
    ],
    'qweb': [
        'static/src/xml/Screens/ReceiptScreen/OrderReceipt.xml',
        'static/src/xml/Screens/PaymentScreen/PaymentScreen.xml',
    ],
    'application': True,
}
