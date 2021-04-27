from odoo import api, models, _
from odoo.exceptions import ValidationError
import json
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

'''
This is too ugly
Need to improve this further
'''

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        if not self.product_id:
            return
        params = {'order_id': self.order_id}
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order.date(),
            uom_id=self.product_uom,
            params=params)

        if seller or not self.date_planned:
            self.date_planned = self._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        # If not seller, use the standard price. It needs a proper currency conversion.
        if not seller:
            if self.product_id.product_tmpl_id.variant_standard_price:
                standard_price = self.product_id.product_tmpl_id.variant_standard_price
            else:
                standard_price = self.product_id.standard_price
            price_unit = self.env['account.tax']._fix_tax_included_price_company(
                self.product_id.uom_id._compute_price(standard_price, self.product_id.uom_po_id),
                self.product_id.supplier_taxes_id,
                self.taxes_id,
                self.company_id,
            )
            if price_unit and self.order_id.currency_id and self.order_id.company_id.currency_id != self.order_id.currency_id:
                price_unit = self.order_id.company_id.currency_id._convert(
                    price_unit,
                    self.order_id.currency_id,
                    self.order_id.company_id,
                    self.date_order or fields.Date.today(),
                    )
            self.price_unit = price_unit
            return

        price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price, self.product_id.supplier_taxes_id, self.taxes_id, self.company_id) if seller else 0.0
        if price_unit and seller and self.order_id.currency_id and seller.currency_id != self.order_id.currency_id:
            price_unit = seller.currency_id._convert(
                price_unit, self.order_id.currency_id, self.order_id.company_id, self.date_order or fields.Date.today())

        if seller and self.product_uom and seller.product_uom != self.product_uom:
            price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

        self.price_unit = price_unit


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('grid')
    def _apply_grid(self):
        if self.grid and self.grid_update:
            grid = json.loads(self.grid)
            product_template = self.env['product.template'].browse(grid['product_template_id'])
            dirty_cells = grid['changes']
            Attrib = self.env['product.template.attribute.value']
            default_po_line_vals = {}
            new_lines = []
            for cell in dirty_cells:
                combination = Attrib.browse(cell['ptav_ids'])
                no_variant_attribute_values = combination - combination._without_no_variant_attributes()

                # create or find product variant from combination
                product = product_template._create_product_variant(combination)
                # TODO replace the check on product_id by a first check on the ptavs and pnavs?
                # and only create/require variant after no line has been found ???
                order_lines = self.order_line.filtered(lambda line: (line._origin or line).product_id == product and (
                            line._origin or line).product_no_variant_attribute_value_ids == no_variant_attribute_values)

                # if product variant already exist in order lines
                old_qty = sum(order_lines.mapped('product_qty'))
                qty = cell['qty']
                diff = qty - old_qty
                if diff and order_lines:
                    if qty == 0:
                        if self.state in ['draft', 'sent']:
                            # Remove lines if qty was set to 0 in matrix
                            # only if PO state = draft/sent
                            self.order_line -= order_lines
                        else:
                            order_lines.update({'product_qty': 0.0})
                    else:
                        """
                        When there are multiple lines for same product and its quantity was changed in the matrix,
                        An error is raised.

                        A 'good' strategy would be to:
                            * Sets the quantity of the first found line to the cell value
                            * Remove the other lines.

                        But this would remove all business logic linked to the other lines...
                        Therefore, it only raises an Error for now.
                        """
                        if len(order_lines) > 1:
                            raise ValidationError(
                                _("You cannot change the quantity of a product present in multiple purchase lines."))
                        else:
                            order_lines[0].product_qty = qty
                            order_lines[0]._onchange_quantity()
                            # If we want to support multiple lines edition:
                            # removal of other lines.
                            # For now, an error is raised instead
                            # if len(order_lines) > 1:
                            #     # Remove 1+ lines
                            #     self.order_line -= order_lines[1:]
                elif diff:
                    if not default_po_line_vals:
                        OrderLine = self.env['purchase.order.line']
                        default_po_line_vals = OrderLine.default_get(OrderLine._fields.keys())
                    last_sequence = self.order_line[-1:].sequence
                    if last_sequence:
                        default_po_line_vals['sequence'] = last_sequence
                    new_lines.append((0, 0, dict(
                        default_po_line_vals,
                        product_id=product.id,
                        price_unit=product_template.variant_standard_price,
                        product_qty=qty,
                        product_no_variant_attribute_value_ids=no_variant_attribute_values.ids)
                                      ))
            if new_lines:
                res = False
                self.update(dict(order_line=new_lines))
                for line in self.order_line.filtered(lambda line: line.product_template_id == product_template):
                    res = line._product_id_change() or res
                    line._onchange_quantity()
                return res
