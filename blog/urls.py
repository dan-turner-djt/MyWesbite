from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	
	path('blog', views.post_list, name='blog_post_list'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/new/', views.post_new, name='post_new'),
	path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
	path('drafts/', views.post_draft_list, name='post_draft_list'),
	path('post/<pk>/publish/', views.post_publish, name='post_publish'),
	path('post/<pk>/remove/', views.post_remove, name='post_remove'),
	
	path('CV', views.entry_list, name='CV_entry_list'),
	path('entry/<int:pk>/', views.entry_detail, name='entry_detail'),
	path('entry/new/', views.entry_new, name='entry_new'),
	path('entry/<int:pk>/edit/', views.entry_edit, name='entry_edit'),
	path('CV/editlist', views.entry_edit_list, name='entry_edit_list'),
	path('entry/<pk>/publish/', views.entry_publish, name='entry_publish'),
	path('entry/<pk>/remove/', views.entry_remove, name='entry_remove'),
]
