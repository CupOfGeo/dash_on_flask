from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import abort

import os
import stripe

stripe.api_key = os.environ['STRIPE_SECRET_KEY']


stripe_bp = Blueprint('stripe', __name__)
stripe_prefix = '/stripe'

products = {
        'private_model': {
            'name': 'your own private fine-tuned model',
            'price': 5000,
            'per': 'month',
        },
    }

@stripe_bp.route('/')
def index():
    return render_template('stripe.html', products=products, stripe_prefix=stripe_prefix)

@stripe_bp.route('/order/<product_id>', methods=['POST'])
def order(product_id):
    if product_id not in products:
        abort(404)

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'product_data': {
                        'name': products[product_id]['name'],
                    },
                    'unit_amount': products[product_id]['price'],
                    'currency': 'usd',
                },
                'quantity': 1,
            },
        ],
        payment_method_types=['card'],
        mode='payment',
        success_url=request.host_url + stripe_prefix.replace('/', '') + '/order/success',
        cancel_url=request.host_url + stripe_prefix.replace('/', '') + '/order/cancel',
    )
    return redirect(checkout_session.url)

@stripe_bp.route('/order/success')
def success():
    return render_template('success.html')


@stripe_bp.route('/order/cancel')
def cancel():
    return render_template('cancel.html')