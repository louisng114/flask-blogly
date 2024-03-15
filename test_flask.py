from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'

class UserTestCase(TestCase):
    """Tests for handling users"""

    def setUp(self):
        self.app = app
        self.client = self.app.test_client() 
        self.context = self.app.app_context()
        self.context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.context.pop()

    def test_new_user_redirect(self):
        with app.test_client() as client:
            resp = client.post("/users/new",
                                data={"first_name" : "Leonhard",
                                        "last_name" : "Euler",
                                        "image_url" : ""})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

    def test_new_user(self):
        with app.test_client() as client:
            resp = client.post("/users/new",
                                data={"first_name" : "Leonhard",
                                        "last_name" : "Euler",
                                        "image_url" : ""},
                                follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/users/1">Leonhard Euler</a></li>',html)

    def edit_user_redirect(self):
        with app.test_client() as client:
            user = User(first_name="Leonhard", last_name="Euler", image_url="")

            db.session.add(user)
            db.session.commit()

            resp = client.post("/users/1/edit",
                                data={"first_name" : "Leonhard",
                                        "last_name" : "Euler",
                                        "image_url" : ""})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users/1")


    def edit_user(self):
        with app.test_client() as client:
            user = User(first_name="Leonhard", last_name="Euler", image_url="")

            db.session.add(user)
            db.session.commit()

            resp = client.post("/users/1/new",
                                data={"first_name" : "Carl",
                                        "last_name" : "Gauss",
                                        "image_url" : ""},
                                follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Euler",html)
            self.assertIn('<li><a href="/users/1">Carl Gauss</a></li>',html)

    def delete_user_redirect(self):
        with app.test_client() as client:
            user = User(first_name="Leonhard", last_name="Euler", image_url="")

            db.session.add(user)
            db.session.commit()

            resp = client.post("/users/1/delete")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

    def delete_user(self):
        with app.test_client() as client:
            user = User(first_name="Leonhard", last_name="Euler", image_url="")

            db.session.add(user)
            db.session.commit()

            resp = client.post("/users/1/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Euler", html)

class PostTestCase(TestCase):
    """Tests for handling posts"""

    def setUp(self):
        self.app = app
        self.client = self.app.test_client() 
        self.context = self.app.app_context()
        self.context.push()

        db.create_all()

        user = User(first_name="Leonhard", last_name="Euler", image_url="")

        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.context.pop()

    def test_new_post_redirect(self):
        with app.test_client() as client:
            resp = client.post("/users/1/posts/new",
                                data={"title" : "Hello",
                                    "content" : "Goodbye"})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users/1")

    def test_new_post(self):
        with app.test_client() as client:
            resp = client.post("/users/1/posts/new",
                                data={"title" : "Hello",
                                    "content" : "Goodbye"},
                                follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/posts/1">Hello</a></li>',html)

    def edit_post_redirect(self):
        with app.test_client() as client:
            post = Post(title="Hello", content="Goodbye", user=1)

            db.session.add(post)
            db.session.commit()

            resp = client.post("/posts/1/edit",
                                data={"title" : "Konnichiwa",
                                        "content" : "Sayounara"})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/posts/1")


    def edit_post(self):
        with app.test_client() as client:
            post = Post(title="Hello", content="Goodbye", user=1)

            db.session.add(post)
            db.session.commit()

            resp = client.post("/posts/1/edit",
                                data={"title" : "Konnichiwa",
                                        "content" : "Sayounara"},
                                follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Hello",html)
            self.assertIn('<li><a href="/post/1">Konnichiwa</a></li>',html)

    def delete_post_redirect(self):
        with app.test_client() as client:
            post = Post(title="Hello", content="Goodbye", user=1)

            db.session.add(post)
            db.session.commit()

            resp = client.post("/posts/1/delete")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users/1")

    def delete_post(self):
        with app.test_client() as client:
            post = Post(title="Hello", content="Goodbye", user=1)

            db.session.add(post)
            db.session.commit()

            resp = client.post("/posts/1/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Hello", html)
