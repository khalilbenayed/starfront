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

company_job_applications_api = Blueprint('company_job_applications_api', __name__)


@company_job_applications_api.route(
    '/api/company/<int:company_id>/job/<int:job_id>/applications', methods=['GET'])
@jwt_required
def get_company_job_applications(company_id, job_id):
    current_user = get_jwt_identity()
    print(company_id, current_user)
    if current_user.get('id') != company_id:
        return jsonify({'message': 'Not authorized'}), 403

    page_number = request.args.get('page_number')
    number_of_applications_per_page = request.args.get('number_of_applications_per_page')
    status_code, data = backend_api.get_company_job_applications(
        company_id, job_id,
        page_number, number_of_applications_per_page)
    return jsonify(data), status_code


@company_job_applications_api.route(
    '/api/company/<int:company_id>/job/<int:job_id>/applications/<int:application_id>', methods=['GET'])
@jwt_required
def get_company_job_application_by_id(company_id, job_id, application_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != company_id:
        return jsonify({'message': 'Not authorized'}), 403

    status_code, data = backend_api.get_company_job_application_by_id(
        company_id, job_id, application_id)
    return jsonify(data), status_code
