from flask import Flask, render_template, flash, redirect, url_for,session
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from models import db,User,Story
from datetime import datetime
from sqlalchemy.exc import IntegrityError 
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/quote_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quote_db.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "mysecretkey"

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error='Internal Server Error'), 500

@app.errorhandler(Exception)
def handle_exception(error):
    return render_template('error.html', error=str(error)), 500


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('email', None)

    return render_template('index.html')

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
    if 'email' not in session and 'username' not in session:
        form = UserLoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.password == form.password.data:
                session['user_id'] = user.id
                session['username'] = user.username
                session['email'] = user.email
                flash('Login Success', 'success')
                return redirect(url_for('acc_home'))
            else:
                flash('Login Failed', 'danger')
                return redirect(url_for('login'))
        return render_template('login.html', form=form)
    else:
        flash('Already logged in', 'info')
        return redirect(url_for('acc_home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.con_password.data:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        try:
            new_user = User(
                username=form.user_name.data,
                email=form.email.data,
                password=form.password.data,
                dp=None, 
                is_deleted=False,
                updated_at=datetime.utcnow(),  
                created_at=datetime.utcnow()  
            )

            # Add user to the database
            db.session.add(new_user)
            db.session.commit()

            flash('Registered successfully', 'success')
            return redirect(url_for('login'))

        except IntegrityError:
            flash('Username or email already exists. Please choose a different one.', 'danger')
            db.session.rollback()  

    return render_template('register.html', form=form)

@app.route('/acc-home', methods=['GET', 'POST'])
def acc_home():
    if 'email' in session and 'username' in session:
        stories = Story.query.all()
        return render_template('aac_home.html', stories=stories)
    else:
        flash('Please Log In', 'error')
        return redirect(url_for('login'))

    
@app.route('/write-story',methods=['GET','POST'])
def write_story():
    if 'email' in session and 'username' in session:
        return redirect(url_for('acc_home'))
    else:
        return redirect(url_for('login'))
    


@app.route('/submit-story', methods=['POST'])
def submit_story():
    if 'email' in session and 'name' in session:
        form=new_story()
        title = form.title.data
        category = form.category.data
        content = form.content.data
        user_id = 1  # Replace with actual user ID retrieval logic

        new_story = Story(title=title, category=category, content=content, user_id=user_id)
        db.session.add(new_story)
        db.session.commit()
        flash(f'{title} Published Succssfully !','success')
        return redirect(url_for('acc_home'))
    else:
        flash('Please Login In !','error')
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
