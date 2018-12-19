from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    """Strona domowa dla Learning Log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Pokaż wszystkie tematy"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Pokaż pojedynczy temat i wszystkie jego wpisy"""
    topic = Topic.objects.get(id=topic_id)
    # Sprawdź czy temaat należy do zalogowanego użytkownika
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic' : topic, 'entries' : entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Dodaj nowy temat"""
    if request.method != 'POST':
        # Brak przekazanych danych, utwórz pusty formularz
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Dodaj nowy wpis"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # Brak przekazanych danych, utwórz pusty formularz
        form = EntryForm()
    else:
        # Dane POST przesłane, przetwórz dane
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic_id]))

    context = {'topic' : topic, 'form' : form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edytuj istniejący wpis"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    topic_id = topic.id

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Wstępne żądanie; wypełnij wcześniej istniejącym wpisem
        form = EntryForm(instance=entry)
    else:
        # Dane POST przesłane, przetwórz dane
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic_id]))
    context = {'entry' : entry, 'topic' : topic, 'form' : form}
    return render(request, 'learning_logs/edit_entry.html', context)
