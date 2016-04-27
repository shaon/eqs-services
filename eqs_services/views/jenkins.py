from flask import Blueprint, request, jsonify
from jenkinsapi.jenkins import Jenkins


jenkins_view = Blueprint('jenkins', __name__)


@jenkins_view.route('/free_job', methods=['POST'])
def free_job():
    job_id = request.json['job_id']
    print job_id
    ret = {'message': 'Failed'}
    if not job_id:
        ret['message'] = 'Job Id not found!'
        return jsonify(ret)
    jenkins_url = 'http://jenkins.qa1.eucalyptus-systems.com'
    server = Jenkins(jenkins_url, username='user', password="password")
    server.build_job('Free Reservation', params={'JOB_ID': job_id})
    ret['message'] = 'success'
    return jsonify(ret)
