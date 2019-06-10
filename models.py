from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    limit = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship(Category)

    def __str__(self):
        return self.category.name


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship(Category)

    def __str__(self):
        return '{} {}€'.format(self.category, self.price)


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
