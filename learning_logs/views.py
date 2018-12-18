from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    """Strona domowa dla Learning Log"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Pokaż wszystkie tematy"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """Pokaż pojedynczy temat i wszystkie jego wpisy"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic' : topic, 'entries' : entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """Dodaj nowy temat"""
    if request.method != 'POST':
        # Brak przekazanych danych, utwórz pusty formularz
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

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

def edit_entry(request, entry_id):
    """Edytuj istniejący wpis"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    topic_id = topic.id

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
