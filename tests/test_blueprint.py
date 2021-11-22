from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

test_deposit = Blueprint('test_deposit', __name__,
                        template_folder='.', url_prefix='/')


@test_deposit.route('/test')
def deposit_form():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)