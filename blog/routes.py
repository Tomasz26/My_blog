from flask import render_template, request, flash, redirect, url_for, session
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm

#app = Flask(__name__)

@app.route("/")
def homepage():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())

    return render_template("home.html", all_posts=all_posts)

@app.route("/new_post", methods=['GET', 'POST'])
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
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


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('homepage'))