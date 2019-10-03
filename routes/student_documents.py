import os
import json
import shutil
from flask import (
    request,
    Blueprint,
    jsonify,
    send_from_directory,
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
import backend_api

student_documents_api = Blueprint('student_documents_api', __name__)


@student_documents_api.route('/api/student/<int:student_id>/student_documents', methods=['GET'])
@jwt_required
def get_student_documents(student_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != student_id:
        return jsonify({'message': 'Not authorized'}), 403

    page_number = request.args.get('page_number')
    number_of_documents_per_page = request.args.get('number_of_documents_per_page')
    status_code, data = backend_api.get_student_documents(student_id, page_number, number_of_documents_per_page)
    return jsonify(data), status_code


@student_documents_api.route('/api/student/<int:student_id>/student_documents/<int:document_id>', methods=['GET'])
@jwt_required
def get_student_document_by_id(student_id, document_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != student_id and current_user.get('is_company') is False:
        return jsonify({'message': 'Not authorized'}), 403

    resp = backend_api.get_student_document_by_id(student_id, document_id)
    if resp.status_code == 200:
        filename = resp.raw.headers.get('Content-Disposition').rsplit('=')[1]
        with open(f'tmp/{filename}', 'wb') as f:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, f)
        resp_to_return = send_from_directory('tmp/', filename, as_attachment=True)
        os.remove(f'tmp/{filename}')
        return resp_to_return


@student_documents_api.route('/api/student/<int:student_id>/student_documents', methods=['POST'])
@jwt_required
def create_student_document(student_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != student_id:
        return jsonify({'message': 'Not authorized'}), 403

    temp_file = request.files.get('document')
    temp_file.save(f'tmp/{temp_file.filename}')
    temp_file.close()
    with open(f'tmp/{temp_file.filename}', 'rb') as f:
        files = {
            'document': f
        }
        status_code, data = backend_api.create_student_document(student_id, request.form, files)
    os.remove(f'tmp/{temp_file.filename}')
    return jsonify(data), status_code


@student_documents_api.route('/api/student/<int:student_id>/student_documents/<int:document_id>', methods=['PATCH'])
@jwt_required
def update_student_document(student_id, document_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != student_id:
        return jsonify({'message': 'Not authorized'}), 403

    payload = json.loads(request.data)
    status_code, data = backend_api.update_student_document(student_id, document_id, payload)
    return jsonify(data), status_code


@student_documents_api.route('/api/student/<int:student_id>/student_documents/<int:document_id>', methods=['DELETE'])
@jwt_required
def delete_student_document(student_id, document_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != student_id:
        return jsonify({'message': 'Not authorized'}), 403

    payload = {
        'state': 'DELETED'
    }
    status_code, data = backend_api.update_student_document(student_id, document_id, payload)
    return jsonify(data), status_code