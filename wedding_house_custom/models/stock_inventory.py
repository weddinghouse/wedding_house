from odoo import models, fields, api


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    product_default_code = fields.Char(related='product_id.default_code')
    product_type = fields.Selection(related='product_id.product_tmpl_id.product_textile_type')
    product_barcode = fields.Char(related='product_id.barcode')


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
