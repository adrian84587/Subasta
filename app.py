from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'clave_secreta'  


def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="Subasta",
        user="postgres",
        password="Adrian"
    )


@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('inicio.html')
    else:
        return redirect(url_for('login'))

#LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['user_id'] = user[0]  
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('home'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Sesión cerrada.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
