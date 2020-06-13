from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest (LiveServerTestCase):

	def setUp (self):
		self.browser = webdriver.Firefox()

	def tearDown (self):
		self.browser.quit()

	def wait_for_row_in_list_table (self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id ('id_list_table')
				rows = table.find_elements_by_tag_name ('tr')
				self.assertIn (row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep (0.5)


	def test_can_add_an_entry (self):
		# Dan wants to visit his website to update his online CV. First he visits its home page
		self.browser.get(self.live_server_url)

		# He notices the new page title and header mention CVs
		

		# He tries to create a new entry
		
		

		# He types "Made a website" into a text box (he just recently made one)
		

		# When he hits enter, the page updates, and now the page lists
		# "Made a website" as an entry in the CV
		
		

		# There is still a text box inviting him to add another entry. He
		# enters "Learnt how to follow TDD" (Dan has learnt to be very methodical)
		


		# The page updates again, and now shows both entries in his CV
		

		self.fail ('Finish the test!')




