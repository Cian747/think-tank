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
    title = "ThinkTank - Home"
    return render_template('landing.html', title=title)


@main.route('/home')
def home():
    '''
    Home page
    '''
    if current_user is None:
        return redirect(url_for('auth.login'))

    pitches = Pitch.query.filter(Pitch.id < 5).all()
    title = 'ThinkTank'

    return render_template('index.html', title = title,pitches = pitches)

@main.route('/pitches', methods=['GET','POST'])
@login_required
def pitch():
    
    
    pitches = Pitch.query.all()

    pitch_form = PitchForm()
	
    if pitch_form.validate_on_submit():
        pitch = Pitch(pitch_content = pitch_form.pitch.data,category_name = pitch_form.category.data,user = current_user)
        pitch.save_pitch()

        return redirect(url_for('main.pitch'))
	
    title = 'Pitches'
    return render_template('pitch.html',pitches = pitches, pitch_form = pitch_form, title = title)


@main.route('/pitch/detail/<int:id>', methods = ['GET','POST'])
@login_required
def detail(id):
    '''
    Displays specific pitch detail
    '''
    one_pitch = Pitch.query.filter_by(id = id).first()
    comments = Comment.query.filter_by(pitch_id = id).all()
    com_form = CommentForm()
    if com_form.validate_on_submit():
        comment_write = Comment(pitch_id = one_pitch.id,com_write = com_form.comment.data,user = current_user.id)
        comment_write.save_comment()

        return redirect(url_for('main.detail', id = one_pitch.id))

    if request.args.get('upVote'):
        one_pitch.upVote = one_pitch.upVote + 1
        print(one_pitch.upVote)
        db.session.add(one_pitch)
        db.session.commit()
        return redirect(url_for('main.detail',id = one_pitch.id))

    elif request.args.get('downVote'):
        one_pitch.downVote = one_pitch.downVote + 1
        db.session.add(one_pitch)
        db.session.commit()
        return redirect(url_for('main.detail', id = one_pitch.id))
 

    return render_template('pitch-detail.html',com_form = com_form,one_pitch = one_pitch,comments = comments)

@main.route('/Business pitches', methods = ['GET', 'POST'])
@login_required
def business():
    '''
    Category Page
    '''
    Business = 'Business'
    pitch_business = Pitch.query.filter_by(category_name = Business).all()
    pitch_form = PitchForm()
	
    if pitch_form.validate_on_submit():
        pitch = Pitch(pitch_content = pitch_form.pitch.data,category_name = pitch_form.category.data,user = current_user)
        pitch.save_pitch()

        return redirect(url_for('main.business'))


    title = "Business"
    return render_template('category.html', categories = Business, pitch_form = pitch_form,pitch_cat = pitch_business, title = title, user = current_user)


@main.route('/Creative(Arts) pitches',methods = ['GET', 'POST'])
def creative():
    '''
    Category Page
    '''
    creative = 'Creative'
    pitch_social = Pitch.query.filter_by(category_name = creative).all()

    pitch_form = PitchForm()
	
    if pitch_form.validate_on_submit():
        pitch = Pitch(pitch_content = pitch_form.pitch.data,category_name = pitch_form.category.data,user = current_user)
        pitch.save_pitch()

        return redirect(url_for('main.creative'))


    title = 'Creatives'

    return render_template('category.html', pitch_cat = pitch_social,title = title,pitch_form = pitch_form ,user = current_user)

@main.route('/sports pitches',methods = ['GET', 'POST'])
def sports():
    '''
    Category Page
    '''
    Sports = 'Sports'
    pitch_sports = Pitch.query.filter_by(category_name=Sports).all()

    pitch_form = PitchForm()
	
    if pitch_form.validate_on_submit():
        pitch = Pitch(pitch_content = pitch_form.pitch.data,category_name = pitch_form.category.data,user = current_user)
        pitch.save_pitch()

        return redirect(url_for('main.sports'))

  
    title = 'sports'
    return render_template('category.html', pitch_cat = pitch_sports, title = title, user = current_user,pitch_form = pitch_form)

@main.route('/youth pitches',methods = ['GET', 'POST'])
def youth():
    '''
    Category Page
    '''
    Youth = 'youth'
    pitch_youth = Pitch.query.filter_by(category_name=Youth).all()

    pitch_form = PitchForm()
	
    if pitch_form.validate_on_submit():
        pitch = Pitch(pitch_content = pitch_form.pitch.data,category_name = pitch_form.category.data,user = current_user)
        pitch.save_pitch()

        return redirect(url_for('main.youth'))


    title = 'youth'
    return render_template('category.html', pitch_cat = pitch_youth,pitch_form = pitch_form,title=title, user = current_user)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    pitches = Pitch.query.filter_by(user = current_user).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,pitches = pitches)

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
    title = f'{current_user.username}'
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

@main.route('/pitch-detail/<int:id>',methods = ['GET','POST'])
def votes(id):
    pitch = Pitch.query.filter_by(id = id).first()



# @main.route('/pitch-detail/<int:id>',methods = ['GET','POST'])
# def thumbs_down(id):
#     pitch = Pitch.query.get(id).first()
#     if request.form:
#         if request.args.get['downvote']:
#             if pitch.downVote == 0 :
#                 pitch.downVote = pitch.downVote + 1
#                 db.session.add(pitch)
#                 db.session.commit()
#     return redirect(url_for('main.thumbs_down'))


