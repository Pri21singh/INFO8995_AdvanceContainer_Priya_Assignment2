# Containerized Web Application with Flask, MySQL, and Load Balancing

This project demonstrates the containerization of a simple web application using Docker. The web application exposes API endpoints for user management, stores user data in a MySQL database, and is scaled with Docker Compose. The setup also includes Nginx for load balancing.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Requirements](#requirements)
3. [Setup and Installation](#setup-and-installation)
4. [Docker Configuration](#docker-configuration)
5. [API Endpoints](#api-endpoints)
6. [Scaling and Load Balancing](#scaling-and-load-balancing)
7. [Security Best Practices](#security-best-practices)
8. [Logs](#logs)
9. [Troubleshooting](#troubleshooting)

## Project Overview

This project consists of:
- A Flask-based web application that exposes two endpoints:
  - **POST /user** to create a user.
  - **GET /user/{id}** to retrieve a user's information.
- A containerized MySQL database that stores user data securely.
- Docker Compose for orchestrating the web and database containers.
- Nginx for load balancing the web application, distributing requests across multiple instances.

## Requirements

- Docker
- Docker Compose
- Python 3.13+
- MySQL

## Setup and Installation
1. Build the Docker containers: docker-compose build

2. Start the containers: docker-compose up -d

## Docker Configuration
1. FROM python:3.13-slim - To optimize the build and deployment process, we use a lightweight version of the official Python 3.13 image.
2.  Set the working directory to /app - This directory will be used as the reference point for all ensuing actions, including file copies and run instructions.
3. The requirements.txt file is added to the container from the local computer using the COPY command. All of the Python requirements needed for the Flask application inside the container are subsequently installed by the RUN command.
4. The application logs produced during runtime are stored in the logs/app directory created inside the container by this line.
5. Every Python application file (app.py,.env, etc.) in the local app folder is copied to the /app directory within the container using the COPY command.
6. Established a new non-root account (myuser) and switches to it for security reasons. By doing this, the program cannot be executed with root rights, which might leave the system vulnerable.
7. The container will listen on port 5000, which is the Flask application's default port, as Docker is informed by the EXPOSE command.
9. The container will run the command python app.py when it starts, which will start the Flask application.

## Docker-Compose.yml
1. The configuration and interaction between the various services in the application are specified in the docker-compose.yml file. The web application, MySQL database, and Nginx reverse proxy are among the services it coordinates.
2. Docker Compose is instructed to use the Dockerfile located in the current directory to build the image using the build:. directive.
3. The depends_on directive guarantees that the web service will launch subsequent to the db (MySQL) service being operational.
4. The Flask application receives environment variables (such database credentials) from the environment section.
5. The networks section makes sure the web container is linked to the same network as the nginx and database containers so they may communicate with each other.
6. By binding the host machine's./logs directory to the container's /app/logs, the volumes section enables you to keep logs even when the container restarts.
7. To ensure that the web application scales horizontally, the deploy section instructs that three replicas of the web container be deployed. In the event of a failure, it also specifies a restart policy that restarts the container.
8. The database service creates a container running MySQL using the official mysql:latest image.
9. Database name, user, password, and root password are among the MySQL environment variables that are configured in the environment section.
10. A volume for MySQL data persistence (db_data) and a volume for database initialization using the init.sql script found in the./db folder are defined in the volumes section.
11. The database container and the other containers are connected to the same network (app-network) via the networks section.

## Nginx Conf
1. The nginx service creates a Nginx reverse proxy container using the official nginx:latest image.
2. The depends_on directive makes sure that the Nginx service doesn't start until the web container is online.
3. External access to the web application is made possible by mapping port 80 of the container to port 80 of the host computer in the ports section.
4. To set up the Nginx reverse proxy for load balancing, the volumes section mounts the nginx.conf configuration file into the container.
5. The nginx container is connected to the same network as the other services via the networks section.

## Scaling and Load Balancing
Using the replicas: 3 directive in the docker-compose.yml file, Docker Compose is used to scale the Flask web application horizontally.
This provides redundancy and load distribution by allowing three instances of the Flask application to operate concurrently.

## Nginx reverse proxy for load balancing
1. To distribute the load evenly among the several Flask instances, Nginx is employed as a reverse proxy.
2. A pool of application servers is defined by the upstream directive. Web:5000, which is equivalent to the Flask containers, is defined here. 
3. Incoming traffic will be routed by Nginx to any of the web instances that are using port 5000.
4. The location / block proxies incoming requests to the application servers while listening on port 80.


## Access Logs
The application logs will be saved in the logs directory as well as under the app folder on the local machine, due to the bind mount in Docker Compose.
Also to access the logs of the containers, you can use the following command:   docker logs -f CONTAINER_NAME_OR_ID
or docker logs -f --timestamps CONTAINER_NAME_OR_ID

## API Endpoints
1. **POST /user**: Create a new user. The request body should contain the user's id, first name, and last name.
{
  "first_name": "P",
  "last_name": "S"
}
Response: 201 Created : {
  "id": 1,
  "message": "User created successfully"
}
2. **GET /user/{id}**: Retrieve a user's information by their id.
Example request: GET /user/1
{
  "id": 1,
  "first_name": "P",
  "last_name": "S"
}

## Nginx Conf
The Nginx configuration is set up to serve the Flask application on port 80 and to balance the load between the Flask containers.

### 1. Clone the repository:
```bash
git clone https://your-repository-url.git
cd your-repository-directory
