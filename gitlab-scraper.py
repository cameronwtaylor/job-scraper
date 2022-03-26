import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://boards.greenhouse.io/gitlab'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup)

def create_list_of_departments(tag, previous_tag, department_level):
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

department_level_one_list = create_list_of_departments('h3','h3','one')
department_level_two_list = create_list_of_departments('h4','h3','two')
department_level_three_list = create_list_of_departments('h5','h4','three')

department_list = department_level_one_list + department_level_two_list + department_level_three_list

department_df = pd.DataFrame(department_list)

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

job_df = pd.DataFrame(job_list)
(job_df.set_index(['job_title', 'job_href','job_location'])
   .apply(lambda x: x.str.split(',').explode())
   .reset_index())

job_df['job_department_id'] = list(job_df['job_department_id'])

job_df.explode('job_department_id')