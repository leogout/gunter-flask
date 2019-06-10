from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField
from wtforms.widgets.html5 import NumberInput


class PurchaseForm(FlaskForm):
    category = SelectField('Category', coerce=int)
    price = FloatField('Price', widget=NumberInput(step=0.01))
