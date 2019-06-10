from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField
from wtforms.widgets.html5 import NumberInput


class PurchaseForm(FlaskForm):
    category = SelectField('Catégorie', coerce=int)
    price = FloatField('Prix', widget=NumberInput(step=0.01))


class BudgetForm(FlaskForm):
    category = SelectField('Catégorie', coerce=int)
    limit = FloatField('Limite', widget=NumberInput(step=0.01))
