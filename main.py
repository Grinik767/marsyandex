from flask import Flask, render_template, redirect, request, abort, jsonify, make_response
from flask_restful import reqparse, abort, Api, Resource
from data.users_resource import UsersResource, UsersListResource
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
import api
import os
from data.users import User
from data.jobs import Jobs
from forms.user import LoginForm, RegisterForm
from forms.job import AddingJob

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api_v2 = Api(app)
db_session.global_init('db/mars.db')
app.register_blueprint(api.blueprint)
db_sess = db_session.create_session()
login_manager = LoginManager()
login_manager.init_app(app)

api_v2.add_resource(UsersListResource, '/api/v2/users')
api_v2.add_resource(UsersResource, '/api/v2/users/<int:users_id>')


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Login', form=form)


@app.route('/')
def main():
    jobs = db_sess.query(Jobs).all()
    cur_jobs = []
    for job in jobs:
        leader = db_sess.query(User).filter(User.id == job.team_leader).first()
        leader1 = f"{leader.surname} {leader.name}"
        is_fin = job.is_finished
        if is_fin:
            is_fin = 'is finished'
            color = 3
        else:
            is_fin = 'is not finished'
            color = 2
        cur_jobs.append(
            [f"Action # {jobs.index(job) + 1}", job.job, leader1, f"{job.work_size} hours", job.collaborators, is_fin,
             job.id, color,
             leader.id])

    return render_template('jobs.html', jobs=cur_jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    form = AddingJob()
    if form.validate_on_submit():
        job = Jobs(
            job=form.title.data,
            work_size=form.work_size.data,
            collaborators=form.collabs.data,
            team_leader=form.tl_id.data,
            is_finished=form.is_fin.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Add a job', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = AddingJob()
    if request.method == "GET":
        job = db_sess.query(Jobs).filter((Jobs.id == id),
                                         ((Jobs.team_leader == current_user.id) | (current_user.id == 1))).first()
        if job:
            form.title.data = job.job
            form.work_size.data = job.work_size
            form.collabs.data = job.collaborators
            form.tl_id.data = job.team_leader
            form.is_fin.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        job = db_sess.query(Jobs).filter((Jobs.id == id),
                                         ((Jobs.team_leader == current_user.id) | (current_user.id == 1))).first()
        if job:
            job.job = form.title.data
            job.work_size = form.work_size.data
            job.collaborators = form.collabs.data
            job.team_leader = form.tl_id.data
            job.is_finished = form.is_fin.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addjob.html',
                           title='Edit a job', form=form
                           )


@app.route('/jobs/<int:id>/delete')
@login_required
def delete_job(id):
    job = db_sess.query(Jobs).filter((Jobs.id == id),
                                     ((Jobs.team_leader == current_user.id) | (current_user.id == 1))).first()
    db_sess.delete(job)
    db_sess.commit()
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
