from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from django import forms


from ..models import Group, Post

User = get_user_model()
COUNT_TEST_POST = 18
TEST_POST_ID = 1


class PostPegesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
        )
        test_posts = []
        for i in range(COUNT_TEST_POST):
            test_posts.append(Post(
                author=cls.user,
                group=cls.group,
                text=f'Тестовый текст поста {i + 1}'))
        Post.objects.bulk_create(test_posts)
        cls.templates_pages_names = {
            reverse(
                'posts:index'
            ): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': cls.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': cls.user.username}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': TEST_POST_ID}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': TEST_POST_ID}
            ): 'posts/create_post.html',
            reverse(
                'posts:post_create'
            ): 'posts/create_post.html',
        }

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username=self.user.username)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_users_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for reverse_name, template in self.templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_pages_users_correct_context_with_paginator(self):
        '''Проверка словаря context для страниц с паджинатором'''
        pages = [
            reverse('posts:index'),
            reverse(
                'posts:profile',
                kwargs={'username': self.user.username}),
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        ]
        for page in pages:
            respons_first_page = self.client.get(page)
            respons_second_page = self.client.get(page + '?page=2')
            self.assertEqual(
                len(respons_first_page.context['page_obj']),
                settings.LIMIT_POSTS
            )
            self.assertEqual(
                len(respons_second_page.context['page_obj']),
                COUNT_TEST_POST - settings.LIMIT_POSTS
            )

    def test_types_with_form_correct_context(self):
        '''Проверка словаря context на страницах с формой'''
        response_create = self.authorized_client.get(
            reverse('posts:post_create')
        )
        response_edit = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': TEST_POST_ID}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = (
                    response_create.context.get('form').fields.get(value)
                )
                self.assertIsInstance(form_field, expected)
                form_field = (
                    response_edit.context.get('form').fields.get(value)
                )
                self.assertIsInstance(form_field, expected)

    def test_post_detail_pages(self):
        '''Шаблон post_detail сформирован с правильным контекстом'''
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'post_id': TEST_POST_ID})
        )
        test_post = {
            response.context.get('post').author: self.user,
            response.context.get('post').group: self.group,
            response.context.get('post').text: 'Тестовый текст поста 1',
        }
        for value, expected in test_post.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_additional_verification_when_creating_a_post(self):
        '''При создании пост появляется на нужных страницах'''
        test_post = Post.objects.create(
            author=self.user,
            group=self.group,
            text='Проверочный пост',
        )
        pages = [
            reverse('posts:index'),
            reverse(
                'posts:profile',
                kwargs={'username': self.user.username}),
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        ]
        for reverse_name in pages:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                first_object = response.context['page_obj'][0]
                self.assertEqual(first_object.author, test_post.author)
                self.assertEqual(first_object.group, test_post.group)
                self.assertEqual(first_object.text, test_post.text)
