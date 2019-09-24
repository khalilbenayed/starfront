import json
from flask import (
    request,
    Blueprint,
    jsonify,
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
import backend_api

company_jobs_api = Blueprint('company_jobs_api', __name__)


@company_jobs_api.route('/api/company/<int:company_id>/jobs', methods=['GET'])
@jwt_required
def get_company_jobs(company_id):
    page_number = request.args.get('page_number')
    number_of_jobs_per_page = request.args.get('number_of_jobs_per_page')
    status_code, data = backend_api.get_company_jobs(company_id, page_number, number_of_jobs_per_page)
    return jsonify(data), status_code


@company_jobs_api.route('/api/company/<int:company_id>/jobs/<int:job_id>', methods=['GET'])
@jwt_required
def get_company_job_by_id(company_id, job_id):
    status_code, data = backend_api.get_company_job_by_id(company_id, job_id)
    return jsonify(data), status_code


@company_jobs_api.route('/api/company/<int:company_id>/jobs', methods=['POST'])
@jwt_required
def create_company_job(company_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != company_id:
        return jsonify({'message': 'Not authorized'}), 403

    payload = json.loads(request.data)
    status_code, data = backend_api.create_company_job(company_id, payload)
    return jsonify(data), status_code


@company_jobs_api.route('/api/company/<int:company_id>/jobs/<int:job_id>', methods=['PATCH'])
@jwt_required
def update_company_job(company_id, job_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != company_id:
        return jsonify({'message': 'Not authorized'}), 403

    payload = json.loads(request.data)
    status_code, data = backend_api.update_company_job(company_id, job_id, payload)
    return jsonify(data), status_code


@company_jobs_api.route('/api/company/<int:company_id>/jobs/<int:job_id>', methods=['DELETE'])
@jwt_required
def delete_company_job(company_id, job_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != company_id:
        return jsonify({'message': 'Not authorized'}), 403

    payload = {
        'state': 'DELETED'
    }
    status_code, data = backend_api.update_company_job(company_id, job_id, payload)
    return jsonify(data), status_code


