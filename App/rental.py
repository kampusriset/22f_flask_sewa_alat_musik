from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental.db'
db = SQLAlchemy(app)

# Model Database User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Model Database Instrument
class Instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    price_per_day = db.Column(db.Integer, nullable=False)

# Halaman Login
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Username atau Password salah!")
    
    return render_template('login.html')

# Halaman Registrasi
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Username sudah digunakan!")

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

# Halaman Lupa Password
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if user:
            return render_template('forgot_password.html', message="Reset password berhasil!")
        else:
            return render_template('forgot_password.html', error="Username tidak ditemukan!")
    
    return render_template('forgot_password.html')

# Halaman Utama (Index)
@app.route('/index')
def index():
    if 'username' in session:
        instruments = Instrument.query.all()
        return render_template('index.html', username=session['username'], instruments=instruments)
    return redirect(url_for('login'))

# Halaman Tambah Alat Musik
@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        price_per_day = request.form['price_per_day']
        
        new_instrument = Instrument(name=name, type=type, price_per_day=price_per_day)
        db.session.add(new_instrument)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if 'username' not in session:
        return redirect(url_for('login'))

    instrument = Instrument.query.get_or_404(id)
    db.session.delete(instrument)
    db.session.commit()

    return redirect(url_for('index'))


# Halaman Edit Alat Musik
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    instrument = Instrument.query.get_or_404(id)
    
    if request.method == 'POST':
        instrument.name = request.form['name']
        instrument.type = request.form['type']
        instrument.price_per_day = request.form['price_per_day']
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit.html', instrument=instrument)

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
