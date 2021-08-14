from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from flask_login import login_required,current_user
from ..models import Comment, User,Pitch
from .. import db,photos
from .forms import CommentForm, UpdateProfile,PitchForm


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

@main.route('/pitches', methods=['GET','POST'])
@login_required
def pitch():
    
    
    pitches = Pitch.query.all()

    pitch_form = PitchForm()
	
    if pitch_form.validate_on_submit():
        pitch = Pitch(pitch_content = pitch_form.pitch.data,category_name = pitch_form.category.data,user = current_user)
        db.session.add(pitch)
        db.session.commit()

        return redirect(url_for('main.pitch'))
	

    return render_template('pitch.html',pitches = pitches, pitch_form = pitch_form)

@main.route('/Business', methods = ['GET', 'POST'])
@login_required
def business(catname):
    '''
    Category Page
    '''
    comment = Comment.query.filter_by(category_name = catname).first()
    pitch_form = PitchForm()
	
    if pitch_form.validate_on_submit():
        pitch = Pitch(pitch_content = pitch_form.pitch.data,category_name = pitch_form.category.data,user = current_user)
        db.session.add(pitch)
        db.session.commit()

        return redirect(url_for('main.pitch'))


    Business = 'Business'

    return render_template('category.html', categories = Business, pitch_form = pitch_form,comment = comment)


@main.route('/pitch/detail/<int:id>', methods = ['GET','POST'])
def detail(id):
    '''
    Displays specific pitch detail
    '''
    one_pitch = Pitch.query.filter_by(id = id).first()

    com_form = CommentForm()
    if com_form.validate_on_submit():
        comments = Comment(com_write = com_form.comment.data)
        db.session.add(comments)
        db.session.commit()

    return render_template('pitch-detail.html',one_pitch = one_pitch,com_form = com_form)

@main.route('/category',methods = ['GET', 'POST'])
def creative():
    '''
    Category Page
    '''
    Social = 'social'

    return render_template('category.html', categories = Social)

@main.route('/category',methods = ['GET', 'POST'])
def sports():
    '''
    Category Page
    '''
    Sports = 'sports'
    single_pitch = Pitch.query.filter_by(category=Sports).all()
  

    return render_template('category.html', single_pitch = single_pitch)

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

@main.route('/review/<int:id>',methods = ['GET','POST'])
def thumbs_up(id):
    pitch = Pitch.query.filter_by(id = id)
    if pitch.upVote is None:
        pitch.upVote = pitch.upVote + 1
        db.session.add(pitch)
        db.session.commit()
    return redirect(url_for('main.thumbs_up'))


@main.route('/review/<int:id>',methods = ['GET','POST'])
def thumbs_down(id):
    pitch = Pitch.query.get(id)
    if pitch.downVote is None:
        pitch.downVote = pitch.downVote + 1
        db.session.add(pitch)
        db.session.commit()
    return redirect(url_for('main.thumbs_down'))

