from odoo import models, fields, api


class POSOrder(models.Model):
    _inherit = 'pos.order'

    sales_person = fields.Many2one('hr.employee', string='Sales Person')


    @api.model
    def _order_fields(self, ui_order):
        print()
        print(ui_order)
        order_fields = super(POSOrder, self)._order_fields(ui_order)
        order_fields['sales_person'] = ui_order.get('sales_person')
        return order_fields