from odoo import models, fields, api


class Bills(models.Model):
    _name = 'pos.session.history.bills'

    name = fields.Char(string='Name')
    value = fields.Float(string='Quantity')
    quantity = fields.Integer(string='Quantity')

    @api.depends('value', 'quantity')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.value * rec.quantity

    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal')

    session_id = fields.Many2one('pos.session.history')


class SessionCashHistory(models.Model):
    _name = 'pos.session.history'

    bills = fields.One2many('pos.session.history.bills', 'session_id')


class POSSession(models.Model):
    _inherit = 'pos.session'

    # def _compute_cash_box_start(self):
    #     for rec in self:
    #         previous_sessions = self.env['pos.session'].search([('config_id', '=', rec.config_id.id)], limit=2,
    #                                                            order='id desc')
    #         if len(previous_sessions) == 2:
    #             rec.cash_box_start = previous_sessions[-1].cash_register_id.cashbox_end_id.cashbox_lines_ids
    #         elif len(previous_sessions) == 1:
    #             rec.cash_box_start = False
    #         else:
    #             rec.cash_box_start = False

    # cash_box_start = fields.One2many('account.cashbox.line', compute='_compute_cash_box_start')
    cash_box_start = fields.One2many(related='cash_register_id.cashbox_start_id.cashbox_lines_ids', readonly=True)
    cash_box_end = fields.One2many(related='cash_register_id.cashbox_end_id.cashbox_lines_ids', readonly=True)
