from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask_talisman import Talisman, ALLOW_FROM

test_deposit = Blueprint('test_deposit', __name__,
                        template_folder='.', url_prefix='/')

talisman = Talisman()

@test_deposit.route('/test')
@talisman(content_security_policy=[])
def deposit_form():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)