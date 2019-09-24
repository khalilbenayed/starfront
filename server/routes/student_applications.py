import os
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

student_applications_api = Blueprint('student_applications_api', __name__)


@student_applications_api.route('/api/student/<int:student_id>/applications', methods=['POST'])
@jwt_required
def create_application(student_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != student_id:
        return jsonify({'message': 'Not authorized'}), 403

    files = request.files
    data = dict(request.form)
    # if both id and files is passed for a type of documents
    # send bad request
    if ((data.get('resume_id') is not None and files.get('resume') is not None) or
            (data.get('cover_letter_id') is not None and files.get('cover_letter') is not None) or
            (data.get('transcript_id') is not None and files.get('transcript') is not None)):
        return jsonify({'message': 'You cannot pass both the id and a document for the same type'}), 400

    # create documents if needed
    for key, temp_file in files.items():
        if key not in {'resume', 'cover_letter', 'transcript'}:
            continue

        temp_file.save(f'server/tmp/{temp_file.filename}')
        temp_file.close()
        with open(f'server/tmp/{temp_file.filename}', 'rb') as f:
            files = {
                'document': f
            }
            payload = {
                'document_type':
                    'RESUME' if key == 'resume' else
                    'COVER_LETTER' if key == 'cover_letter' else
                    'TRANSCRIPT'
            }
            status_code, resp = backend_api.create_student_document(student_id, payload, files)
        os.remove(f'server/tmp/{temp_file.filename}')

        if status_code != 200:
            return jsonify(resp), status_code

        if key == 'resume':
            data['resume_id'] = resp.get('id')
        elif key == 'cover_letter':
            data['cover_letter_id'] = resp.get('id')
        else:
            data['transcript_id'] = resp.get('id')

    status_code, resp = backend_api.create_application(student_id, data)
    return jsonify(resp), status_code


@student_applications_api.route('/api/student/<int:student_id>/applications', methods=['GET'])
@jwt_required
def get_student_applications(student_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != student_id:
        return jsonify({'message': 'Not authorized'}), 403

    page_number = request.args.get('page_number')
    number_of_applications_per_page = request.args.get('number_of_applications_per_page')
    status_code, data = backend_api.get_student_applications(student_id, page_number, number_of_applications_per_page)
    return jsonify(data), status_code


@student_applications_api.route('/api/student/<int:student_id>/applications/<int:application_id>', methods=['GET'])
@jwt_required
def get_student_application_by_id(student_id, application_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != student_id:
        return jsonify({'message': 'Not authorized'}), 403

    status_code, data = backend_api.get_student_application_by_id(student_id, application_id)
    return jsonify(data), status_code


@student_applications_api.route('/api/student/<int:student_id>/applications/<int:application_id>', methods=['DELETE'])
@jwt_required
def delete_student_application(student_id, application_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != student_id:
        return jsonify({'message': 'Not authorized'}), 403

    payload = {
        'state': 'CANCELLED',
    }
    status_code, data = backend_api.update_student_application(student_id, application_id, payload)
    return jsonify(data), status_code
