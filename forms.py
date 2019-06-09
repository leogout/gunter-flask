from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField


class PurchaseForm(FlaskForm):
    category = SelectField('Category', coerce=int)
    price = FloatField('Price')

