from flask import Flask, request, session, jsonify, render_template, redirect, url_for
from sqlalchemy import create_engine, Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_mail import Mail, Message
from config import MAIL, MAIL_PASSWORD

app = Flask(__name__)
app.secret_key = '203965'

engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)


Base.metadata.create_all(engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = '12212112'
app.config['MAIL_SERVER'] = 'smtp.ukr.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = MAIL
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/')
def index():
    return render_template('index1.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(user)
        session.commit()
        msg = Message('Ласкаво просимо в наш додаток!', recipients=[email])
        msg.body = f'Дякуємо за реєстрацію! Ваш логін: {username}, Ваш пароль: {password}'
        mail.send(msg)

        return jsonify({'message': 'Користувач успішно зареєстрований'})
    else:
        return render_template('signup.html')

@app.route('/cc')
def f_76():
    print('змінна')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        Session = sessionmaker(bind=engine)
        db_session = Session()
        user = db_session.query(User).filter_by(username=username, password=password).first()

        if user:
            session['logged_in'] = True
            db_session.close()
            return jsonify({'message': 'Вхід успішний'})


        else:
            db_session.close()
            return jsonify({'message': 'Неправильне ім`я користувача або пароль'}), 401
    else:
        return render_template('login.html')



@app.route('/crypto')
def crypt():
    return render_template('crypto.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'Потрібен текст для шифрування'}), 400

    encrypted_text = cipher_suite.encrypt(text.encode()).decode()
    return jsonify({'encrypted_text': encrypted_text}), 200


@app.route('/decrypt', methods=['POST'])
def decrypt():
    # encrypted_text = request.form['encrypted_text']
    text1 = request.form.get('text1')
    # if not encrypted_text:
    if not text1:
        return jsonify({'error': 'Потрібен зашифрований текст'}), 400

    # decrypted_text = cipher_suite.decrypt(encrypted_text.encode()).decode()
    decrypted_text = cipher_suite.decrypt(text1.encode()).decode()

    return jsonify({'decrypted_text': decrypted_text}), 200






if __name__ == '__main__':
    app.run(debug=True, port=7000)
