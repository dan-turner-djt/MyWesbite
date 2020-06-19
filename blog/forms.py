from django import forms
from .models import Post
from .models import CVEntry

class PostForm (forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title', 'text',)


SECTIONS = [
	('Introduction', 'Introduction'),
	('Technical skills', 'Technical skills'),
	('Education', 'Education'),
	('Work Experience', 'Work Experience'),
	('Projects', 'Projects'),
]


class CVEntryForm (forms.ModelForm):
	
	class Meta:
		model = CVEntry
		widgets = {'section': forms.Select(choices=SECTIONS)}
		fields = ('title', 'start_date', 'end_date', 'location', 'text', 'section')
		
