from flask import render_template, request, flash, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

#app = Flask(__name__)

@app.route("/")
def homepage():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())

    return render_template("home.html", all_posts=all_posts)

@app.route("/new_post", methods=['GET', 'POST'])
def new_post():
    form = EntryForm()
    errors = ""

    if request.method == "POST":
        if form.validate_on_submit():
            post = Entry(
                title = form.title.data,
                body = form.body.data,
                is_published=form.is_published.data
                )
            db.session.add(post)
            db.session.commit()
            flash("Post added successfully!", "success")
            return redirect(url_for("homepage"))
        else:
            errors = form.errors

    return render_template("add_post.html", form=form, errors=errors)

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
   entry = Entry.query.filter_by(id=entry_id).first_or_404()
   form = EntryForm(obj=entry)
   errors = None
   if request.method == 'POST':
       if form.validate_on_submit():
           form.populate_obj(entry)
           db.session.commit()
       else:
           errors = form.errors
   return render_template("add_post.html", form=form, errors=errors)