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
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy Peacock Feathers" as an item in a to-do list


        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly"
        # The page then updates again, and now shows both items on her list

        self.check_for_row_in_list_table('1: Buy Peacock Feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')


        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She then visits that url - her to-do list is still there

        # Satisfied, she then goes back to sleep
        self.fail('Finish the test!')

