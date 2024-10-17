from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import News
from .forms import NewsForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    #  Pobranie pozycji z bazy danych
    news = News.objects.order_by('-create_time')
    # Stworzenie słownika przechowującego elementy bazy danych pod zmienną news
    context = {'news': news}
    # Przesłanie wyrenderowanej strony wraz z dodanymi elementami z bazy danych
    # elementy ze słownika context wykorzytywane są w pliku news/index.html 
    return render(request, 'news/index.html', context)

@login_required(login_url='/login/')
def add(request):
    # Sprawdzenie metody jaką przyszło zapytanie HTTP
    # Jeżeli POST - szukamy danych w ciele zapytania
    # Jeżeli GET - wysyłałym formularz do wypełnienia 
    # (można przesyłać dane w zapytaniu GET - 
    # ale w tym rozwiązaniu tego nie wykorzystujemy)
    if request.method == 'POST':
        
        # Formularze w Django umożliwiają sprawdzenie poprawności danych
        # więc tworzymy obiekt formularza z zapytania
        news = NewsForm(request.POST)

        # Jeżeli formularz - czyli dane przesłane z zapytania POST 
        # są proawidłowe dodajemy element do bazy danych 
        if news.is_valid():
            news = news.save(commit=False)
            news.author = request.user
            news.create_time = timezone.now()
            news.last_edit_time = timezone.now()
            news.save()
            return redirect('view_news')
        # Jeżeli nie są prawidłowe przesyłamy formularz z powrotem do kilenta 
        # Autmatyczny walidator tworzy również pola błędów, które są dostępne po
        # stronie klienta
        else:
            context = {'form': news}
            return render(request, 'news/add.html', context)
    
    # Jeżeli zapytanie typu GET przesyłamy pusty formularz
    else:
        news = NewsForm()
        context = {'form': news}
        return render(request, 'news/add.html', context)


def get(request, id):
    # funkcja get_object_or_404 zwraca element z bazy 
    # danych o danej wartości argumentu
    # lub przesłyła do kilenta błąd
    news = get_object_or_404(News, id=id)
    context = {'news': news}
    return render(request, 'news/view.html', context)