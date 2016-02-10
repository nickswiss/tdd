#
# Functional Tests
# Nick Arnold
#
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



class NewVisitorTest(FunctionalTest):

    def test_can_start_list_and_retrieve(self):
        self.browser.get(self.server_url)
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

        self.browser.get(self.server_url)
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

