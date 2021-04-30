from odoo import models, fields, api


class POSORder(models.Model):
    _inherit = 'pos.order'

    sales_person = fields.Many2one('hr.employee', string='Sales Person')
