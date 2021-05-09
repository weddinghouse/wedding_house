from odoo import models, fields, api, _


class Employee(models.Model):
    _inherit = 'hr.employee'

    is_sales_person = fields.Boolean(string='Sales Person', groups="hr.group_hr_user")

    pos_order_ids = fields.One2many('pos.order', 'sales_person', string='Orders', groups="hr.group_hr_user")

    @api.depends('pos_order_ids')
    def _compute_pos_order_count(self):
        for rec in self:
            rec.pos_order_count = len(rec.pos_order_ids)

    pos_order_count = fields.Integer(string='Orders', compute='_compute_pos_order_count', groups="hr.group_hr_user")

    def action_view_pos_order(self):
        return {
            'name': _('Orders'),
            'res_model': 'pos.order',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('point_of_sale.view_pos_order_tree_no_session_id').id, 'tree'),
                (self.env.ref('point_of_sale.view_pos_pos_form').id, 'form'),
            ],
            'type': 'ir.actions.act_window',
            'domain': [('sales_person', '=', self.id)],
        }
