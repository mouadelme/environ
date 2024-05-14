from django.test import TestCase
from whistleblower.models import UploadFile
from whistleblower.models import User

class TestUploadFile(TestCase):
    @classmethod
    def setUpTestData(cls):
        UploadFile.objects.create(name='test', picture="test.pdf")

    def testNameLength(self):
        file = UploadFile.objects.get(id=1)
        max_length = file._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def testUserNameLength(self):
        file = UploadFile.objects.get(id=1)
        max_length = file._meta.get_field('username').max_length
        self.assertEqual(max_length, 50)

    def testUserEmailLength(self):
        file = UploadFile.objects.get(id=1)
        max_length = file._meta.get_field('email').max_length
        self.assertEqual(max_length, 50)

    def testUserExplanationLength(self):
        file = UploadFile.objects.get(id=1)
        max_length = file._meta.get_field('explanation').max_length
        self.assertEqual(max_length, 300)

    def testUserStatusLength(self):
        file = UploadFile.objects.get(id=1)
        max_length = file._meta.get_field('status').max_length
        self.assertEqual(max_length, 3)

    def testUserStatus(self):
        file = UploadFile.objects.get(id=1)
        self.assertEqual(file.status, "New")


class TestImproperFile(TestCase):
    def testWrongFileType(self):
        self.assertRaisesMessage("Error message", UploadFile.objects.create(name='test', picture="test.py"))

class TestUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='test', password='<PASSWORD>')

    def testUserPermissonsName(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('user_permissions').verbose_name
        self.assertEqual(field_label, "user permissions")

    def testIsAdminName(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('is_admin').verbose_name
        self.assertEqual(field_label, "site admin status")

    def testIsUserName(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('is_user').verbose_name
        self.assertEqual(field_label, "user status")
