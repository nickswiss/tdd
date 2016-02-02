from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_start_and_retrieve(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Edith is invited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        # She types "Buy Peacock Feathers" into a text box
        input_box.send_keys('Buy Peacock Feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy Peacock Feathers" as an item in a to-do list
        input_box.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn('1: Buy Peacock Feathers', [row.text for row in rows])

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly"
        # The page then updates again, and now shows both items on her list
        self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])


        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She then visits that url - her to-do list is still there

        # Satisfied, she then goes back to sleep
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()
