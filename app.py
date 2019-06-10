from flask import Flask, render_template, redirect, url_for
from models import db, Category, Budget, Purchase
from forms import PurchaseForm
from datetime import datetime
from sqlalchemy import extract
import locale
import os

if os.name == 'nt':
    locale.setlocale(locale.LC_TIME, "fr")
else:
    locale.setlocale(locale.LC_TIME, "fr_FR")

app = Flask(__name__)


app.secret_key = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

db.init_app(app)


class CategoryRecap:
    def __init__(self, category, purchases, budget):
        self.category = category
        self.purchases = purchases
        self.budget = budget

    def get_price(self):
        return sum([p.price for p in self.purchases])

    def get_budget(self):
        return self.budget.limit

    def get_name(self):
        return self.category.name

    def get_percentage(self):
        return round(self.get_price() / self.get_budget() * 100)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = PurchaseForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        purchase = Purchase(
            date=datetime.now(),
            category_id=form.category.data,
            price=form.price.data
        )
        db.session.add(purchase)
        db.session.commit()

        return redirect(url_for('home'))

    purchases_q = Purchase.query \
        .filter(extract('month', Purchase.date) == datetime.now().month) \
        .order_by(Purchase.date.desc())

    category_recaps = []

    for category in Category.query.all():
        purchases = purchases_q.filter(Purchase.category == category).all()
        budget = Budget.query.filter(Budget.category == category).first()
        category_recaps.append(CategoryRecap(category=category, purchases=purchases, budget=budget))

    return render_template('homepage.html', form=form, category_recaps=category_recaps, recap=recap)


@app.route('/remove/<int:id>', methods=['GET', 'POST'])
def remove(id):
    search = Purchase.query.get(id)

    if search:
        db.session.delete(search)
        db.session.commit()

    return redirect(url_for('home'))


@app.route('/recap', methods=['GET', 'POST'])
def recap():
    purchases = Purchase.query.filter(extract('month', Purchase.date) == datetime.now().month - 1).all()

    return render_template('recap.html', purchases=purchases)


@app.cli.command()
def initdb():
    db.create_all()

    cat_petrol = Category(name='Essence')
    cat_hobby = Category(name='Loisirs')
    cat_groceries = Category(name='Courses')

    db.session.add(cat_petrol)
    db.session.add(cat_hobby)
    db.session.add(cat_groceries)

    db.session.commit()

    bud_petrol = Budget(category=cat_petrol, limit=200)
    bud_hobby = Budget(category=cat_hobby, limit=200)
    bud_groceries = Budget(category=cat_groceries, limit=200)

    db.session.add(bud_petrol)
    db.session.add(bud_hobby)
    db.session.add(bud_groceries)

    db.session.commit()
