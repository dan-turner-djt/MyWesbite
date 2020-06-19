from django.test import TestCase
from django.urls import resolve
from django.urls import reverse
from django.http import HttpRequest
from blog.models import CVEntry
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from blog.views import entry_list

# Create your tests here.


class CV_Test (TestCase):


	def setUp (self):
		User.objects.create_user('dan', 'dan.turner.djt@gmail.com', 'test')
		login = self.client.login (username='dan', password='test')
		self.response = login
		
	def test_logged_in (self):
		self.assertTrue(self.response)


	def test_cv_url_resolves_to_cv_page_view (self):
		found = resolve ('/CV')
		self.assertEqual (found.func, entry_list)

	def test_uses_cv_base_template(self):
		response = self.client.get('/CV')
		self.assertTemplateUsed(response, 'cv/base.html')

	def test_uses_entry_list_template(self):
		response = self.client.get('/CV')
		self.assertTemplateUsed(response, 'cv/entry_list.html')

	def test_can_save_a_POST_request(self):
		response = self.client.post(reverse('entry_new'), data={'title': 'newEntry', 'text': 'A new list entry', 'section': 'Introduction'}) 
		self.assertEqual(response.status_code, 302)
		self.assertEqual (CVEntry.objects.count(), 1)
		new_entry = CVEntry.objects.first()
		self.assertEqual (new_entry.text, 'A new list entry')

	def test_redirects_to_entry_detail_after_POST (self):
		response = self.client.post(reverse('entry_new'), data={'title': 'newEntry', 'text': 'A new list entry', 'section': 'Introduction'})
		self.assertEqual (response.status_code, 302)
		self.assertEqual (response['location'], '/entry/1/')
	
	def test_only_saves_entries_when_necessary (self):
		self.client.get('/CV')
		self.assertEqual (CVEntry.objects.count(), 0)

	def test_displays_all_unpublished_entries_in_drafts_list (self):
		CVEntry.objects.create(title = 'entry 1', text='this is entry 1', section='Introduction')
		CVEntry.objects.create(title = 'entry 2', text='this is entry 2', section='Education')

		response = self.client.get('/CV/editlist')

		self.assertIn('this is entry 1', response.content.decode())
		self.assertIn('this is entry 2', response.content.decode())


	def test_displays_all_entries_with_published_date_in_main_list (self):
		CVEntry.objects.create(title = 'entry 1', text='this is entry 1', published_date=timezone.now(), section='Introduction')
		CVEntry.objects.create(title = 'entry 2', text='this is entry 2', published_date=timezone.now(), section='Education')

		response = self.client.get('/CV')

		self.assertIn('this is entry 1', response.content.decode())
		self.assertIn('this is entry 2', response.content.decode())


	def test_edited_entry_updates_in_main_list_and_drafts_list (self):
		CVEntry.objects.create(title = 'entry 1', text='this is entry 1', published_date=timezone.now(), section='Introduction')
		
		CVEntry.objects.filter(title='entry 1').update(text='this entry has been edited')
		
		response = self.client.get('/CV')
		self.assertIn('this entry has been edited', response.content.decode())
		
		response = self.client.get('/CV/editlist')
		self.assertIn('this entry has been edited', response.content.decode())

	
	def test_deleted_entries_no_longer_show_in_main_list_or_drafts_list (self):
		CVEntry.objects.create(title = 'entry 1', text='this is entry 1', published_date=timezone.now(), section='Introduction')
		
		CVEntry.objects.filter(title='entry 1').delete()
		
		response = self.client.get('/CV')
		self.assertNotIn('this is entry 1', response.content.decode())
		
		response = self.client.get('/CV/editlist')
		self.assertNotIn('this is entry 1', response.content.decode())
		


class EntryModelTest (TestCase):

	def test_saving_and_retrieving_entries (self):
		first_entry = CVEntry()
		first_entry.text = 'The first entry'
		first_entry.save()

		second_entry = CVEntry()
		second_entry.text = 'Entry second'
		second_entry.save()

		saved_entries = CVEntry.objects.all()
		self.assertEqual(saved_entries.count(), 2)

		first_saved_entry = saved_entries[0]
		second_saved_entry= saved_entries[1]
		self.assertEqual(first_saved_entry.text, 'The first entry')
		self.assertEqual(second_saved_entry.text, 'Entry second')

	
	def test_publishing_and_setting_published_date_for_entries (self):
		first_entry = CVEntry()
		first_entry.text = 'The first entry'
		first_entry.save()
		first_entry.publish()
		second_entry = CVEntry()
		second_entry.text = 'The first entry'
		second_entry.save()
		saved_entries = CVEntry.objects.all()
		self.assertFalse (saved_entries[0].published_date is None)
		self.assertTrue (saved_entries[1].published_date is None)
		

	
