from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User
import stripe
from .. import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main.route('/subscribe')
@login_required
def subscribe():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Premium Access',
                    },
                    'unit_amount': 999,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=os.getenv('STRIPE_SUCCESS_URL'),
            cancel_url=os.getenv('STRIPE_CANCEL_URL'),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        flash(f"Payment failed: {e}")
        return redirect(url_for('main.dashboard'))

@main.route('/success')
@login_required
def success():
    current_user.is_premium = True
    db.session.commit()
    return render_template('success.html')

@main.route('/ai-feature')
@login_required
def ai_feature():
    if not current_user.is_premium:
        flash('Upgrade to premium to access this feature.')
        return redirect(url_for('main.dashboard'))
    result = 'Sample AI result here.'
    return render_template('ai.html', result=result)
