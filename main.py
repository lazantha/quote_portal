from flask import Flask, render_template, flash, redirect, url_for
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from models import db,User

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/quote_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quote_db.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "mysecretkey"

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Import forms after app initialization to avoid circular import
from forms import UserLoginForm, UserRegisterForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            flash('Login Successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed', 'danger')
            return redirect(url_for('login'))
        pass
    return render_template('login.html', form=form)

@app.route('/home',methods=['GET', 'POST'])
def home():

    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        password = form.password.data
        con_password = form.con_password.data
        if password != con_password:
            flash('Password Not Matched', 'danger')
            return redirect(url_for('register'))
        else:
            user = User(username=form.user_name.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registered Successfully', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
