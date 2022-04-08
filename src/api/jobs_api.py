from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_simple import jwt_required, get_jwt_identity
from data import db_session
from data.jobs import Jobs
from data.users import User


blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)
JOBFIELDS = ("id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished")


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs': [item.to_dict(only=JOBFIELDS) for item in jobs]
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
@jwt_required
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in JOBFIELDS):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    try:
        job = Jobs(
            id=int(request.json["id"]),
            team_leader=int(request.json["team_leader"]),
            job=str(request.json["job"]),
            work_size=int(request.json["work_size"]),
            collaborators=str(request.json["collaborators"]),
            start_date=datetime.fromisoformat(str(request.json["start_date"])),
            end_date=datetime.fromisoformat(str(request.json["end_date"])),
            is_finished=bool(request.json["is_finished"]),
        )

        if (db_sess.query(Jobs).get(job.id)):
            return jsonify({'error': 'Id already exists'})
        if (not db_sess.query(User).get(job.team_leader)):
            return jsonify({'error': 'Leader does not exists'})
        for user in job.collaborators.split(","):
            if (not db_sess.query(User).get(user)):
                return jsonify({'error': f'Collaborator with id "{user}" does not exists'})
        db_sess.add(job)
        db_sess.commit()
    except Exception:
        return jsonify({'error': 'Bad request'})
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:id>')
def get_job(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(id)
    if (not job):
        return jsonify({'error': 'Not found'})
    fields = ("id", "team_leader", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished")
    return jsonify(
        {
            'job': job.to_dict(only=fields)
        }
    )


@blueprint.route('/api/jobs/<int:id>', methods=['DELETE'])
@jwt_required
def delete_jobs(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(id)
    if (not job):
        return jsonify({'error': 'Not found'})
    userId = get_jwt_identity()
    if (job.team_leader != userId and userId != 1):
        return jsonify({'error': 'Forbidden'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:id>', methods=['PUT'])
@jwt_required
def edit_jobs(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(id)
    if (not job):
        return jsonify({'error': 'Not found'})
    userId = get_jwt_identity()
    if (job.team_leader != userId and userId != 1):
        return jsonify({'error': 'Forbidden'})
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not any(key in request.json for key in JOBFIELDS):
        return jsonify({'error': 'Bad request'})
    try:
        if ("id" in request.json):
            new_id = int(request.json["id"])
            if (db_sess.query(Jobs).get(new_id)):
                return jsonify({'error': 'Id already exists'})
            job.id = new_id
        if ("team_leader" in request.json):
            team_leader = request.json["team_leader"]
            if (not db_sess.query(User).get(team_leader)):
                return jsonify({'error': 'Leader does not exists'})
            job.team_leader = int(team_leader)
        if ("job" in request.json):
            job.job = str(request.json["job"])
        if ("work_size" in request.json):
            job.work_size = int(request.json["work_size"])
        if ("collaborators" in request.json):
            collaborators = request.json["collaborators"]
            for user in collaborators.split(","):
                if (not db_sess.query(User).get(user)):
                    return jsonify({'error': f'Collaborator with id "{user}" does not exists'})
            job.collaborators = str(collaborators)
        if ("start_date" in request.json):
            job.start_date = datetime.fromisoformat(str(request.json["start_date"]))
        if ("end_date" in request.json):
            job.end_date = datetime.fromisoformat(str(request.json["end_date"]))
        if ("is_finished" in request.json):
            job.is_finished = bool(request.json["is_finished"])

        db_sess.add(job)
        db_sess.commit()
    except Exception:
        return jsonify({'error': 'Bad request'})
    return jsonify({'success': 'OK'})
