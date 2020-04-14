from django.test import TestCase
from .models import *
from .forms import *
from datetime import date

class UserProfileTestCase(TestCase):
    def setUp(self):
        skill0 = Skill.objects.create(
            title="skill0",
            description="Nothing yet"
        )
        
        skill1 = Skill.objects.create(
            title="skill1",
            description="Nothing yet"
        )

        skill2 = Skill.objects.create(
            title="skill2",
            description="Nothing yet"
        )

        user0 = UserProfile.objects.create(
            username="user0",
            email="user0@case.edu",
            first_name="User",
            last_name="Zero",
            date_of_birth=date(2020, 3, 27),
            has_skill=skill0)

        user1 = UserProfile.objects.create(
            username="user1",
            email="user1@case.edu",
            first_name="User",
            last_name="One",
            date_of_birth=date(2020, 3, 26),
            has_skill=skill1)

        user2 = UserProfile.objects.create(
            username="user2",
            email="user2@case.edu",
            first_name="User",
            last_name="Two",
            date_of_birth=date(2020, 3, 25),
            has_skill=skill2)

        post0 = Post.objects.create(
            title="post0",
            description="Nothing",
            status="PENDING",
            points=10,
            seeker=user0,
            req_skill=skill1
        )

        post1 = Post.objects.create(
            title="post1",
            description="Nothing",
            status="PENDING",
            points=1000,
            seeker=user1,
            req_skill=skill2
        )

        post2 = Post.objects.create(
            title="post2",
            description="Nothing",
            status="PENDING",
            points=10,
            seeker=user2,
            req_skill=skill0
        )

        app0 = Application.objects.create(
            post=post0,
            giver=user1,
            status='PENDING'
        )

    def test_userprofile_creation(self):
        user = UserProfile.objects.get(username="user0")
        skill = Skill.objects.get(title="skill0")
        self.assertEqual(user.username, "user0")
        self.assertEqual(user.email, "user0@case.edu")
        self.assertEqual(user.first_name, "User")
        self.assertEqual(user.last_name, "Zero")
        self.assertEqual(user.date_of_birth, date(2020, 3, 27))
        self.assertEqual(user.has_skill, skill)

    def test_can_accept_application_true(self):
        user0 = UserProfile.objects.get(username="user0")
        post0 = Post.objects.get(title="post0")
        self.assertTrue(user0.can_accept_application(post0))

    def test_can_accept_application_false(self):
        user0 = UserProfile.objects.get(username="user0")
        post0 = Post.objects.get(title="post0")
        user1 = UserProfile.objects.get(username="user1")
        post1 = Post.objects.get(title="post1")
        self.assertFalse(user1.can_accept_application(post0))
        self.assertFalse(user1.can_accept_application(post1))

    def test_accept_application(self):
        user0 = UserProfile.objects.get(username="user0")
        post0 = Post.objects.get(title="post0")
        user0.accept_application(post0)
        self.assertEqual(user0.points, 90)
        # self.assertEqual(post0.status, 'ACCEPTED')

    def test_can_create_post_true(self):
        user0 = UserProfile.objects.get(username="user0")
        post0 = Post.objects.get(title="post0")
        self.assertTrue(user0.can_create_post(post0))

    def test_can_create_post_false(self):
        user0 = UserProfile.objects.get(username="user0")
        post0 = Post.objects.get(title="post0")
        user1 = UserProfile.objects.get(username="user1")
        post1 = Post.objects.get(title="post1")
        self.assertFalse(user0.can_create_post(post1))
        self.assertFalse(user1.can_create_post(post0))

    def test_can_apply_post_true(self):
        user1 = UserProfile.objects.get(username="user1")
        post0 = Post.objects.get(title="post0")
        self.assertTrue(user1.can_apply_post(post0))

    def test_can_apply_post_false(self):
        user0 = UserProfile.objects.get(username="user0")
        post0 = Post.objects.get(title="post0")
        user1 = UserProfile.objects.get(username="user1")
        post1 = Post.objects.get(title="post1")
        self.assertFalse(user0.can_apply_post(post0))
        self.assertFalse(user1.can_apply_post(post1))
        self.assertFalse(user0.can_apply_post(post1))

    
