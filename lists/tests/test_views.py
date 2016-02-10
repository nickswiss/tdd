from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List

class NewListTest(TestCase):

    def test_saving_a_POST(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % new_list.id)

    def test_can_save_a_POST_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/{0}/add_item'.format(correct_list.id),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{0}/add_item'.format(correct_list.id),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/{0}/'.format(correct_list.id))

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % list_.id)
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Item1', list=correct_list)
        Item.objects.create(text='Item2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='Other list item 1', list=other_list)
        Item.objects.create(text='Other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % correct_list.id)
        self.assertContains(response, 'Item1')
        self.assertContains(response, 'Item2')

        self.assertNotContains(response, 'Other list item 1')
        self.assertNotContains(response, 'Other list item 2')


class HomePageTest(TestCase):

    def test_root_url_resolves(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string(
            'home.html',
            # {'new_item_text': 'A new list item'},
            request=request
        )
        self.assertEqual(response.content.decode(), expected_html)


