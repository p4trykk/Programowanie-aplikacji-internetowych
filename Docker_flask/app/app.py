from flask import Flask, render_template, request

app = Flask(__name__)

# Strona główna z formularzem
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        imie = request.form.get('imie')
        nazwisko = request.form.get('nazwisko')
        status = request.form.get('status')
        wiadomosc = request.form.get('wiadomosc')
        
        return f'<h1>Dziękujemy, {imie} {nazwisko}!</h1>' \
               f'<p>Status: {status}</p>' \
               f'<p>Twoja wiadomość: {wiadomosc}</p>'
    
    return '''
    <h2>Formularz Kontaktowy</h2>
    <form method="POST">
        <label for="imie">Imię:</label><br>
        <input type="text" id="imie" name="imie" required><br><br>

        <label for="nazwisko">Nazwisko:</label><br>
        <input type="text" id="nazwisko" name="nazwisko" required><br><br>

        <label for="status">Status:</label><br>
        <select id="status" name="status">
            <option value="Student">Student</option>
            <option value="Pracujący">Pracujący</option>
            <option value="Bezrobotny">Bezrobotny</option>
        </select><br><br>

        <label for="wiadomosc">Wiadomość:</label><br>
        <textarea id="wiadomosc" name="wiadomosc" rows="4" cols="50" required></textarea><br><br>

        <button type="submit">Wyślij Formularz</button>
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
