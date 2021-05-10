from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    product_template_ids = fields.Many2many('product.template', string='Templates')

    @api.onchange('product_template_ids')
    def _onchange_product_template_ids(self):
        lines = [(5, 0, 0)]
        lines = []
        for template in self.product_template_ids:

            products = self.env['product.product'].search([('product_tmpl_id', '=', template._origin.id)])
            for product in products:
                values = {
                    'product_id': product.id,
                    'product_uom': template.uom_po_id.id,
                }
                lines.append((0, 0, values))
        self.update(dict(move_ids_without_package=lines))
