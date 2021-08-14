from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from flask_login import login_required,current_user
from ..models import User,Pitch
from .. import db,photos
from .forms import UpdateProfile,PitchForm


@main.route('/')
def landing():
    '''
    Greeting and landing page when a user launches the application
    '''
    title = "ThinkTank"
    return render_template('landing.html', title=title)


@main.route('/home')
def home():
    '''
    Home page
    '''
    if current_user is None:
        return redirect(url_for('auth.login'))
    message = 'Your time starts now'
    title = 'ThinkTank'

    return render_template('index.html', title = title, message = message)

@main.route('/pitch')
@login_required
def pitch(usname):
    user = User.query.filter_by(username = usname).first()

    if user is None:
        abort(404)

    pitch_form = PitchForm()
	
    if pitch_form.validate_on_submit():
        if pitch_form.category_name.data == 'Business':
            pitch = Pitch( category_id = pitch_form.category_name.data ,pitch_content = pitch_form.pitch_content )
            db.session.add(pitch)
            db.session.commit()
            
        elif pitch_form.category_name.data == 'sports':
            pitch = Pitch(category_id = pitch_form.category_name.data ,pitch_content = pitch_form.pitch_content)
            db.session.add(pitch)
            db.session.commit()
            
        elif pitch_form.category_name.data == 'youth':
            pitch = Pitch(category_id = pitch_form.category_name.data,pitch_content = pitch_form.pitch_content )
            db.session.add(pitch)
            db.session.commit()
        
        elif pitch_form.category_name.data == 'creative':
            pitch = Pitch(category_id = pitch_form.category_name.data  ,pitch_content =pitch_form.pitch_content )
            db.session.add(pitch)
            db.session.commit()

        else:
            flash('Fill in the fields correctly')
                
            return redirect(url_for('main.home'))

@main.route('/Business', methods = ['GET', 'POST'])
@login_required
def business():

    '''
    Category Page
    '''
  
    pitch_form = PitchForm()
	
    if pitch_form.validate_on_submit():
        pitch = Pitch(pitch_content = pitch_form.pitch.data,category_name = pitch_form.category.data,user = current_user)
        db.session.add(pitch)
        db.session.commit()

        return redirect(url_for('main.home'))


    Business = 'Business'

    return render_template('category.html', categories = Business, pitch_form = pitch_form)

@main.route('/category',methods = ['GET', 'POST'])
def creative():
    '''
    Category Page
    '''
    Social = 'Category'

    return render_template('category.html', categories = Social)

@main.route('/category',methods = ['GET', 'POST'])
def sports():
    '''
    Category Page
    '''
    Sports = 'Category'

    return render_template('category.html', categories = Sports)

@main.route('/category',methods = ['GET', 'POST'])
def youth():
    '''
    Category Page
    '''
    Youth = 'Category'

    return render_template('category.html', categories = Youth )

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['GET','POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()

    if request.method == 'POST':
        if request.files:
            if 'photo' in request.files:
                    filename = photos.save(request.files['photo'])
                    path = f'photos/{filename}'
                    user.profile_pic_path = path
                    print(user.profile_pic_path)
                    db.session.add(user)
                    db.session.commit()
                    
    return redirect(url_for('main.profile',uname=uname))
