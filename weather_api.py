import requests
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from sqlalchemy import Column ,create_engine , String, ForeignKey, Date

from sqlalchemy.orm import sessionmaker, Mapped
import flask_wtf
import wtforms
from flask import request, Flask, render_template, url_for, redirect,session,jsonify
from wtforms import StringField, SubmitField, IntegerField, PasswordField , DateField
from sqlalchemy.orm import DeclarativeBase , sessionmaker, Mapped, mapped_column
from wtforms.validators import InputRequired
api_key = "6ef4e7612bde555867a4a6aa9c2fe746"

engine = create_engine('sqlite:///weather1.db', echo=True)
Session = sessionmaker(bind=engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = '07031986'
class Base(DeclarativeBase):
    def create_db(self):
        Base.metadata.create_all(engine)

    def drop_db(self):
        Base.metadata.drop_all(engine)
class City(flask_wtf.FlaskForm):
    city = wtforms.StringField('Введіть місто', validators=[wtforms.validators.InputRequired()])
    submit = wtforms.SubmitField('Goo!')

class Submit(flask_wtf.FlaskForm):
    submit = wtforms.SubmitField('Дізнатися погоду')

class text(Base):
    __tablename__ = "text"
    id: Mapped[int] = mapped_column(primary_key=True)
    text1: Mapped[int] = mapped_column(String(80))
    user_id: Mapped[int] = mapped_column(ForeignKey('log.id'))

@app.route('/')
def f_1():
    return render_template('host.html')
@app.route('/weather_pg')
def f_6():
    return render_template('weather_pg1.html')

@app.route('/weather', methods = ['POST'])
def f_7():
    city = request.form['text']
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    res = requests.get(url)
    if res.status_code == 200:
        data1 = res.json()
        session1 = session.get('list', [])
        if city not in session1:
            session1.append(city)
            session['list'] = session1
        data = {'Тeмпература': f'{round(data1["main"]["temp"] - 273, 1)}',"Вологість" : f'{data1["main"]["humidity"]}', 'Швидкість вітру:' : f'{data1["wind"]["speed"]}'}

    else:
        data = {'Тeмпература': f'Виникла помилка('}
    return jsonify(data), 200

# base =Base()
# base.create_db()

if __name__ == '__main__':
    app.run(debug=True, port=8000)