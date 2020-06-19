from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.auth.models import User
import time

MAX_WAIT = 10

class EditCVTest (LiveServerTestCase):

	def setUp (self):
		self.browser = webdriver.Firefox()
			
		#login
		User.objects.create_user('dan', 'dan.turner.djt@gmail.com', 'test')
		self.client.login (username='dan', password='test')
		cookie = self.client.cookies['sessionid']
		self.browser.get(self.live_server_url + '/admin/')  #selenium will set cookie domain based on current page domain
		self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
		self.browser.refresh() #need to update page for logged in user
		self.browser.get(self.live_server_url + '/admin/')

	def tearDown (self):
		self.browser.quit()



	def test_can_add_an_entry (self):
		# Dan wants to visit his website to update his online CV. First he visits its home page
		self.browser.get(self.live_server_url)
		

		# He notices the CV page and naviagates to it, noticing that the new page title mentions CVs
		self.browser.find_element_by_link_text("CV").click()
		time.sleep (1)
		header_text = self.browser.find_element_by_class_name ('page-title').text
		self.assertIn ('CV', header_text)

		# He tries to create a new entry for the projects section
		plus_button = self.browser.find_element_by_css_selector ('span.glyphicon-plus')
		plus_button.click()
		
		
		# He selects projects from the section selection list
		time.sleep (1)
		self.browser.find_element_by_xpath("//select[@id='id_section']/option[text()='Projects']").click()

		# He types "Website" into the title box and "Made a website" into the text box 
		titleBox = self.browser.find_element_by_id('id_title')
		titleBox.send_keys ('Website')
		textBox = self.browser.find_element_by_id('id_text')
		textBox.send_keys ('Made a website')

		#Finally he preses the "Save" button to submit what he has entered
		save_button = self.browser.find_element_by_class_name ('btn-default')
		save_button.click()
		
		# After submitting, he sees that the page has redirected to the drafts list page where he see can what he just submitted
		time.sleep(1)
		entry = self.browser.find_element_by_css_selector ('div.entry')
		title_text = entry.find_element_by_tag_name('h2').text
		text_text = entry.find_element_by_tag_name('p').text
		self.assertIn ('Website', title_text)
		self.assertIn ('Made a website', text_text)
		
		
		# Looking at it, he decides to be a little more specific, so clicks on the edit button in order to expand on it
		edit_button = self.browser.find_element_by_css_selector ('span.glyphicon-pencil')
		edit_button.click()

		
		# He adds "using django" into the text box and presses save again
		time.sleep (1)
		textBox = self.browser.find_element_by_id('id_text')
		textBox.send_keys (' using django')

		save_button = self.browser.find_element_by_class_name ('btn-default')
		save_button.click()

			
		#Back on the drafts list page, he can see that his entry has been updated with the extra text he entered
		time.sleep(1)
		entry = self.browser.find_element_by_css_selector ('div.entry')
		text_text = entry.find_element_by_tag_name('p').text
		self.assertIn ('Made a website using django', text_text)


		#Happy with his entry, he presses the "Publish" button to publish it on the public page
		publish_button = self.browser.find_element_by_link_text ('Publish')
		publish_button.click()		


		# After publishing, he returns to the main CV page where he can see his published entry
		time.sleep (1)
		self.browser.find_element_by_link_text("CV").click()
		time.sleep (1)
		entry = self.browser.find_element_by_css_selector ('div.entry')
		text_text = entry.find_element_by_tag_name('p').text
		self.assertIn ('Made a website using django', text_text)


		# He decides to add another entry, this time to the education section, so presses the plus button, selects education from the section list, types in the details, save it, and submits it like last time
		plus_button = self.browser.find_element_by_css_selector ('span.glyphicon-plus')
		plus_button.click()
		time.sleep (1)
		self.browser.find_element_by_xpath("//select[@id='id_section']/option[text()='Education']").click()
		titleBox = self.browser.find_element_by_id('id_title')
		titleBox.send_keys ('Nursery')
		textBox = self.browser.find_element_by_id('id_text')
		textBox.send_keys ('I went to nursery')
		save_button = self.browser.find_element_by_class_name ('btn-default')
		save_button.click()
		time.sleep (1)
		publish_button = self.browser.find_element_by_link_text ('Publish')
		publish_button.click()
			
		
		# After publishing, he returns to the main CV page where he can see both the first entry and his new second published entry
		time.sleep (1)
		self.browser.find_element_by_link_text("CV").click()
		time.sleep (1)
		entries = self.browser.find_elements_by_css_selector ('div.entry')
		self.assertIn ('nursery', entries[0].find_element_by_tag_name('p').text)
		self.assertIn ('website', entries[1].find_element_by_tag_name('p').text)


		#He decides that he doesn't like his new entry, and wants to delete, so he goes to the edit-list, clicks the entry and then clicks the delete button
		edit_list_button = self.browser.find_element_by_css_selector ('span.glyphicon-edit')
		edit_list_button.click()
		time.sleep (1)
		self.browser.find_element_by_link_text("Nursery").click()
		time.sleep (1)
		
		edit_button = self.browser.find_element_by_css_selector ('span.glyphicon-remove')
		edit_button.click()
		

		# Returning to the main list page, he can see that the only entry still there is his orignal entry
		time.sleep (1)
		entries = self.browser.find_elements_by_css_selector ('div.entry')
		self.assertNotIn ('nursery', entries[0].find_element_by_tag_name('p').text)
		self.assertIn ('website', entries[0].find_element_by_tag_name('p').text)
		




