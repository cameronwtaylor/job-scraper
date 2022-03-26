import requests
import json
from bs4 import BeautifulSoup
from dagster import in_process_executor, job, op, mem_io_manager

@op
def retrieve_job_board_soup():
    url = 'https://boards.greenhouse.io/gitlab'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

@op
def set_tag_h3():
    return 'h3'

@op
def set_tag_h4():
    return 'h4'

@op
def set_tag_h5():
    return 'h5'

@op
def set_department_level_one():
    return 'one'

@op
def set_department_level_two():
    return 'two'

@op
def set_department_level_three():
    return 'three'

@op
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
def build_department_json(department_level_one_list, department_level_two_list, department_level_three_list):
    department_list = department_level_one_list + department_level_two_list + department_level_three_list
    with open('gitlab_departments.json', 'w') as fp:
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
    with open('gitlab_jobs.json', 'w') as fp:
        json.dump(job_list, fp, sort_keys=True, indent=4)

@job(
    resource_defs={'io_manager': mem_io_manager},
    executor_def=in_process_executor
)
def gitlab_jobs_extract():
    soup = retrieve_job_board_soup()
    tag_h3 = set_tag_h3()
    tag_h4 = set_tag_h4()
    tag_h5 = set_tag_h5()
    department_level_one = set_department_level_one()
    department_level_two = set_department_level_two()
    department_level_three = set_department_level_three()
    department_level_one_list = create_list_of_departments(soup, tag_h3, tag_h3, department_level_one)
    department_level_two_list = create_list_of_departments(soup, tag_h4, tag_h3, department_level_two)
    department_level_three_list = create_list_of_departments(soup, tag_h5, tag_h4, department_level_three) 
    build_department_json(department_level_one_list, department_level_two_list, department_level_three_list)
    build_job_json(soup)