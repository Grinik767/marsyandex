import flask
from flask import jsonify, request

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=(
                    'id', 'job', 'work_size', 'collaborators', 'start_date', 'finish_date', 'is_finished',
                    'team_leader'))
                    for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_job(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': job.to_dict(only=(
                'id', 'job', 'work_size', 'collaborators', 'start_date', 'finish_date', 'is_finished',
                'team_leader'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'work_size', 'collaborators', 'is_finished',
                  'team_leader']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job_check = db_sess.query(Jobs).get(request.json['id'])
    if job_check:
        return jsonify({'error': 'Id already exists'})
    job = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        team_leader=request.json['team_leader']
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_job(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def edit_job(jobs_id):
    json = request.json
    if not json:
        return jsonify({'error': 'Empty request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return jsonify({'error': 'Not found'})
    else:
        params_to_change = ['collaborators', 'is_finished', 'job', 'team_leader', 'work_size', 'start_date',
                            'finish_date']
        if all([p in params_to_change for p in json]):
            if params_to_change[0] in json:
                job.collaborators = json['collaborators']
            if params_to_change[1] in json:
                job.is_finished = json['is_finished']
            if params_to_change[2] in json:
                job.job = json['job']
            if params_to_change[3] in json:
                job.team_leader = json['team_leader']
            if params_to_change[4] in json:
                job.work_size = json['work_size']
            if params_to_change[5] in json:
                job.start_date = json['start_date']
            if params_to_change[6] in json:
                job.finish_date = json['finish_date']
            db_sess.commit()
            return jsonify({'success': 'OK'})
        else:
            return jsonify({'error': 'Bad request'})
