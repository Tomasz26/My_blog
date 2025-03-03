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