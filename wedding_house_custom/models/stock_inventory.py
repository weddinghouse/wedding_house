from odoo import models, fields, api


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    product_template_ids = fields.Many2many(
        'product.template', string='Templates', check_company=True,
        domain="[('type', '=', 'product'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="Specify Product Templates to focus your inventory on particular Products Templates.")

    @api.onchange('product_template_ids')
    def _onchange_product_template(self):
        products = []
        current_products = self.product_ids
        for template in self.product_template_ids:
            for product_id in template.product_variant_ids.ids:
                products.append(product_id)
        self.update(dict(product_ids=products))
