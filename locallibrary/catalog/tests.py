from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Author, Book, BookInstance


class BookAdminInlineTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test-password",
        )
        self.client.force_login(self.admin_user)

        author = Author.objects.create(first_name="Test", last_name="Author")
        self.book = Book.objects.create(
            title="Current Book",
            author=author,
            summary="Test summary",
            isbn="1234567890123",
        )
        other_book = Book.objects.create(
            title="Other Book",
            author=author,
            summary="Other summary",
            isbn="3210987654321",
        )
        self.current_instance = BookInstance.objects.create(
            book=self.book,
            imprint="Current imprint",
        )
        self.other_instance = BookInstance.objects.create(
            book=other_book,
            imprint="Other imprint",
        )

    def test_inline_only_shows_instances_for_current_book(self):
        response = self.client.get(
            reverse("admin:catalog_book_change", args=[self.book.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.current_instance.pk))
        self.assertNotContains(response, str(self.other_instance.pk))
        self.assertContains(
            response,
            'name="bookinstance_set-TOTAL_FORMS" value="1"',
            html=True,
        )
