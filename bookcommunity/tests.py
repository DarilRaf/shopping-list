from django.test import TestCase
from homepage.models import CustomUser  # Ganti sesuai dengan tempat CustomUser Anda berada
from .models import Forum, Discussion

class ForumModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a custom user for testing
        cls.user = CustomUser.objects.create_user(username='testuser', password='testpassword')


class DiscussionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a custom user for testing
        cls.user = CustomUser.objects.create_user(username='testuser', password='testpassword')

    def setUp(self):
        # Create a sample forum
        self.forum = Forum.objects.create(user=self.user, book='Sample Book', subject='Sample Subject', description='Sample Description')
    
    def test_subject_max_length(self):
        forum = Forum.objects.get(id=self.forum.id)
        max_length = forum._meta.get_field('subject').max_length
        self.assertLessEqual(len(forum.subject), max_length)

    def test_str_representation(self):
        forum = Forum.objects.get(id=self.forum.id)
        self.assertEqual(str(forum), forum.subject)

class DiscussionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a user for testing
        cls.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        
    def setUp(self):
        # Create a sample forum and discussion
        self.forum = Forum.objects.create(user=self.user, book='Sample Book', subject='Sample Subject', description='Sample Description')
        self.discussion = Discussion.objects.create(user=self.user, forum=self.forum, discuss='Sample Discussion')
    
    def test_discuss_max_length(self):
        discussion = Discussion.objects.get(id=self.discussion.id)
        max_length = discussion._meta.get_field('discuss').max_length
        self.assertLessEqual(len(discussion.discuss), max_length)

    def test_str_representation(self):
        discussion = Discussion.objects.get(id=self.discussion.id)
        self.assertEqual(str(discussion), str(discussion.forum))

    def test_user_can_be_null(self):
        discussion = Discussion.objects.create(forum=self.forum, discuss='Sample Discussion')
        self.assertIsNone(discussion.user)
