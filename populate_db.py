from faker import Faker
from blog import app
from blog.models import Entry, db

def generate_random_posts(how_many=10):
    #function tht generates randoms post for project database
    fake = Faker()

    with app.app_context():
        for i in range(how_many):
            post = Entry(
                title = fake.sentence(),
                body='\n'.join(fake.paragraphs(3)), # <-- choose how long the post should be
                is_published=True
            )
            db.session.add(post)
        db.session.commit()
        print(f"I worked and populated db with {how_many} new posts")

if __name__ == "__main__":
    generate_random_posts(10)
