from odoo import fields, models, api
from random import randrange
from itertools import zip_longest


class ProductCategory(models.Model):
    _inherit = 'product.category'

    barcode_prefix = fields.Char(string='Barcode Prefix', size=2)
    sequence_id = fields.Many2one(comodel_name='ir.sequence', copy=False)


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    @api.depends('sequence')
    def _compute_barcode_key(self):
        for rec in self:
            rec.barcode_key = str(rec.sequence).zfill(2)

    barcode_key = fields.Char(string='Barcode Key', size=2, compute='_compute_barcode_key')


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    barcode_sequence = fields.Integer(string='Barcode Sequence')
    print_name = fields.Char(string='Print Name', required=True, translate=True)


class ProductPattern(models.Model):
    _name = 'product.template.pattern'

    name = fields.Char(string='Name', translate=True)


class ProductBreastType(models.Model):
    _name = 'product.template.breast.type'

    name = fields.Char(string='Name', translate=True)


class ProductFit(models.Model):
    _name = 'product.template.fit'

    name = fields.Char(string='Name', translate=True)


class ProductLapelType(models.Model):
    _name = 'product.template.lapel.type'

    name = fields.Char(string='Name', translate=True)


class ProductLapelSize(models.Model):
    _name = 'product.template.lapel.size'

    name = fields.Char(string='Name', translate=True)


class ProductPocketType(models.Model):
    _name = 'product.template.pocket.type'

    name = fields.Char(string='Name', translate=True)


class ProductSleeveButton(models.Model):
    _name = 'product.template.sleeve.button'

    name = fields.Char(string='Name', translate=True)


class ProductSleeveButtonStyle(models.Model):
    _name = 'product.template.sleeve.button.style'

    name = fields.Char(string='Name', translate=True)


class ProductVentType(models.Model):
    _name = 'product.template.vent.type'

    name = fields.Char(string='Name', translate=True)


class ProductCollarType(models.Model):
    _name = 'product.template.collar.type'

    name = fields.Char(string='Name', translate=True)


class ProductCuffsType(models.Model):
    _name = 'product.template.cuffs.type'

    name = fields.Char(string='Name', translate=True)


class ProductShoesClosureType(models.Model):
    _name = 'product.template.shoes.closure.type'

    name = fields.Char(string='Name', translate=True)


