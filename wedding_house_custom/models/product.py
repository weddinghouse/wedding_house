from odoo import fields, models, api
from random import  randrange
from itertools import zip_longest

class ProductCategory(models.Model):
    _inherit = 'product.category'

    barcode_prefix = fields.Char(string='Barcode Prefix', size=2)


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    barcode_key = fields.Char(string='Barcode Key', size=2)


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    barcode_sequence = fields.Integer(string='Barcode Sequence')


class ProductTemplate(models.Model):
    _inherit = 'product.template'


class Product(models.Model):
    _inherit = 'product.product'

    def generate_barcode(self):
        prefix = self.categ_id.barcode_prefix or '00'
        postfix = str(randrange(10 ** 4, 10 ** 5, 5))
        infix = []
        attributes = []
        for av in self.product_template_attribute_value_ids:
            attributes.append({
                'sequence': av.attribute_id.barcode_sequence or 0,
                'key': av.product_attribute_value_id.barcode_key or '00',
            })
        attributes_sorted = sorted(attributes, key=lambda x: x['sequence'])
        for i, v in zip_longest(range(3), attributes_sorted, fillvalue=False):
            if i > 3: break
            if v: infix.append(v['key'])
            else: infix.append('00')
        barcode = prefix + ''.join([v for v in infix]) + postfix
        self.barcode = barcode
