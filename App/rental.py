from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/music_rental'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model Database
class Instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Boolean, default=True)

# Route untuk menampilkan semua alat musik
@app.route('/')
def index():
    instruments = Instrument.query.all()
    return render_template('index.html', instruments=instruments)

# Route untuk menambahkan alat musik baru
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        price_per_day = request.form['price_per_day']
        new_instrument = Instrument(name=name, type=type, price_per_day=price_per_day, availability=True)
        db.session.add(new_instrument)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# Route untuk memperbarui alat musik
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    instrument = Instrument.query.get(id)
    if request.method == 'POST':
        instrument.name = request.form['name']
        instrument.type = request.form['type']
        instrument.price_per_day = request.form['price_per_day']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', instrument=instrument)

# Route untuk menghapus alat musik
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    instrument = Instrument.query.get(id)
    db.session.delete(instrument)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
