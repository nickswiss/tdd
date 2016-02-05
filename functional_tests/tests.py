#
# Functional Tests
# Nick Arnold
#
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import TestCase
import unittest


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_list_and_retrieve(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Edith is invited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        # She types "Buy Peacock Feathers" into a text box
        input_box.send_keys('Buy Peacock Feathers')
        input_box.send_keys(Keys.ENTER)

        # When she hits enter, she is taken to a new URL and the page now lists
        # "1: Buy Peacock Feathers" as an item in a to-do list
        ediths_url = self.browser.current_url
        self.assertRegexpMatches(ediths_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy Peacock Feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly"

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)

        # The page then updates again, and now shows both items on her list

        self.check_for_row_in_list_table('1: Buy Peacock Feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Now a new user, Francis, comes along to the site.
        # We use a new browser session to make sure that no information of
        # Edith's is coming through from cookies, etc

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Edith's list

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_elements_by_tag_name('body')

        self.assertNotIn('Buy Peacock Feathers', page_text)
        self.assertNotIn('Make a fly', page_text)

        # Francis starts a new list by entering a new item

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)

        # Francis gets his own unique URL

        francis_url = self.browser.current_url
        self.assertRegexpMatches(francis_url, '/lists/.+')
        self.assertNotEqual(francis_url, ediths_url)


        # Again there is no trace of Edith's list

        page_text = self.browser.find_elements_by_tag_name('body')
        self.assertNotIn('Buy Peacock Feathers', page_text)
        self.assertNotIn('Make a fly', page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 512, delta=5)
        input_box.send_keys('testing\n')

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 512, delta=5)