class ProductShoesStyle(models.Model):
    _name = 'product.template.shoes.style'

    name = fields.Char(string='Name', translate=True)


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _rec_name = 'complete_name'

    @api.depends('default_code', 'name')
    def _compute_complete_name(self):
        for template in self:
            template.complete_name = f'[{template.default_code}] {template.name}'

    complete_name = fields.Char(string='Complete Name', compute='_compute_complete_name', store=True)

    internal_code = fields.Char(string='Internal Code', copy=False)

    @api.onchange('categ_id', 'categ_id.name')
    def _onchange_category(self):
        self.name = self.categ_id.name

    @api.model
    def create(self, vals):
        if 'categ_id' in vals:
            category = self.env['product.category'].browse(vals['categ_id'])
            code = category.sequence_id._next()
            prefix = category.barcode_prefix
            vals['default_code'] = str(prefix or 00) + str(code).zfill(7)
            vals['internal_code'] = code.zfill(7)
        template = super(ProductTemplate, self).create(vals)
        return template

    def write(self, vals):
        print(vals)
        if 'categ_id' in vals:
            category = self.env['product.category'].browse(vals['categ_id'])
            vals['internal_code'] = category.sequence_id._next().zfill(7)

        if 'internal_code' in vals:
            category = self.env['product.category'].browse(vals['categ_id'])
            vals['default_code'] = category.barcode_prefix + vals['internal_code']

        if 'default_code' in vals:
            vals['barcode'] = vals['default_code'] + '0' * 4

        res = super(ProductTemplate, self).write(vals)

    @api.onchange('product_textile_type')
    def _onchange_product_textile_type(self):
        if self.product_textile_type in ['suit', 'blazer']:
            self.collar_type_id = False
            self.cuffs_type_id = False
            self.shoes_closure_type_id = False
            self.shoes_style_id = False
        elif self.product_textile_type == 'shirt':
            self.breast_type_id = False
            self.lapel_button_hole = False
            self.lapel_type_id = False
            self.lapel_size_id = False
            self.pocket_type_id = False
            self.sleeve_button_id = False
            self.sleeve_button_style_id = False
            self.shoes_closure_type_id = False
            self.shoes_style_id = False
        elif self.product_textile_type == 'shoes':
            self.pattern_id = False
            self.breast_type_id = False
            self.fit_id = False
            self.lapel_button_hole = False
            self.lapel_type_id = False
            self.lapel_size_id = False
            self.pocket_type_id = False
            self.sleeve_button_id = False
            self.sleeve_button_style_id = False
            self.vent_type_id = False
            self.collar_type_id = False
            self.cuffs_type_id = False
        else:
            self.pattern_id = False
            self.breast_type_id = False
            self.fit_id = False
            self.lapel_button_hole = False
            self.lapel_type_id = False
            self.lapel_size_id = False
            self.pocket_type_id = False
            self.sleeve_button_id = False
            self.sleeve_button_style_id = False
            self.vent_type_id = False
            self.collar_type_id = False
            self.cuffs_type_id = False
            self.shoes_closure_type_id = False
            self.shoes_style_id = False

    product_textile_type = fields.Selection([
        ('suit', 'Suit'),
        ('blazer', 'Blazer'),
        ('shirt', 'Shirt'),
        ('shoes', 'Shoes'),
    ], string='Product Type')

    is_base_template = fields.Boolean(string='Base Template', default=False, copy=False)
    # Suits
    pattern_id = fields.Many2one('product.template.pattern', string='Pattern')  # Common between shirts and suits
    breast_type_id = fields.Many2one('product.template.breast.type', string='Breast Type')
    fit_id = fields.Many2one('product.template.fit', string='Fit')  # Common between shirts and suits
    lapel_button_hole = fields.Boolean(string='Lapel Button Hole')
    lapel_type_id = fields.Many2one('product.template.lapel.type', string='Lapel Type')
    lapel_size_id = fields.Many2one('product.template.lapel.size', string='Lapel Size')
    pocket_type_id = fields.Many2one('product.template.pocket.type', string='Pocket Type')
    sleeve_button_id = fields.Many2one('product.template.sleeve.button', string='Sleeve Buttons')
    sleeve_button_style_id = fields.Many2one('product.template.sleeve.button.style', string='Sleeve Button Style')
    vent_type_id = fields.Many2one('product.template.vent.type', string='Vent Type')
    # Shirts
    collar_type_id = fields.Many2one('product.template.collar.type', string='Collar Type')
    cuffs_type_id = fields.Many2one('product.template.cuffs.type', string='Cuffs Type')
    # Shoes
    shoes_closure_type_id = fields.Many2one('product.template.shoes.closure.type', string='Shoes Closure Type')
    shoes_style_id = fields.Many2one('product.template.shoes.style', string='Shoes Style')

    variant_standard_price = fields.Float('Variant Cost', digits='Product Price', groups="base.group_user")


class Product(models.Model):
    _inherit = 'product.product'

    def generate_barcode(self):
        prefix = self.product_tmpl_id.categ_id.barcode_prefix or '00'
        if self.product_tmpl_id.internal_code:
            infix = self.product_tmpl_id.internal_code
        else:
            infix = '0' * 7
        postfix = []
        attributes = []
        for av in self.product_template_attribute_value_ids:
            attributes.append({
                'sequence': av.attribute_id.barcode_sequence or 0,
                'key': av.product_attribute_value_id.barcode_key or '00',
            })
        attributes_sorted = sorted(attributes, key=lambda x: x['sequence'])
        for i, v in zip_longest(range(2), attributes_sorted, fillvalue=False):
            if i > 2: break
            if v:
                postfix.append(v['key'])
            else:
                postfix.append('00')
        barcode = prefix + infix + ''.join([v for v in postfix])
        self.barcode = barcode

    @api.model_create_multi
    def create(self, values):
        products = super(Product, self).create(values)
        for product in products:
            if not product.barcode:
                product.generate_barcode()
        return products

    @api.depends('product_tmpl_id.variant_standard_price')
    def _compute_variant_cost_price(self):
        for rec in self:
            rec.standard_price = rec.product_tmpl_id.variant_standard_price

    standard_price = fields.Float(
        'Cost', company_dependent=True,
        digits='Product Price',
        groups="base.group_user",
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
            In FIFO: value of the last unit that left the stock (automatically computed).
            Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
            Used to compute margins on sale orders.""",
        compute='_compute_variant_cost_price',
        readonly=False,
    )
