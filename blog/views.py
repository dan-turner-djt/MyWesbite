from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .models import CVEntry
from .forms import PostForm
from .forms import CVEntryForm


def home (request):
	return render (request, 'home.html')



def post_list (request):
	posts = Post.objects.filter (published_date__lte=timezone.now()).order_by('-published_date')
	return render (request, 'blog/post_list.html', {'posts': posts})


def post_detail (request, pk):
	post = get_object_or_404 (Post, pk=pk)
	return render (request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new (request):
	if request.method == "POST":
		form = PostForm (request.POST)
		if form.is_valid():
			post = form.save (commit=False)
			post.author = request.user
			post.save()
			return redirect ('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render (request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')




def entry_list (request):
	entries = CVEntry.objects.filter (published_date__lte=timezone.now()).order_by('-published_date')
	introductionEntries = []
	technicalSkillsEntries = []
	educationEntries = []
	workExperienceEntries = []
	projectsEntries = []

	for entry in entries:
		if entry.section == 'Introduction':
			introductionEntries.append(entry)
		elif entry.section == 'Technical skills':
			technicalSkillsEntries.append(entry)
		elif entry.section == 'Education':
			educationEntries.append(entry)
		elif entry.section == 'Work Experience':
			workExperienceEntries.append(entry)
		elif entry.section == 'Projects':
			projectsEntries.append(entry)
			
	return render (request, 'cv/entry_list.html', {'introductionEntries': introductionEntries, 'technicalSkillsEntries': technicalSkillsEntries, 'educationEntries': educationEntries, 'workExperienceEntries': workExperienceEntries, 'projectsEntries': projectsEntries})


def entry_detail (request, pk):
	entry = get_object_or_404 (CVEntry, pk=pk)
	return render (request, 'cv/entry_detail.html', {'entry': entry})


@login_required
def entry_new (request):
	if request.method == "POST":
		form = CVEntryForm (request.POST)
		if form.is_valid():
			entry = form.save (commit=False)
			entry.save()
			return redirect ('entry_detail', pk=entry.pk)
	else:
		form = CVEntryForm()
	return render (request, 'cv/entry_edit.html', {'form': form})


@login_required
def entry_edit(request, pk):
	entry = get_object_or_404(CVEntry, pk=pk)
	if request.method == "POST":
		form = CVEntryForm(request.POST, instance=entry)
		if form.is_valid():
			entry = form.save(commit=False)
			entry.save()
			return redirect('entry_detail', pk=entry.pk)
	else:
		form = CVEntryForm(instance=entry)
	return render(request, 'cv/entry_edit.html', {'form': form})


@login_required
def entry_edit_list(request):
    entries = CVEntry.objects.filter(created_date__isnull=False).order_by('-published_date')
    return render(request, 'cv/entry_edit_list.html', {'entries': entries})


@login_required
def entry_publish(request, pk):
    entry = get_object_or_404(CVEntry, pk=pk)
    entry.publish()
    return redirect('entry_detail', pk=pk)


@login_required
def entry_remove(request, pk):
    entry = get_object_or_404(CVEntry, pk=pk)
    entry.delete()
    return redirect('CV_entry_list')
