## Introduction
This project scrapes data from individual company job boards. 

**Goals**
* Learning the components of the Modern Data Stack including
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
2. Clone this repo (`git clone https://gitlab.com/cameronwtaylor/job-scraper.git`)
3. Navigate into the folder containing the repo
3. Create a virtual environment in the project folder (`python3 -m venv .venv`)
4. Install required dependencies (`python3 -m pip install -r requirements.txt`)
5. Activate the environment (`source .venv/bin/activate`)
6. Launch the Dagster UI (`dagit -f gitlab-scraper.py`)
7. Clone the Airbyte repo (`git clone https://github.com/airbytehq/airbyte.git`)
8. Navigate into the local repo
9. Open Docker Desktop
10. Install Airbyte (`docker-compose up`)
11. Navigate to http://localhost:8000/ to test Airbyte installation
12. Pull a docker postgres instance (`docker pull postgres`)
13. Run a postgres instance (`docker run --name postgres-database -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=password -d postgres`)
14. Create a folder called `gitlab` inside `tmp/airbyte_local`
15. Create an Airbyte source for gitlab departments file
16. Create an Airbyte source for gitlab jobs file
17. Create an Airbyte destination for local postgres
18. Create a connection between departments file source and destination
19. Create a connection between jobs file source and destination
20. Load the connection IDs into github-scraper.py


* https://www.docker.com/products/docker-desktop/
* https://docs.airbyte.com/quickstart/deploy-airbyte
* https://airbyte.com/tutorials/orchestrate-data-ingestion-and-transformation-pipelines
* https://airbyte.com/tutorials/data-scraping-with-airflow-and-beautiful-soup

## Infrastructure
* Scraping scripts (Python with `requests` and `BeautifulSoup4`)
* Extract/Load (Airbyte)
* Transform (dbt)
* Orchestration (Dagster)
* Storage (Postgres)
* Containerization (Docker)

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
