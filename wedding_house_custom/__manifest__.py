# -*- coding: utf-8 -*-
{
    'name': 'Wedding House',
    'description': 'Wedding House Technical Modifications',
    'version': '0.0.1',
    'author': 'EffVision',
    'category': 'POS',

    'depends': ['stock', 'hr', 'purchase', 'point_of_sale', 'purchase_product_matrix', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'report/stock_report_view.xml',
        'templates/templates.xml',
        'reports/delivery_receipt.xml',
        'data/product_data.xml',
        'wizard/template_wizard.xml',
        # 'views/assets.xml',
        'views/hr_employee.xml',
        'views/pos_order.xml',
        'views/purchase_order.xml',
        'views/product.xml',
        'views/stock_picking.xml',
        'views/pos_session.xml',
        'views/stock_reports.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'wedding_house_custom/static/src/js/models.js',
            'wedding_house_custom/static/src/js/Screens/PaymentScreen/PaymentScreen.js',
        ],
        'web.assets_qweb': [
            'wedding_house_custom/static/src/xml/Screens/ReceiptScreen/OrderReceipt.xml',
            'wedding_house_custom/static/src/xml/Screens/PaymentScreen/PaymentScreen.xml',
        ],
    },
    'application': True,
}
