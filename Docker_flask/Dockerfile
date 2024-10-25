# Użycie obrazu Pythona jako bazy
FROM python:3.9-slim

# Ustawienie katalogu roboczego w kontenerze
WORKDIR /app

# Skopiowanie plików aplikacji do kontenera
COPY app/ /app

# Instalacja Flask
RUN pip install flask

# Ustawienie portu dla kontenera
EXPOSE 5000

# Dodanie zmiennej środowiskowej Flask do trybu developerskiego
ENV FLASK_ENV=development

# Polecenie do uruchomienia aplikacji
CMD ["python", "app.py"]
