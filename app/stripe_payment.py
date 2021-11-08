from flask import Blueprint
from flask import redirect
from flask import render_template

from flask import abort, jsonify, request
from flask_login import current_user
from flask_login import login_required

from app.models import User
from app.extensions import db

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
        'adjustable_quantity': {
            'enabled': True,
            'minimum': 1,
            'maximum': 3,
        },
    },
}


@stripe_bp.route('/')
def index():
    return render_template('stripe.html', products=products, stripe_prefix=stripe_prefix)


@stripe_bp.route('/order/<product_id>', methods=['POST'])
@login_required
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

                'adjustable_quantity': products[product_id].get(
                    'adjustable_quantity', {'enabled': False}),
            },
        ],
        payment_method_types=['card'],
        mode='payment',
        success_url=request.host_url + stripe_prefix.replace('/', '') + '/order/success',
        cancel_url=request.host_url + stripe_prefix.replace('/', '') + '/order/cancel',
    )
    return redirect(checkout_session.url)


@stripe_bp.route('/order/success')
@login_required
def success():
    return render_template('success.html')


@stripe_bp.route('/order/cancel')
@login_required
def cancel():
    return render_template('cancel.html')


@stripe_bp.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ['STRIPE_WEBHOOK_SECRET']
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
    elif event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']
    elif event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print('🔔 Payment succeeded!')

        # for test user doesnt exist
        if current_user.is_authenticated:
            user = User.query.filter_by(username=current_user.username).first()
            user.inc_models_allowed()
            db.session.commit()

        # session = stripe.checkout.Session.retrieve(
        #     event['data']['object'].id, expand=['line_items'])
        # print(f'Sale to {session.customer_details.email}:')
        # for item in session.line_items.data:
        #     print(f'  - {item.quantity} {item.description} '
        #           f'${item.amount_total/100:.02f} {item.currency.upper()}')
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)
