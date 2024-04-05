# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

# Resource type Model
class FomResourceType(models.Model):
    _name='fom.resourcetype'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Resource Type Management Interface"

    # Name field
    name = fields.Char(string='Resource Code', required=True, copy=False, readonly=True, default=lambda self: _('New Resource Type'))

    # Generate unique identifier.
    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New Resource Type'):
            sequence = self.env['ir.sequence'].next_by_code('fom.resourcetype') or _('New Resource Type')
            vals['name'] = sequence
        res = super(FomResourceType, self).create(vals)
        return res

    # Code Field
    resource_type_name = fields.Char(string='Resorce Type Name', required=True, translate=True)

    # Parent Category field
    resource_type_parent_category = fields.Many2one('fom.resourcetype', string="Parent Category", required=False)

    # Status field
    active = fields.Boolean(string='Active', default=True, tracking=True)

    # Note
    remark = fields.Text(string="Remark")

    # Created time field
    created_time = fields.Datetime(string='Created Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)

    # Parent Category Custom Name.
    def name_get(self):
        result = []
        for rec in self:
            value = '[' + rec.name + '] ' + rec.resource_type_name
            result.append((rec.id, value))
        return result

# Resource model
class FomResource(models.Model):
    _name='fom.resource'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Resource Info Management Interface"

    # Name field
    name = fields.Char(string='Resource Info Code', required=True, copy=False, readonly=True, default=lambda self: _('New Resource Information'))

    # Generate unique identifier.
    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New Resource Information'):
            sequence = self.env['ir.sequence'].next_by_code('fom.resource') or _('New Resource Information')
            vals['name'] = sequence
        res = super(FomResource, self).create(vals)
        if 'last_modified_date' not in vals:
            res.update_last_modified_date()
        return res

    def write(self, vals):
        res = super(FomResource, self).write(vals)
        if 'last_modified_date' not in vals:
            self.update_last_modified_date()
        return res

    def update_last_modified_date(self):
        self.last_modified_date = fields.Datetime.now()

    # Resource Type List
    resource_type_id = fields.Many2one('fom.resourcetype', string="Resource Type", required=True)

    # Resource Name field
    resource_name = fields.Char(string='Resource Name', required=True, translate=True)

    # Distribuitor list
    distributor_id = fields.Many2one('res.partner', string="Distributor", required=True)

    # Status field
    active = fields.Boolean(string='Active', default=True, tracking=True)

    # Remark field
    remark = fields.Text(string="Remark")

    # Created time field
    created_time = fields.Datetime(string='Created Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
    last_modified_date = fields.Datetime(string='Modified Date', readonly=True)

# Store Type model
class FomStoreType(models.Model):
    _name='fom.storetype'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Store Type Interface"

    # Name field
    name = fields.Char(string='Store Type Code', required=True, copy=False, readonly=True, default=lambda self: _('New Store Type'))

    # Generate unique identifier.
    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New Store Type'):
            sequence = self.env['ir.sequence'].next_by_code('fom.storetype') or _('New Store Type')
            vals['name'] = sequence
        res = super(FomStoreType, self).create(vals)
        if 'last_modified_date' not in vals:
            res.update_last_modified_date()
        return res

    def write(self, vals):
        res = super(FomStoreType, self).write(vals)
        if 'last_modified_date' not in vals:
            self.update_last_modified_date()
        return res

    def update_last_modified_date(self):
        self.last_modified_date = fields.Datetime.now()

    # Name Field
    store_type_name = fields.Char(string='Store Type Name', required=True, translate=True)

    # Parent Category field
    store_type_parent_category = fields.Many2one('fom.storetype', string="Parent Category", required=False)

    # Status field
    active = fields.Boolean(string='Active', default=True, tracking=True)

    # Remark field
    remark = fields.Text(string="Remark")

    # Created time field
    created_time = fields.Datetime(string='Created Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
    last_modified_date = fields.Datetime(string='Modified Date', readonly=True)
    
    # Parent Category Custom Name.
    def name_get(self):
        result = []
        for rec in self:
            value = '[' + rec.name + '] ' + rec.store_type_name
            result.append((rec.id, value))
        return result

#Order Type Model
class FomOrderType(models.Model):
    _name='fom.ordertype'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Order Type Interface"

    # Name field
    name = fields.Char(string='Order Type Code', required=True, copy=False, readonly=True, default=lambda self: _('New Order Type'))

    # Generate unique identifier.
    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New Order Type'):
            sequence = self.env['ir.sequence'].next_by_code('fom.ordertype') or _('New Order Type')
            vals['name'] = sequence
        res = super(FomOrderType, self).create(vals)
        if 'last_modified_date' not in vals:
            res.update_last_modified_date()
        return res

    def write(self, vals):
        res = super(FomOrderType, self).write(vals)
        if 'last_modified_date' not in vals:
            self.update_last_modified_date()
        return res

    def update_last_modified_date(self):
        self.last_modified_date = fields.Datetime.now()

    # Name Field
    order_type_name = fields.Char(string='Order Type Name', required=True, translate=True)

    # Parent Category field
    order_type_parent_category = fields.Many2one('fom.ordertype', string="Parent Category", required=False)

    # Status field
    active = fields.Boolean(string='Active', default=True, tracking=True)

    # Remark field
    remark = fields.Text(string="Remark")

    # Created time field
    created_time = fields.Datetime(string='Created Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
    last_modified_date = fields.Datetime(string='Modified Date', readonly=True)
    
    # Parent Category Custom Name.
    def name_get(self):
        result = []
        for rec in self:
            value = '[' + rec.name + '] ' + rec.order_type_name
            result.append((rec.id, value))
        return result

# Store Type model
class FomMarketType(models.Model):
    _name='fom.markettype'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Market Type Interface"

    # Name field
    name = fields.Char(string='Market Type Code', required=True, copy=False, readonly=True, default=lambda self: _('New Market Type'))

    # Generate unique identifier.
    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New Market Type'):
            sequence = self.env['ir.sequence'].next_by_code('fom.markettype') or _('New Market Type')
            vals['name'] = sequence
        res = super(FomMarketType, self).create(vals)
        if 'last_modified_date' not in vals:
            res.update_last_modified_date()
        return res

    def write(self, vals):
        res = super(FomMarketType, self).write(vals)
        if 'last_modified_date' not in vals:
            self.update_last_modified_date()
        return res

    def update_last_modified_date(self):
        self.last_modified_date = fields.Datetime.now()

    # Name Field
    market_type_name = fields.Char(string='Market Type Name', required=True, translate=True)

    # Parent Category field
    market_type_parent_category = fields.Many2one('fom.markettype', string="Parent Category", required=False)

    # Status field
    active = fields.Boolean(string='Active', default=True, tracking=True)

    # Remark field
    remark = fields.Text(string="Remark")

    # Created time field
    created_time = fields.Datetime(string='Created Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
    last_modified_date = fields.Datetime(string='Modified Date', readonly=True)
    
    # Parent Category Custom Name.
    def name_get(self):
        result = []
        for rec in self:
            value = '[' + rec.name + '] ' + rec.market_type_name
            result.append((rec.id, value))
        return result

# Terminal Model
class FomTerminalMgmt(models.Model):
    _name='fom.terminal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Terminal Management Interface"

    # Name field
    name = fields.Char(string='Register Code', required=True, copy=False, readonly=True, default=lambda self: _('New Terminal Information'))

    # Generate unique identifier.
    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New Terminal Information'):
            sequence = self.env['ir.sequence'].next_by_code('fom.terminal') or _('New Terminal Information')
            vals['name'] = sequence
        res = super(FomTerminalMgmt, self).create(vals)
        if 'last_modified_date' not in vals:
            res.update_last_modified_date()
        return res

    def write(self, vals):
        res = super(FomTerminalMgmt, self).write(vals)
        if 'last_modified_date' not in vals:
            self.update_last_modified_date()
        return res

    def update_last_modified_date(self):
        self.last_modified_date = fields.Datetime.now()

    # Store name
    store_name = fields.Char(string='Store Name', required=True, translate=True)

    # Distribuitor
    distributor = fields.Many2one('res.partner', string='Distributor', required=True)

    # Store Type
    store_type = fields.Many2one('fom.storetype', string='Store Type', required=True)

    # Storekeeper
    store_keeper = fields.Char(string='Storekeeper', required=True)

    # Phone number
    phone_number = fields.Char(string='Phone Number', required=True,  widget="phone", options="{'mask': '+55 (99) 99999-9999'}")

    # Put Address
    put_address = fields.Char(string='Put Address', required=True)

    # Country
    country = fields.Char(string='Country', required=True)

    # State of
    country_state = fields.Char(string='State of', required=True)

    # City
    city = fields.Char(string='City', required=True)

    # Street Adress
    street_address = fields.Char(string='Street Address', required=True)

    # Longitude
    longitude = fields.Char(string='Longitude')

    # Longitude
    latitude = fields.Char(string='Latitude')

    # Created time field
    created_time = fields.Datetime(string='Created Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
    last_modified_date = fields.Datetime(string='Modified Date', readonly=True)

    # Adding breazilian phone mask
    def formatar_telefone(self):
        if self.telefone:
            # Displays like : +55 (XX) XXXX-XXXX
            phone_mask = "+55 ({}) {}-{}".format(
                self.phone_number[:2],
                self.phone_number[2:6],
                self.phone_number[6:]
            )
            return phone_mask
        return False


# Takeback Model
class FomTakeBack(models.Model):
    _name='fom.takeback'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Takeback Interface"

    # Name field
    name = fields.Char(string='Takeback Code', required=True, copy=False, readonly=True, default=lambda self: _('New Takeback'))

    # Generate unique identifier.
    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New Takeback'):
            sequence = self.env['ir.sequence'].next_by_code('fom.takeback') or _('New Takeback')
            vals['name'] = sequence
        res = super(FomTakeBack, self).create(vals)
        if 'last_modified_date' not in vals:
            res.update_last_modified_date()
        return res

    def write(self, vals):
        res = super(FomTakeBack, self).write(vals)
        if 'last_modified_date' not in vals:
            self.update_last_modified_date()
        return res

    def update_last_modified_date(self):
        self.last_modified_date = fields.Datetime.now()


    # Takeback name
    takeback_name = fields.Char(string='Takeback Name', required=True, translate=True)

    # Takeback reason
    takeback_reason = fields.Text(string='Takeback Description', tracking=True)

    # Status field
    active = fields.Boolean(string='Active', default=True, tracking=True)

    # Created time field
    created_time = fields.Datetime(string='Created Date', required=True, readonly=True, index=True, copy=False, default=fields.Datetime.now)
    last_modified_date = fields.Datetime(string='Modified Date', readonly=True)


