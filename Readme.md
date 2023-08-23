# Resume Booster: Enhance Your Resume with ATS Compatibility
### Try it now : https://resumeatsparss-758b89fcdb8f.herokuapp.com/
![Animation_1](https://github.com/RawfurJim/Job_Scan/assets/64610564/209e77a9-722e-47cb-a671-5f34033693b6)

## Overview
Resume Booster is a machine learning-based application designed to help individuals improve their resumes by aligning them with job descriptions, thereby increasing their chances of passing through ATS (Applicant Tracking System) scanners.

With the majority of organizations utilizing ATS scanners to filter resumes, having the right keywords related to the job description is essential. Resume Booster scans the provided job description and the candidate's resume, comparing the skills mentioned and giving immediate feedback. The result includes a comprehensive list of skills found in the job description, marked with a check if present in the resume or marked otherwise.

## Key Features

#### Active Learning Method 
Utilizing an iterative process that involves scraping, annotating, and training.
#### Skill Matching
Identifying both hard skills (e.g., Python, SQL) and soft skills (e.g., Good Communication, Problem Solving) in the job description and comparing them to the resume.
#### Dockerized Workflow
The entire project has been containerized, ensuring ease of setup and deployment.
#### CI/CD Pipeline
Seamless integration and deployment using GitHub Actions and deployment to Heroku.


## How it Works


![Animation_3](https://github.com/RawfurJim/Job_Scan/assets/64610564/d6325d67-84d2-4c24-8855-24b046cb7c6b)



#### Data Scraping
Initial scraping of data from various sources, saved to an SQL database.
#### Manual Annotation
The data is manually annotated with hard and soft skills and then saved to a MongoDB database.
#### Model Training
Utilizing SpaCy, the data is fetched from MongoDB and used to train the model.
#### Active Learning Pipeline
Creation of a connection/pipeline to input data to the model from the SQL database, obtaining initial annotation results (NER) for hard and soft skills. The annotations are stored in MongoDB, where manual checking and corrections are performed before feeding the data back into the model for training.
Docker and CI/CD: Dockerizing the entire process, making it accessible via Docker Hub, and creating a CI/CD pipeline using GitHub Actions to deploy the application to Heroku.



## Installation

To Install This App on Your Local Machine
Follow the steps below to get this app running on your local machine:

### Using Docker

### First install Docker in your local machine. Then Pull the Docker Image: Use the following command to pull the latest image from Docker Hub.
#### docker pull rmjim/job_scan:latest

### Next, run the following command to start the container. Mapping port 6000 inside the container to port 6001 on your host machine
#### docker container run -d -p 6001:6000 rmjim/job_scan:latest

### Access the App: Open your browser and navigate to:
##### http://localhost:6001

