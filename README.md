## Introduction
This project scrapes data from individual company job boards. 

**Goals**
* Learning the components of the Modern Data Stack
* Long term: Creating a curated repository of remote jobs to overcome the challenges of traditional job aggregators including
    * Duplication of postings
    * Lack of postings
    * Inability to perform fine-grained searching

**Supported job boards**
* GitLab

## Installation
1. Install Python 3.9.10
2. Install git
3. Install Docker https://docs.docker.com/desktop/mac/install/

https://dbeaver.io/download/

**Initial Setup**
1. Create a local folder to hold the job scraper and Airbyte repos
2. Open a terminal window from that folder or `cd` into the folder
3. Clone the job scraper repo (run `git clone https://gitlab.com/cameronwtaylor/job-scraper.git` in your terminal)

**Create Python Virtual Environment**
1. Navigate into the job scraper repo in your terminal
2. Run the following commands in your terminal
    * `python3 -m venv .venv` (creates a virtual environment)
    * `python3 -m pip install -r requirements.txt` (installs required dependencies)
    * `source .venv/bin/activate` (activates the environment)

**Install Docker and Airbyte**
1. Open a terminal window from the local folder you created in **Initial Setup** or `cd` into the folder
2. Follow the official [Deploy Airbyte](https://docs.airbyte.com/quickstart/deploy-airbyte) instructions
3. Create a folder called `gitlab` inside `tmp/airbyte_local` (this is a hidden folder in the root directory)

If this is your first time installing Docker, you may need to open Docker Desktop before running `docker-compose up` to avoid errors.

**Install Postgres**
1. Pull a docker Postgres instance (run `docker pull postgres` in your terminal)
2. Run a Postgres instance in a Docker container (run `docker run --name postgres-database -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=password -d postgres` in your terminal)

**Create Airbyte Components**
1. Navigate to http://localhost:8000/
1. Create an Airbyte source for GitLab departments file
2. Create an Airbyte source for GitLab jobs file
3. Create an Airbyte destination for local Postgres
4. Create a connection between departments file source and destination
5. Create a connection between jobs file source and destination
6. Load the connection IDs into github-scraper.py


* https://www.docker.com/products/docker-desktop/
* https://docs.airbyte.com/quickstart/deploy-airbyte
* https://airbyte.com/tutorials/orchestrate-data-ingestion-and-transformation-pipelines
* https://airbyte.com/tutorials/data-scraping-with-airflow-and-beautiful-soup

6. Launch the Dagster UI (`dagit -f gitlab-scraper.py`)

## Infrastructure
* Scraping scripts - [Python](https://www.python.org/) with [requests](https://docs.python-requests.org/en/latest/) and [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* Extract/Load - [Airbyte](https://airbyte.com/)
* Orchestration - [Dagster](https://dagster.io/)
* Storage - [Postgres](https://www.postgresql.org/)

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

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
