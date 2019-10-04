import json
import os
from flask import (
    request,
    Blueprint,
    jsonify,
    url_for,
    render_template,
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
)
import backend_api
from utils import (
    hash_password,
    generate_confirmation_token,
    confirm_token,
    send_email,
)


company_login_api = Blueprint('company_login_api', __name__)


@company_login_api.route('/api/company/login', methods=['POST'])
def company_login():
    payload = json.loads(request.data)
    status_code, data = backend_api.login_company(payload)
    response_data = {
        "data": data
    }
    if status_code == 200:
        access_token = create_access_token(identity={
            'id': data.get('id'),
            'email': data.get('email'),
            'is_company': True
        })
        refresh_token = create_refresh_token(identity={
            'id': data.get('id'),
            'email': data.get('email'),
            'is_company': True
        })
        response_data["access_token"] = access_token
        response_data["refresh_token"] = refresh_token
    return jsonify(response_data), status_code


@company_login_api.route('/api/company/signup', methods=['POST'])
def company_signup():
    payload = json.loads(request.data)
    payload['password'] = hash_password(payload['password'])
    status_code, data = backend_api.signup_company(payload)
    response_data = {
        "data": data
    }
    if status_code == 200:
        access_token = create_access_token(identity={
            'id': data.get('id'),
            'email': data.get('email'),
            'is_company': True
        })
        refresh_token = create_refresh_token(identity={
            'id': data.get('id'),
            'email': data.get('email'),
            'is_company': True
        })
        response_data["access_token"] = access_token
        response_data["refresh_token"] = refresh_token

        # skip email confirmation for test environment
        if os.environ.get('TEST') is None:
            token = generate_confirmation_token(payload['email'])
            verification_url = url_for('company_login_api.confirm_email', token=token, _external=True)
            html = render_template('verification_email.html', verification_url=verification_url)
            subject = "Please confirm your email"
            send_email(data.get('email'), subject, html)
    return jsonify(response_data), status_code


@company_login_api.route('/api/company/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


@company_login_api.route('/api/company/verify/<string:token>', methods=['get'])
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        return jsonify({'error': 'The confirmation link is invalid or has expired.'}), 400
    status_code, data = backend_api.get_company_by_email(email)
    if status_code == 200:
        company = data.get('companies')[0]
        if company.get('state') != 'NOT_VERIFIED':
            return jsonify({'message': 'This account has already been verified.'})
        else:
            payload = {
                'state': 'ACTIVE'
            }
            status_code, data = backend_api.update_company(company.get('id'), payload)
            if status_code == 200:
                return jsonify({'message': 'Your account has been verified successfully.'}), 200
            else:
                return jsonify(data), status_code
    else:
        return jsonify(data), status_code


@company_login_api.route('/api/company/<int:company_id>', methods=['PATCH'])
@jwt_required
def update_company(company_id):
    current_user = get_jwt_identity()
    if current_user.get('id') != company_id:
        return jsonify({'message': 'Not authorized'}), 403

    payload = json.loads(request.data)
    status_code, data = backend_api.update_company(company_id, payload)
    return jsonify(data), status_code


# @company_login_api.route('/api/company/logout')
# @login_required
# def company_logout():
#     logout_user()
#     return jsonify({})
