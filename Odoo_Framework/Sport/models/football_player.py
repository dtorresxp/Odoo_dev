from odoo import api, fields, models


class FootballPlayer(models.Model):
    _name = 'football.player'

    name = fields.Char(string='Name',
                       required='1')
    age = fields.Integer(string='Age',
                         required='1')
    address = fields.Char(string='Address')
    phone = fields.Char(string='Phone Number')
    clb_id = fields.Many2one(comodel_name='club',
                             string='Club')
    training_place_ids = fields.Many2many('training.places',
                                          string='Training Places')
    salary = fields.Float(string="Salary")
    tax = fields.Float(string='Personal Income Tax',
                       compute='tax_calculation',
                       store=True)
    state = fields.Selection(selection=[('free', 'Free'),
                                        ('payroll', 'Payroll')],
                             default='free', compute='_state_player', store=True)

    @api.depends('clb_id')
    def _state_player(self):
        if self.clb_id:
            self.state = 'payroll'
        else:
            self.state = 'free'

    @api.onchange('training_place_ids')
    def get_default_salary(self):
        if len(self.training_place_ids) > 1:
            self.salary = 15000000
        else:
            self.salary = 10000000

    @api.depends('salary')
    def tax_calculation(self):
        if self.salary > 10000000:
            self.tax = self.salary * 0.1

    @api.model
    def create(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()
        res = super(FootballPlayer, self).create(vals)
        return res

    def write(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()
        res = super(FootballPlayer, self).write(vals)
        return res
