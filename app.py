from flask import Flask, render_template, redirect, url_for
from models import db, Category, Budget, Purchase
from forms import PurchaseForm
from datetime import datetime
from sqlalchemy import extract

app = Flask(__name__)


app.secret_key = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

db.init_app(app)


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

    purchases = Purchase.query.filter(extract('month', Purchase.date) == datetime.now().month).all()

    return render_template('homepage.html', form=form, purchases=purchases)


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
