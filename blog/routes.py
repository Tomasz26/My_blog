from flask import render_template, request, flash, redirect, url_for, session, Flask
from blog import app
from blog.models import Entry, Message, db
from blog.forms import EntryForm, LoginForm, MessageForm
import functools

def login_required(view_func):
   @functools.wraps(view_func)
   def check_permissions(*args, **kwargs):
       if session.get('logged_in'):
           return view_func(*args, **kwargs)
       return redirect(url_for('login', next=request.path))
   return check_permissions

@app.route("/")
def homepage():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())

    return render_template("home.html", all_posts=all_posts)

@app.route('/contact_me', methods=['GET', 'POST'])
def contact():
    form = MessageForm()

    if request.method == 'POST' and form.validate_on_submit():
        message = Message(
            name_surname=form.name_surname.data,
            contact_mail=form.contact_mail.data,
            body=form.body.data
        )
        db.session.add(message)
        db.session.commit()
        flash("Message sent successfully!", "success")
        return redirect(url_for("homepage"))

    return render_template("contact.html", form=form)

@app.route("/new_post", methods=['GET', 'POST'])
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def handle_post(entry_id = None):
    errors = ""

    if entry_id:  
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
    else:  
        form = EntryForm()
        entry = Entry()

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(entry)

        if not entry_id: 
            db.session.add(entry)

        db.session.commit()
        flash("Post saved successfully!", "success")
        return redirect(url_for("homepage"))

    errors = form.errors if request.method == 'POST' else None
    return render_template("add_post.html", form=form, errors=errors)

@app.route("/delete-post/<int:entry_id>", methods=["POST"])
@login_required
def delete_post(entry_id = None):

    post = Entry.query.filter_by(id=entry_id).first_or_404()

    if post:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully!", "success")
        return redirect(url_for("drafts"))

    return render_template("draft_list.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')

    if request.method == 'POST':
       if form.validate_on_submit():
           session['logged_in'] = True
           session.permanent = True  # Use cookie to store session.
           flash('You are now logged in.', 'success')
           return redirect(next_url or url_for('homepage'))
       else:
           errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)

@app.route('/post/<int:entry_id>')
def show_post(entry_id):
    error = None

    if entry_id:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
    else:
        error = error

    return render_template("post.html", post = entry, error = error)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('homepage'))

@app.route('/about/', methods=['GET', 'POST'])
def about_me():
    return render_template("about.html")

@app.route('/posts_not_published', methods=['GET', 'POST'])
@login_required
def drafts():
    all_posts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())

    return render_template("draft_list.html", all_posts=all_posts)