class PostTestCase(TestCase):
    def setUp(self):
        skill0 = Skill.objects.create(
            title="skill0",
            description="Nothing yet"
        )
        
        skill1 = Skill.objects.create(
            title="skill1",
            description="Nothing yet"
        )

        skill2 = Skill.objects.create(
            title="skill2",
            description="Nothing yet"
        )

        user0 = UserProfile.objects.create(
            username="user0",
            email="user0@case.edu",
            first_name="User",
            last_name="Zero",
            date_of_birth=date(2020, 3, 27),
            has_skill=skill0)

        user1 = UserProfile.objects.create(
            username="user1",
            email="user1@case.edu",
            first_name="User",
            last_name="One",
            date_of_birth=date(2020, 3, 26),
            has_skill=skill1)

        user2 = UserProfile.objects.create(
            username="user2",
            email="user2@case.edu",
            first_name="User",
            last_name="Two",
            date_of_birth=date(2020, 3, 25),
            has_skill=skill2)

        post0 = Post.objects.create(
            title="post0",
            description="Nothing",
            status="PENDING",
            points=10,
            seeker=user0,
            req_skill=skill1
        )

        post1 = Post.objects.create(
            title="post1",
            description="Nothing",
            status="PENDING",
            points=1000,
            seeker=user1,
            req_skill=skill2
        )

        post2 = Post.objects.create(
            title="post2",
            description="Nothing",
            status="PENDING",
            points=10,
            seeker=user2,
            req_skill=skill0
        )

    def test_post_creation(self):
        post = Post.objects.get(title="post0")
        user = UserProfile.objects.get(username="user0")
        skill = Skill.objects.get(title="skill1")
        self.assertEqual(post.title, "post0")
        self.assertEqual(post.description, "Nothing")
        self.assertEqual(post.status, "PENDING")
        self.assertEqual(post.points, 10)
        self.assertEqual(post.seeker, user)
        self.assertEqual(post.req_skill, skill)

class SkillTestCase(TestCase):
    def setUp(self):
        skill0 = Skill.objects.create(
            title="skill0",
            description="Nothing yet"
        )

    def test_skill_creation(self):
        skill = Skill.objects.get(title="skill0")
        self.assertEqual(skill.title, "skill0")
        self.assertEqual(skill.description, "Nothing yet")

class ApplicationTestCase(TestCase):
    def setUp(self):
        skill0 = Skill.objects.create(
            title="skill0",
            description="Nothing yet"
        )
        
        skill1 = Skill.objects.create(
            title="skill1",
            description="Nothing yet"
        )

        user0 = UserProfile.objects.create(
            username="user0",
            email="user0@case.edu",
            first_name="User",
            last_name="Zero",
            date_of_birth=date(2020, 3, 27),
            has_skill=skill0)

        user1 = UserProfile.objects.create(
            username="user1",
            email="user1@case.edu",
            first_name="User",
            last_name="One",
            date_of_birth=date(2020, 3, 26),
            has_skill=skill1)

        post0 = Post.objects.create(
            title="post0",
            description="Nothing",
            status="PENDING",
            points=10,
            seeker=user0,
            req_skill=skill1
        )

        app0 = Application.objects.create(
            post=post0,
            giver=user1,
            status='PENDING'
        )
    
    def test_application_creation(self):
        post = Post.objects.get(title="post0")
        app = Application.objects.get(post=post)
        giver = UserProfile.objects.get(username="user1")
        self.assertEqual(app.post, post)
        self.assertEqual(app.giver, giver)
        self.assertEqual(app.status, "PENDING")

class PostListViewTestCase(TestCase):
    def test_normal(self):
        res = self.client.get('posts:post/1')
        self.assertEqual(res.status_code, 404)

class UserProfileCreationForm(TestCase):
    def setUp(self):
        skill0 = Skill.objects.create(
            title="skill0",
            description="Nothing yet"
        )

        self.user0 = UserProfile.objects.create(
            username="user0",
            email="user0@case.edu",
            first_name="User",
            last_name="Zero",
            date_of_birth=date(2020, 3, 27),
            has_skill=skill0)

    # def test_normal(self):
    #     UserProfileCreationForm(fields="user0")