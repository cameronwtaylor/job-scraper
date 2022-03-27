import requests
import json
from bs4 import BeautifulSoup
from dagster import in_process_executor, job, op, mem_io_manager
from dagster_airbyte import airbyte_resource, airbyte_sync_op

def create_list_of_departments(soup, tag, previous_tag, department_level):
    department_list = []
    departments = soup.find_all(tag)
    for department in departments:
        department_name_value = department.text
        department_id_value = department.get('id')
        if tag == 'h3':
            department_parent_id_value = department_id_value
        else:
            department_parent_id_value = department.find_previous(previous_tag).get('id')
        department_dict = {'department_id':department_id_value,
                           'department_level':department_level,
                           'department_name':department_name_value,
                           'department_parent_id':department_parent_id_value}
        department_list.append(department_dict)
    return list(filter(lambda i: i['department_id'] != 'filter-count', department_list)) 

@op
def retrieve_job_board_soup():
    url = 'https://boards.greenhouse.io/gitlab'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

@op
def build_department_json(soup):
    department_level_one_list = create_list_of_departments(soup, 'h3', 'h3', 'one')
    department_level_two_list = create_list_of_departments(soup, 'h4', 'h3', 'two')
    department_level_three_list = create_list_of_departments(soup, 'h5', 'h4', 'three')
    department_list = department_level_one_list + department_level_two_list + department_level_three_list
    with open('/private/tmp/airbyte_local/gitlab/gitlab_departments.json', 'w') as fp:
        json.dump(department_list, fp, sort_keys=True, indent=4)

@op
def build_job_json(soup):
    job_list = []
    jobs = soup.find_all('div', {'class':'opening'})
    for job in jobs:
        job_title_value = job.find('a').text
        job_href_value = job.find('a').get('href')
        job_department_id_value = job.get('department_id')
        job_office_id_value = job.get('office_id')
        job_location_value = job.find('span', {'class':'location'}).text
        job_dict = {'job_title':job_title_value,
                    'job_href':job_href_value,
                    'job_department_id':job_department_id_value,
                    'job_office_id':job_office_id_value,
                    'job_location':job_location_value}
        job_list.append(job_dict)
    with open('/private/tmp/airbyte_local/gitlab/gitlab_jobs.json', 'w') as fp:
        json.dump(job_list, fp, sort_keys=True, indent=4)

sync_gitlab_departments = airbyte_sync_op.configured(
    {"connection_id": "b503b849-189e-47eb-b684-fdbe1221cd4c"}, name="sync_gitlab_departments"
)

sync_gitlab_jobs = airbyte_sync_op.configured(
    {"connection_id": "411aed26-f442-4b94-ba79-3a5cae0dd3da"}, name="sync_gitlab_jobs"
)

@job(
    #in memory io manager and in process executor used because bs4
    #text output cannot be pickled with the default fs_io_manager
    resource_defs={
        'io_manager': mem_io_manager,
        'airbyte': airbyte_resource.configured({'host': 'localhost', 'port': '8000'}),
    },
    executor_def=in_process_executor
)
def gitlab_jobs_extract():
    soup = retrieve_job_board_soup()
    sync_gitlab_departments(start_after=build_department_json(soup))
    sync_gitlab_jobs(start_after=build_job_json(soup))