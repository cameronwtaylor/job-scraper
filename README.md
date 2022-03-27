## Introduction
This project scrapes data from individual company job boards. 

**Goals**
* Learn the components of the Modern Data Stack
* Long term: Create a curated repository of remote jobs to overcome traditional job aggregator challenges including
    * Duplication of postings
    * Lack of postings
    * Inability to perform fine-grained searching

**Supported job boards**
* GitLab

## Installation

**Prerequisites**
* [Python](https://www.python.org/downloads/) is installed
* [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) is installed

**Initial Setup**
1. Create a local folder to hold the job scraper and Airbyte repos
2. Open a terminal window from that folder or `cd` into the folder
3. Clone the job scraper repo (run `git clone https://gitlab.com/cameronwtaylor/job-scraper.git` in your terminal)

**Create Virtual Environment**
1. Navigate into the job scraper repo in your terminal
2. Run the following commands in your terminal
    * `python3 -m venv .venv` (creates a virtual environment)
    * `python3 -m pip install -r requirements.txt` (installs required dependencies)
    * `source .venv/bin/activate` (activates the environment)

**Install Docker and Airbyte**
1. Open a terminal window from the local folder you created in **Initial Setup** or `cd` into the folder
2. Follow the official [Deploy Airbyte](https://docs.airbyte.com/quickstart/deploy-airbyte) instructions
3. Create a folder called `gitlab` inside `tmp/airbyte_local` (this is a hidden folder in the root directory of your machine)

If this is your first time installing Docker, you may need to open Docker Desktop before running `docker-compose up` to avoid errors.

**Install Postgres**
1. Pull a docker Postgres instance (run `docker pull postgres` in your terminal)
2. Run a Postgres instance in a Docker container (run `docker run --name postgres-database -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=password -d postgres` in your terminal)

**Create Airbyte Components**
1. Navigate to http://localhost:8000/
2. Create an Airbyte source for the GitLab departments file
![Airbyte GitLab departments file source](/images/airbyte_gitlab_departments_source.png)
2. Create an Airbyte source for the GitLab jobs file
![Airbyte GitLab jobs file source](/images/airbyte_gitlab_jobs_source.png)
3. Create an Airbyte destination for the local Postgres instance
![Airbyte local Postgres destination](/images/airbyte_postgres_destination.png)
4. Create a connection between the departments source and the destination
![Airbyte GitLab departments connection](/images/airbyte_gitlab_departments_connection.png)
5. Create a connection between the jobs source and the destination
![Airbyte GitLab jobs connection](/images/airbyte_gitlab_jobs_connection.png)
6. Retrieve the connection ID for each connection by looking at UUID in the URL of the connection
`http://localhost:8000/workspaces/53dbc046-08cd-4a4a-b980-370a9c56833e/connections/b503b849-189e-47eb-b684-fdbe1221cd4c/status`
7. Load the connection IDs into `scrapers/github_scraper.py` in the `sync_gitlab_departments` and `sync_gitlab_jobs` Dagster ops

**Run the Scraper**
1. Open a terminal from the `job-scraper` repo
2. Launch the Dagster UI (run `dagit` in your terminal)
3. Click `Launchpad`
4. Click `Launch Run` in the bottom right corner

**Helpful Links**

This project is basically a mash-up of these two tutorials:
* https://airbyte.com/tutorials/orchestrate-data-ingestion-and-transformation-pipelines
* https://airbyte.com/tutorials/data-scraping-with-airflow-and-beautiful-soup

If you want a database client to view your Postgres tables, [DBeaver](https://dbeaver.io/download/) is one option.

## Infrastructure
* Scraping scripts - [Python](https://www.python.org/) with [requests](https://docs.python-requests.org/en/latest/) and [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* Extract/Load - [Airbyte](https://airbyte.com/)
* Orchestration - [Dagster](https://dagster.io/)
* Storage - [Postgres](https://www.postgresql.org/)

## Support
Please submit an issue for any support. 

## Roadmap

**Short Term**
* Use dagster-dbt to add dbt transformation example to the pipeline
* Write scrapers for more job boards

**Long Term**
* Host this project on the cloud to automate pipeline
* Transition from Postgres to Snowflake
* Create 
* Create weekly email digest of new jobs

## Contributing
Accepting all contributions!

## License
MIT License

## Project status
Active
