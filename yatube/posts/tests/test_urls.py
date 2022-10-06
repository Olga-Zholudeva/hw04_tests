from django.test import TestCase, Client
from django.contrib.auth import get_user_model


from ..models import Group, Post

User = get_user_model()


class PostUrlTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            pk=1,
            author=cls.user,
            group=cls.group,
            text='Тестовый текст'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username=self.user.username)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_availability_of_pages_and_template_names_for_non_authorized_users(self):
        url_addresses_templates_names = {
            '/': 'posts/index.html',
            '/group/test_slug/': 'posts/group_list.html',
            '/profile/test_user/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
        }
        for address, template in url_addresses_templates_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)

    def test_availability_of_pages_and_template_names_for_authorized_users(self):
        url_addresses_templates_names = {
            '/create/': 'posts/create_post.html',
            '/posts/1/edit/': 'posts/create_post.html',
        }
        for address, template in url_addresses_templates_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)

    def test_request_to_a_non_existent_page(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)
