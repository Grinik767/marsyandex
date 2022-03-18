from data import db_session
from data.jobs import Jobs
from data.users import User


def main():
    db_session.global_init("db/mars.db")
    db_sess = db_session.create_session()

    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    db_sess.add(user)

    user1 = User()
    user1.surname = "Kiselev"
    user1.name = "Grigorii"
    user1.age = 18
    user1.position = "captain1"
    user1.speciality = "pilot"
    user1.address = "module_2"
    user1.email = "kiselev_grig@mars.org"
    db_sess.add(user1)

    user2 = User()
    user2.surname = "Parker"
    user2.name = "Scotti"
    user2.age = 40
    user2.position = "captain2"
    user2.speciality = "engineer"
    user2.address = "module_3"
    user2.email = "scotti@mars.org"
    db_sess.add(user2)

    user3 = User()
    user3.surname = "Parker"
    user3.name = "Tom"
    user3.age = 30
    user3.position = "captain3"
    user3.speciality = "engineer biologist"
    user3.address = "module_4"
    user3.email = "tom@mars.org"
    db_sess.add(user3)

    job = Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False
    db_sess.add(job)

    job1 = Jobs()
    job1.team_leader = 2
    job1.job = 'deployment smth'
    job1.work_size = 25
    job1.collaborators = '3, 5'
    job1.is_finished = True
    db_sess.add(job1)

    db_sess.commit()


if __name__ == '__main__':
    main()
