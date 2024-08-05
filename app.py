from flask import Flask, render_template, flash, redirect, url_for,session,request
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from models import db,User,Story,Comment
from forms import UserLoginForm, UserRegisterForm,StoryForm,CommentForm
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
    return render_template('errors/error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/error.html', error='Internal Server Error'), 500

@app.errorhandler(Exception)
def handle_exception(error):
    return render_template('errors/error.html', error=str(error)), 500


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('email', None)
    print("session cleared")
    return redirect(url_for('index'))


@app.route('/')
def index():
    stories = Story.query.order_by(Story.created_at.asc()).all()
    return render_template('index.html',stories=stories)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Import forms after app initialization to avoid circular import

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
        user = User.query.filter_by(email=session['email'], username=session['username']).first()
        stories = Story.query.filter_by(user_id=user.id).order_by(Story.created_at.asc()).all()
        return render_template('user_account/aac_home.html', stories=stories)
    else:
        flash('Please Log In', 'error')
        return redirect(url_for('login'))


    
@app.route('/write-story',methods=['GET','POST'])
def write_story():
    if 'email' in session and 'username' in session:
        form=StoryForm()
        
        return render_template('user_account/write_story.html',form=form)

    else:
        return redirect(url_for('login'))
    



@app.route('/submit-story', methods=['POST'])
def submit_story():
    if 'email' in session and 'username' in session:
        form = StoryForm()
        if form.validate_on_submit():
            title = form.title.data
            category = form.category.data
            content = form.content.data
            
            user = User.query.filter_by(email=session['email'], username=session['username']).first()
            
            if user:
                new_story = Story(title=title, category=category, content=content, user_id=user.id)
                db.session.add(new_story)
                db.session.commit()
                flash(f'{title} Published Successfully!', 'success')
                return redirect(url_for('acc_home'))
            else:
                flash('User not found. Please log in again.', 'error')
                return redirect(url_for('login'))
        else:
            flash('Form validation failed. Please check your inputs.', 'error')
            return redirect(url_for('acc_home'))
    else:
        flash('Please log in to submit a story.', 'error')
        return redirect(url_for('login'))


@app.route('/romantic', methods=['GET'])
def romantic():
    romance_stories = Story.query.filter_by(category='romance').order_by(Story.created_at.asc()).all()

    return render_template('categories/romance.html',stories=romance_stories)

@app.route('/horror', methods=['GET'])
def horror():
    horror_stories = Story.query.filter_by(category='horror').order_by(Story.created_at.asc()).all()
    return render_template('categories/horror.html',stories=horror_stories)


@app.route('/adventure', methods=['GET'])
def adventure():
    adventure_stories = Story.query.filter_by(category='adventure').order_by(Story.created_at.asc()).all()
    
    return render_template('categories/adventure.html',stories=adventure_stories)


@app.route('/love',methods=['GET'])
def love():
    love_stories = Story.query.filter_by(category='love').order_by(Story.created_at.asc()).all()
    
    return render_template('categories/love.html',stories=love_stories)


@app.route('/story/<int:story_id>', methods=['GET'])
def view_story(story_id):
    story = Story.query.get_or_404(story_id)
    print("Story:", story)
    form = CommentForm()
    comments = Comment.query.filter_by(story_id=story_id).order_by(Comment.created_at.asc()).all()        
    return render_template('user_account/view_story.html', story=story, form=form, comments=comments)


# delete stories
@app.route('/delete_story/<int:story_id>', methods=['GET'])
def delete_story(story_id):
    if 'email' in session and 'username' in session:
        story = Story.query.get_or_404(story_id)
        db.session.delete(story)
        db.session.commit()
        flash(f'Story "{story.title}" has been deleted successfully!', 'success')
        return redirect(request.referrer or url_for('acc_home'))
    else:
        flash('Please Log In!', 'error')
        return redirect(url_for('login'))
    

# implement

@app.route('/edit_story/<int:story_id>', methods=['GET'])
def edit_story(story_id):
    if 'email' in session and 'username' in session:
        story = Story.query.get_or_404(story_id)
        form = StoryForm(obj=story)
        return render_template('user_account/edit_story.html', form=form, story=story)
    else:
        flash('Please Log In!', 'error')
        return redirect(url_for('login'))

@app.route('/update_story/<int:story_id>', methods=['POST'])
def update_story(story_id):
    if 'email' in session and 'username' in session:
        story = Story.query.get_or_404(story_id)
        form = StoryForm()
        if form.validate_on_submit():
            story.title = form.title.data
            story.category = form.category.data
            story.content = form.content.data
            db.session.commit()
            flash(f'Story "{story.title}" has been updated successfully!', 'success')
            return redirect(url_for('acc_home'))
        return render_template('edit_story.html', form=form, story=story)
    else:
        flash('Please Log In!', 'error')
        return redirect(url_for('login'))


@app.route('/comment/<int:story_id>', methods=['POST'])
def comment(story_id):
    print("comment method loaded")
    
    if 'email' in session and 'username' in session:
        form = CommentForm()
        print("ready to render form")
        
        if form.validate_on_submit():
            comment_content = form.comment.data
            print("comment loaded:", comment_content)
            
            user = User.query.filter_by(email=session['email'], username=session['username']).first()
            
            if user:
                print("user loaded", user.id)
                
                new_comment = Comment(content=comment_content, user_id=user.id, story_id=story_id)
                db.session.add(new_comment)
                print("comment added to the database")
                
                try:
                    db.session.commit()
                    print("database committed")
                    flash('Comment added successfully', 'success')
                    return redirect(url_for('view_story', story_id=story_id))
                except Exception as e:
                    print("database commit failed:", e)
                    db.session.rollback()
                    flash('Database error. Please try again.', 'error')
                    return redirect(url_for('view_story', story_id=story_id))
                
                return redirect(url_for('view_story', story_id=story_id))
            else:
                print("user not found")
                flash('User not found. Please log in again.', 'error')
                return redirect(url_for('login'))
        else:
            print("form validation failed")
            flash('Form validation failed. Please check your inputs.', 'error')
            return redirect(url_for('view_story', story_id=story_id))
    else:
        print("user not logged in")
        flash('Please Log In!', 'error')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
