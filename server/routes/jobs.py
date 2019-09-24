from flask import request, Blueprint, jsonify
from flask_jwt_extended import (
    jwt_required,
)
import backend_api

jobs_api = Blueprint('jobs_api', __name__)


@jobs_api.route('/api/jobs', methods=['GET'])
@jwt_required
def get_jobs():
    page_number = request.args.get('page_number')
    number_of_jobs_per_page = request.args.get('number_of_jobs_per_page')
    status_code, data = backend_api.get_jobs(page_number, number_of_jobs_per_page)
    return jsonify(data), status_code


@jobs_api.route('/api/jobs/<int:job_id>', methods=['GET'])
@jwt_required
def get_job_by_id(job_id):
    status_code, data = backend_api.get_company_job_by_id(job_id)
    return jsonify(data), status_code
