from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import re


# ABSTRACT USER

class User(models.AbstractModel):
    _name = 'uber.user'
    _description = 'Abstract User'

    name = fields.Char(required=True)
    phone = fields.Char(required=True)
    email = fields.Char(required=True)

    @api.constrains('name', 'email', 'phone')
    def _check_fields(self):
        for rec in self:

            # Name validation
            if rec.name:
                if rec.name.strip() == "":
                    raise ValidationError("Name cannot be empty!")
                if not re.match(r'^[A-Za-z\s]+$', rec.name):
                    raise ValidationError("Name must contain letters only!")

            # Email validation
            if rec.email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', rec.email):
                raise ValidationError("Invalid email format!")

            # Phone validation (11 digits)
            if rec.phone and not re.match(r'^\d{11}$', rec.phone):
                raise ValidationError("Phone must be exactly 11 digits!")

    def action_check_phone(self):
        for rec in self:
            if not re.match(r'^\d{11}$', rec.phone):
                raise ValidationError("Phone is NOT valid!")
            else:
                raise UserError("Phone is valid ✅")


# PASSENGER

class Passenger(models.Model):
    _name = 'uber.passenger'
    _inherit = 'uber.user'
    _description = 'Passenger'

    rides_ids = fields.One2many('uber.ride', 'passenger_id')
    ride_count = fields.Integer(compute="_compute_ride_count")

    def _compute_ride_count(self):
        for rec in self:
            rec.ride_count = len(rec.rides_ids)


# DRIVER

class Driver(models.Model):
    _name = 'uber.driver'
    _inherit = 'uber.user'
    _description = 'Driver'

    vehicle = fields.Char(required=True)
    rides_ids = fields.One2many('uber.ride', 'driver_id')
    ride_count = fields.Integer(compute="_compute_ride_count")

    def _compute_ride_count(self):
        for rec in self:
            rec.ride_count = len(rec.rides_ids)


# RIDE

class Ride(models.Model):
    _name = 'uber.ride'
    _description = 'Ride'

    name = fields.Char(compute="_compute_name", store=True)

    passenger_id = fields.Many2one('uber.passenger', required=True)
    driver_id = fields.Many2one('uber.driver')

    pickup = fields.Char(required=True)
    destination = fields.Char(required=True)

    fare = fields.Float(
        compute='_compute_fare',
        store=True,
        readonly=True,
        default=0.0
    )

    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('done', 'Done')
    ], default='pending')

    payment_id = fields.Many2one('uber.payment', string="Payment")

    url = fields.Char(compute="_compute_url")

    # ---------------- COMPUTE ----------------

    def _compute_url(self):
        for rec in self:
            rec.url = f"/web#id={rec.id}&model=uber.ride&view_type=form"

    @api.depends('pickup', 'destination')
    def _compute_name(self):
        for rec in self:
            if rec.pickup and rec.destination:
                rec.name = f"{rec.pickup} -> {rec.destination}"
            else:
                rec.name = "New Ride"

    @api.depends('pickup', 'destination')
    def _compute_fare(self):
        for rec in self:
            if rec.pickup and rec.destination:
                rec.fare = len(rec.pickup) * 2 + len(rec.destination)
            else:
                rec.fare = 0.0

    # CONSTRAINT

    @api.constrains('pickup', 'destination')
    def _check_locations(self):
        for rec in self:

            if not rec.pickup or not rec.pickup.strip():
                raise ValidationError("Pickup cannot be empty!")

            if not rec.destination or not rec.destination.strip():
                raise ValidationError("Destination cannot be empty!")

            if rec.pickup.strip() == rec.destination.strip():
                raise ValidationError("Pickup and Destination cannot be same!")

    # BUTTONS

    def action_confirm_ride(self):
        for rec in self:
            if rec.status != 'pending':
                raise ValidationError("Only pending rides can be confirmed!")
            rec.status = 'accepted'

    def action_complete_ride(self):
        for rec in self:

            if rec.status == 'done':
                raise ValidationError("Ride already completed!")

            if rec.status != 'accepted':
                raise ValidationError("Ride must be accepted first!")

            # Create payment only if not exists
            if not rec.payment_id:
                payment = self.env['uber.payment'].create({
                    'ride_id': rec.id,
                    'amount': rec.fare
                })
                rec.payment_id = payment.id

            rec.status = 'done'

    def action_view_payment(self):
        self.ensure_one()

        if not self.payment_id:
            raise UserError("No payment found for this ride!")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Payment',
            'res_model': 'uber.payment',
            'view_mode': 'form',
            'res_id': self.payment_id.id,
            'target': 'current',
        }


# سPAYMENT

class Payment(models.Model):
    _name = 'uber.payment'
    _description = 'Payment'

    ride_id = fields.Many2one('uber.ride', required=True)
    amount = fields.Float(required=True, default=0.0)

    status = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid')
    ], default='draft')

    def action_pay(self):
        for rec in self:
            rec.status = 'paid'