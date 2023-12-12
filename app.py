from flask import Flask, render_template, url_for, request, redirect
from flask_apscheduler import APScheduler

from logging import  FileHandler, INFO, DEBUG

from bd import session
from Entity.User import User
from Entity.Doctor import Doctor
from Entity.Record import Record

from datetime import datetime, timedelta

file_handler = FileHandler("records.log")
file_handler.setLevel(DEBUG)

app = Flask(__name__)

app.logger.addHandler(file_handler)
app.logger.setLevel(DEBUG)
app.logger.propagate = False

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            user_id = session.query(User.id).filter(
                User.name == request.form['user_name']).scalar()
            doctor_id = session.query(Doctor.id).filter(
                Doctor.name == request.form['doctor_name']).scalar()
            datetime = request.form['datetime']
            record_count = session.query(Record).filter(
                Record.doctor_id == doctor_id, Record.slot == datetime, Record.user_id == None).count()
            if record_count != 1:
                return render_template("index.html", mes="При добавлении записи произошла ошибка")
            session.query(Record).filter(Record.doctor_id == doctor_id, Record.slot == datetime, Record.user_id == None).\
                update({"user_id": user_id}, synchronize_session='fetch')
            session.commit()
            return redirect('/record')
        except:
            return render_template("index.html", mes="При добавлении записи произошла ошибка")
    else:
        return render_template("index.html")


@app.route('/user')
def user_all():
    user = session.query(User).all()
    return render_template("users.html", list=user)


@app.route('/doctor')
def doctor_all():
    doctor = session.query(Doctor).all()
    return render_template("doctors.html", list=doctor)


@app.route('/record')
def record_all():
    record_free = (session.query(Record.slot, Doctor.name, Doctor.spec)
                   .select_from(Record, Doctor)
                   .filter(Record.user_id == None)
                   .join(Doctor, Doctor.id == Record.doctor_id)
                   .all()
                   )
    record_busy = (session.query(Record.slot, Doctor.name.label('doc_name'), Doctor.spec, User.name)
                   .select_from(Record, Doctor, User)
                   .join(Doctor, Doctor.id == Record.doctor_id)
                   .join(User, User.id == Record.user_id)
                   .all()
                   )
    return render_template("records.html", list_free=record_free, list_busy=record_busy)


def job():
    records = (session.query(Record.slot, Doctor.name.label('doc_name'), Doctor.spec, User.name)
               .select_from(Record, Doctor, User)
               .join(Doctor, Doctor.id == Record.doctor_id)
               .join(User, User.id == Record.user_id)
               .all()
               )
    for record in records:
        # current date and time
        now: datetime = datetime.now().replace(microsecond=0, second=0)
        if record.slot - now == timedelta(days=1, hours=0, minutes=0):
            app.logger.info(f"Здравствуйте, {record.name}! Напоминаем, Вы записаны завтра в {record.slot }!")
        if record.slot - now == timedelta(hours=2):
            app.logger.info(f"Здравствуйте, {record.name}! Вам через 2 часа на прием!")
    return

if __name__ == "__main__":
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='test-job', func=job, trigger='interval', seconds=60)
    app.run(debug=False)
