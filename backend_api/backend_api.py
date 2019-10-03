from .backend_client import AMSClient

ams_client = AMSClient()


def signup_student(data):
    return ams_client.post('api/students/', data)


def signup_company(data):
    return ams_client.post('api/companies/', data)


def login_student(data):
    return ams_client.post('api/students/login', data)


def login_company(data):
    return ams_client.post('api/companies/login', data)


def get_student_by_id(student_id):
    return ams_client.get(f'api/students/{student_id}')


def get_student_by_email(email):
    return ams_client.get(f'api/students?email={email}')


def get_company_by_id(company_id):
    return ams_client.get(f'api/companies/{company_id}')


def get_company_by_email(email):
    return ams_client.get(f'api/companies?email={email}')


def update_student(student_id, data):
    return ams_client.patch(f'api/students/{student_id}', data)


def update_company(company_id, data):
    return ams_client.patch(f'api/companies/{company_id}', data)


def get_company_jobs(company_id, page_number=None, number_of_jobs_per_page=None):
    url = f'api/companies/{company_id}/jobs'
    if page_number is not None and number_of_jobs_per_page is not None:
        url += f'?page_number={page_number}&number_of_jobs_per_page={number_of_jobs_per_page}'
    return ams_client.get(url)


def get_company_job_by_id(company_id, job_id):
    return ams_client.get(f'api/companies/{company_id}/jobs/{job_id}')


def get_jobs(page_number=None, number_of_jobs_per_page=None):
    url = f'api/jobs'
    if page_number is not None and number_of_jobs_per_page is not None:
        url += f'?page_number={page_number}&number_of_jobs_per_page={number_of_jobs_per_page}'
    return ams_client.get(url)


def get_job_by_id(job_id):
    return ams_client.get(f'api/jobs/{job_id}')


def create_company_job(company_id, data):
    return ams_client.post(f'api/companies/{company_id}/jobs', data)


def update_company_job(company_id, job_id, data):
    return ams_client.patch(f'api/companies/{company_id}/jobs/{job_id}', data)


def create_student_document(student_id, data, files):
    return ams_client.post(f'api/students/{student_id}/student_documents', data, files)


def get_student_documents(student_id, page_number=None, number_of_jobs_per_page=None):
    url = f'api/students/{student_id}/student_documents'
    if page_number is not None and number_of_jobs_per_page is not None:
        url += f'?page_number={page_number}&number_of_jobs_per_page={number_of_jobs_per_page}'
    return ams_client.get(url)


def get_student_document_by_id(student_id, document_id):
    return ams_client.get_file(f'api/students/{student_id}/student_documents/{document_id}')


def create_application(student_id, data):
    return ams_client.post(f'api/students/{student_id}/applications', data)


def get_student_applications(student_id, page_number=None, number_of_applications_per_page=None):
    url = f'api/students/{student_id}/applications'
    if page_number is not None and number_of_applications_per_page is not None:
        url += f'?page_number={page_number}&number_of_jobs_per_page={number_of_applications_per_page}'
    return ams_client.get(url)


def get_student_application_by_id(student_id, application_id):
    return ams_client.get(f'api/students/{student_id}/applications/{application_id}')


def update_student_application(student_id, application_id, data):
    return ams_client.patch(f'api/students/{student_id}/applications/{application_id}', data)


def get_company_job_applications(company_id, job_id,
        page_number=None, number_of_applications_per_page=None):
    url = f'api/companies/{company_id}/jobs/{job_id}/applications'
    if page_number is not None and number_of_applications_per_page is not None:
        url += f'?page_number={page_number}&number_of_jobs_per_page={number_of_applications_per_page}'
    return ams_client.get(url)


def get_company_job_application_by_id(company_id, job_id, application_id):
    return ams_client.get(f'api/companies/{company_id}/jobs/{job_id}/applications/{application_id}')


def update_student_document(student_id, document_id, data):
    return ams_client.patch(f'api/students/{student_id}/student_documents/{document_id}', data)
