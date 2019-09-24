"""server/app.py - main api app declaration"""
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import yaml
import os
from routes import (
    student_login_api,
    company_login_api,
    company_jobs_api,
    student_documents_api,
    jobs_api,
    student_applications_api,
    company_job_applications_api,
)
from flask_jwt_extended import JWTManager


with open('server/config.yaml') as cfg_file:
    cfg = yaml.load(cfg_file, Loader=yaml.Loader).get(os.environ['ENV'])
    secret_key = cfg.get('secret-key')
    mail_sender = cfg.get('mail-sender')

"""Main wrapper for app creation"""
app = Flask(__name__, static_folder='../build')
CORS(app)

app.config.update(dict(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_SENDER=mail_sender
))

app.config['JWT_SECRET_KEY'] = secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

bcrypt = Bcrypt(app)


##
# View route
##
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """Return index.html for all non-api routes"""
    # pylint: disable=unused-argument
    return send_from_directory(app.static_folder, 'index.html')


app.register_blueprint(student_login_api)
app.register_blueprint(company_login_api)
app.register_blueprint(company_jobs_api)
app.register_blueprint(jobs_api)
app.register_blueprint(student_documents_api)
app.register_blueprint(student_applications_api)
app.register_blueprint(company_job_applications_api)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7000)
