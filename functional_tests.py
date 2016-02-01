from selenium import webdriver
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

        self.fail('Finish the test!')
        # Edith is invited to enter a to-do item straight away
        # She types "Buy Peacock Feathers" into a text box

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy Peacock Feathers" as an item in a to-do list

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly"

        # The page then updates again, and now shows both items on her list

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She then visits that url - her to-do list is still there

        # Satisfied, she then goes back to sleep

if __name__ == '__main__':
    unittest.main()
