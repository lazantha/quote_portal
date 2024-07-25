from flask_sqlalchemy import SQLAlchemy
# model upgrade and make changes
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

    stories = db.relationship('Story', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='comment_author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Story(db.Model):
    __tablename__ = 'stories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)
    updated_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())

    comments = db.relationship('Comment', backref='story', lazy=True)

    def __repr__(self):
        return f'<Story {self.title}>'

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)
    updated_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())

    def __repr__(self):
        return f'<Comment {self.content}>'
