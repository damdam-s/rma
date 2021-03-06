# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2015 Eezee-It, MONK Software
#    Copyright 2013 Camptocamp
#    Copyright 2009-2013 Akretion,
#    Author: Emmanuel Samyn, Raphaël Valyi, Sébastien Beau,
#            Benoît Guillot, Joel Grand-Guillaume, Leonardo Donelli
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    claim_id = fields.Many2one('crm.claim', string='Claim')

    @api.model
    def create(self, vals):
        if ('name' not in vals) or (vals.get('name') == '/'):
            vals['name'] = self.env['ir.sequence'].get(self._name)
        return super(StockPicking, self).create(vals)


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def create(self, vals):
        """
        In case of a wrong picking out, We need to create a new stock_move in a
        picking already open.
        To avoid having to confirm the stock_move, we override the create and
        confirm it at the creation only for this case.
        """
        move = super(StockMove, self).create(vals)
        if vals.get('picking_id'):
            picking = self.env['stock.picking'].browse(vals['picking_id'])
            if picking.claim_id and picking.picking_type_id.code == 'incoming':
                move.write({'state': 'confirmed'})
        return move
