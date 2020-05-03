from flask_login import UserMixin

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from config import db, login_manager, app

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@login_manager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    products = db.relationship('Product', backref='seller', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    __table_args__ = {'extend_existing': True}


class Product(db.Model):
    id_product = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    seller_username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)

    def __repr__(self):
        return f"Product('{self.product_name}', '{self.price}')"

    __table_args__ = {'extend_existing': True}


if __name__ == '__main__':
    manager.run()
