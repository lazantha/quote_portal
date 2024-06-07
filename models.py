from main import db

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(80), nullable=False)
    dp=db.Column(db.FileField(), nullable=True)
    
    def __repr__(self):
        return '<User %r>' % self.username

class posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text(), unique=True, nullable=False)
    image=db.Column(db.FileField(), nullable=True)

    def __repr__(self):
        return '<Post %r>' % self.title