from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    """Wyloguj użytykownika"""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
    """Zarejestruj nowego użytkownika"""
    if request.method != 'POST':
        # Pokaż pusty formularz rejestracji.
        form = UserCreationForm()
    else:
        # Przetwórz uzupełniony formularz.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Zaloguj użytkownika i przekieruj na stronę domową.
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form' : form}
    return render(request, 'users/register.html', context)
