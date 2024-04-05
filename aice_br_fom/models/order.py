# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

# Class for products
class FomProducts(models.Model):
    _name = "fom.products"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Freezer Product"
    
    #defining a sequence number for the name.
    name = fields.Char(string='Product Name', required=True)
    reference = fields.Char(string='Product Reference', readonly=True, default=lambda self: _('New Product'))

    @api.model
    def create(self, vals):
        if not vals.get('reference') or vals['reference'] == _('New Product'):
            sequence = self.env['ir.sequence'].next_by_code('fom.products') or _('New Product')
            vals['reference'] = sequence
        res = super(FomProducts, self).create(vals)
        return res
    order = fields.Integer(string="Order")

    # Going to the next item in the sequence
    def can_sell(self):
        self.state = 'sell'

    def cant_sell(self):
        self.state = 'not_sell'

    # Product name
    prod_name = fields.Char(string="Product Reference", required=True, copy=False, readonly=True, default=lambda self: _('New Product'))
    # Internal Reference
    vis_name = fields.Char(string="Product Name", required=True)
    # Price
    price = fields.Float(string="Sell Price", required=True)
    # Quantity
    qty_in_hands = fields.Integer(string="Quantity In Stock", required=True)
    # Created when ?
    created_when = fields.Datetime(string="Created When", readonly=True, default=fields.Datetime.now)

    # Array of status names.
    state = fields.Selection([
        ('sell', 'Can Sell'),
        ('not_sell', 'Cant Sell'),
        ], string='Status', default='sell', tracking=True)
 
# Class for the actual conponnent
class FomOrder(models.Model):
    _name = "fom.order"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Freezer Order Head"

    #defining a sequence number for the name.
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Order Created'
        if vals.get('name', _('New Order')) == _('New Order'):
            vals['name'] = self.env['ir.sequence'].next_by_code('fom.order') or _('New Order')
        res = super(FomOrder, self).create(vals)
        return res
    
    # Going to the next item in the sequence
    def jump_state(self):
        self.state = 'sent'

    # ------------ Cancel button start
    invoice_ids = fields.Many2many("account.move", string='Invoices', readonly=True, copy=False, search="_search_invoice_ids")
    def CancelState(self):
        cancel_warning = self._show_cancel_wizard()
        if cancel_warning:
            return {
                'name': _('Cancel Sales Order'),
                'view_mode': 'form',
                'res_model': 'sale.order.cancel',
                'view_id': self.env.ref('sale.sale_order_cancel_view_form').id,
                'type': 'ir.actions.act_window',
                'context': {'default_order_id': self.id},
                'target': 'new'
            }
        return self._action_cancel()

    def _action_cancel(self):
        inv = self.invoice_ids.filtered(lambda inv: inv.state == 'draft')
        inv.button_cancel()
        return self.write({'state': 'cancel'})
    
    def _show_cancel_wizard(self):
        for order in self:
            if order.invoice_ids.filtered(lambda inv: inv.state == 'draft') and not order._context.get('disable_cancel_warning'):
                return True
        return False
    # ------------ Cancel button end

    def toDraft(self):
        self.state = 'draft'
    
    # Name of the operation.
    name = fields.Char(string='Order ID', required=True, copy=False, readonly=True, default=lambda self: _('New Order'))

    # Order Types
    ordertype = fields.Many2one('fom.ordertype',string="Order Type", required=True, tracking=True)
    
    # Gets the actual date time from the server.
    dateorder = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)

    # Maket types
    markettype = fields.Many2one('fom.markettype',string="Market Type", required=True, tracking=True)

    # Gets the costumer array from db res.partner
    customer_id = fields.Many2one(
        'res.partner', string='Customer',
        required=True, change_default=True, index=True, tracking=True)
    note = fields.Text(string='Description')
    
    # Array of status names.
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('freezer_order', 'Freezer Order'),
        ('done', 'Locked'),
         ('cancel', 'Cancelled'),
        ], string='Status', default='draft', tracking=True)
   
    # Order line page
    order_line = fields.One2many('fom.order.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, tracking=True)
    
    # Monetary information.
    t_amt = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    untaxed_amount = fields.Float(string='Untaxed Amount', compute='_compute_untaxed_amount', store=True)
    amount_taxed = fields.Float(string='Amount Taxed', compute='_compute_amount_taxed', store=True)

    # Company
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, tracking=True)

    # Currency id
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=lambda self: self.env.company.currency_id.id)

    # Archive / Unarchive
    active = fields.Boolean(string='Active', default=True, tracking=True)

    @api.depends('order_line.subtotal')
    def _compute_untaxed_amount(self):
        for ordem in self:
            ordem.untaxed_amount = sum(ordem.order_line.mapped('subtotal'))

    @api.depends('order_line.subtotal', 'order_line.tax')
    def _compute_amount_taxed(self):
        for ordem in self:
            ordem.amount_taxed = sum(ordem.order_line.mapped('tax'))
            ordem.t_amt = ordem.untaxed_amount + ordem.amount_taxed

    # calculate te total with tax
    @api.depends('order_line.subtotal', 'amount_taxed')
    def _compute_total_amount(self):
        for ordem in self:
            ordem.t_amt = ordem.untaxed_amount + ordem.amount_taxed

    # Responsable to move the order to the inventory and creating a purchase order on the purchase module.
    def DoneState(self):
        # Responsable for changing the state of the order, once the function returns true.
        self.state = 'freezer_order'

        # Creating the purchase order parammeters.
        #purchase_order = self.env['purchase.order'].create({
        #    'partner_id': self.customer_id.id,
        #    'date_order': self.dateorder,
        #    'picking_type_id': 1,
        #    'company_id': self.company_id.id,
        #    'origin': self.name,
        #    'order_line': [(0, 0, {
        #        'name': line.product_id.name,
        #        'product_id': line.product_id.id,
        #        'product_qty': line.product_uom_qty,
        #        'product_uom': line.product_id.uom_id.id,
        #        'price_unit': line.price_unit,
        #        'taxes_id': [(6, 0, line.tax_id.ids)] if line.tax_id else False,
        #    }) for line in self.order_line],
        #})

        # Returns true.
        return True
    
    # Only show the orders from the company that saved the order.
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        company_ids = self.env.context.get('allowed_company_ids', [self.env.company.id])
        args += [('company_id', 'in', company_ids)]
        return super(FomOrder, self).search(args, offset, limit, order, count=count)
    
