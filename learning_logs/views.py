from django.shortcuts import render, redirect
# A decorator is a directive placed just
# before a function definition that Python applies to the function before it
# runs, to alter how the function code behaves.
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm
# Create your views here.

def check_topic_owner(topic, request):
    if topic.owner != request.user:
        raise Http404

# Django passes the request object 
# to this view functions.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics."""
    # When a user is logged in, the request object has a request.user attribute set
    #  that stores information about the user.
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its asociated entries."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    check_topic_owner(topic, request)
    entries = topic.entry_set.order_by('-date_added') if topic is not None else None
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics') # View name
    

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Editing an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # Make sure that the entrie belongs to a logged in user.
    check_topic_owner(topic, request)

    if request.method != 'POST':
        # Initial request; pre-fill from with the current entry.

        # The argument(instance) tells Django to create the form
        # prefilled with information from the existing entry object.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.

        # When processing a POST request, we pass the instance=entry argument
        # and the data=request.POST argument. These arguments tell Django to create
        # a form instance based on the information associated with the existing
        # entry object, updated with any relevant data from request.POST.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

