from flask_sqlalchemy import SQLAlchemy
# model upgrade and make changes
# export FLASK_APP=app.py
# flask db init
# flask db migrate -m'messege'
# flask db upgrade

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    dp = db.Column(db.String(200), nullable=True)
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)
    updated_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())

    def __repr__(self):
        return f'<User {self.username}>'