# Class responsable for The item list itself.
class FomOrderLine(models.Model):
    _name = 'fom.order.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Freezer Order Line'
    _check_company_auto = True

    # -- UNUSED
    qtytype = fields.Selection([
        ('dg', 'DG'),
        ('gtg', 'GTG'),
        ('pp', 'PP'),
        ('mf', 'MF'),
        ('mt', 'MT'),
    ], string="Market Type", required=True, default='dg', tracking=True)

    # Fields
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)], change_default=True, tracking=True)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0, tracking=True)
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0, tracking=True)
    order_id = fields.Many2one('fom.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store = True)
    tax_id = fields.Many2one('account.tax', string='Tax', tracking=True)
    tax = fields.Float(string='Tax', compute='_compute_tax', store=True)
    
    # Currency id
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=lambda self: self.env.company.currency_id.id)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    # Calculating the total
    @api.depends('tax_id', 'subtotal')
    def _compute_tax(self):
        for linha_pedido in self:
            linha_pedido.tax = linha_pedido.subtotal * (linha_pedido.tax_id.amount / 100) if linha_pedido.tax_id else 0.0
   
    # Getting the dependency
    @api.depends('product_uom_qty', 'price_unit', 'tax_id')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal =  line.product_uom_qty * line.price_unit 
        
    # Automatically getting field information o tree from
    @api.onchange('product_id')
    def set_code(self):
        self.price_unit = self.product_id.lst_price

    # Custom message
    def write(self, vals):
        super().write(vals)
        if set(vals) & set(self._get_tracked_fields()):
            self._track_changes(self.order_id)

    def _track_changes(self, field_to_track):
        if self.message_ids:
            message_id = field_to_track.message_post(body=f'<strong>{ self._description }:</strong> { self.display_name }').id
            trackings = self.env['mail.tracking.value'].sudo().search([('mail_message_id', '=', self.message_ids[0].id)])
            for tracking in trackings:
                tracking.copy({'mail_message_id': message_id})