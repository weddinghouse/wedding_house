from odoo import models, fields, api


class TemplateWizardLines(models.TransientModel):
    _name = 'template.wizard.line'
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Integer(string='Quantity')


class TemplateWizard(models.TransientModel):
    _name = 'template.wizard'

    product_template_id = fields.Many2one('product.template', string='Template')
    line_ids = fields.Many2many('template.wizard.line')

    @api.onchange('product_template_id')
    def _onchange_product_template_id(self):
        product_list = [(5, 0, 0)]
        for product in self.product_template_id.product_variant_ids:
            product_list.append((0, 0, {'product_id': product.id, 'quantity': 0}))
        self.line_ids = product_list

    def action_confirm(self):
        stock_picking_id = self._context['stock_picking_id']
        stock_picking = self.env['stock.picking'].browse(stock_picking_id)
        print("Stock Picking ", stock_picking, stock_picking.immediate_transfer)
        lines = []
        total_quantity = 0
        if not stock_picking.immediate_transfer:
            for line in self.line_ids:
                total_quantity += line.quantity
                lines.append((0, 0, {
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'product_uom': line.product_id.uom_po_id.id,
                    'location_id': stock_picking.location_id,
                    'location_dest_id': stock_picking.location_dest_id,
                }))
            stock_picking.description_lines = [
                (0, 0, {'name': self.product_template_id.display_name, 'quantity': total_quantity})]
            stock_picking.update(dict(move_ids_without_package=lines))
        else:
            for line in self.line_ids:
                total_quantity += line.quantity
                if line.quantity:
                    lines.append((0, 0, {
                        'company_id': self.env.company.id,
                        'product_id': line.product_id.id,
                        'qty_done': line.quantity,
                        'product_uom_id': line.product_id.uom_po_id.id,
                        'location_id': stock_picking.location_id.id,
                        'location_dest_id': stock_picking.location_dest_id.id,
                    }))
            stock_picking.description_lines = [
                (0, 0, {'name': self.product_template_id.display_name, 'quantity': total_quantity})]
            stock_picking.update(dict(move_line_ids_without_package=lines))
