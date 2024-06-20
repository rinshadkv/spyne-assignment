# Social Media Microservices Project


This project is a social media platform split into three microservices to manage users, discussions, and an API gateway for routing. The project uses FastAPI for the backend, PostgreSQL for the database, and Docker for containerization and orchestration.
## Table of Contents

1. Project Overview
2. Microservices : 
    * User Service
    * Discussion Service
    * API Gateway
3. Database Schema
4. Installation
5. API Endpoints
6. Functionalities 
7. Tech Stack

## Project Overview
This project implements a social media platform where users can sign up, log in, follow other users, create and interact with posts, and search for posts or users. The project is divided into three microservices:

* User Service:  Manages user-related operations including authentication, user management, and following features.
* Discussion Service: Handles post CRUD operations, comments, replies, likes, and views.
* API Gateway: Uses NGINX for reverse proxy and routing requests to the appropriate microservice.
* All services use a shared PostgreSQL database and are containerized using Docker. Docker Compose is used for orchestration

## Microservices

### User Service
#### Handles user management and authentication.

Features:
* User sign up
* User login
* Create, update, delete user
* Search user by name
* Follow/unfollow users


### Discussion Service
#### Manages discussions (posts), comments, and interactions.

Features:
* Create, update, delete discussion
* Comment on discussions
* Like comments and posts
* Reply to comments
* View count for posts
* Search discussions by tags and text

### API Gateway
#### Routes incoming requests to the appropriate microservice using NGINX.


## Database Schema
### The PostgreSQL database schema includes the following tables:


##### Users

* id (Primary Key)
* name
* mobile_no (Unique)
* email (Unique)
* password_hash (Hashed)

##### Followers

* id (Primary Key)
* follower_id (Foreign Key to Users)
* followed_id (Foreign Key to Users)


##### Post

* id (Primary Key)
* user_id (Foreign Key to Users)
* text
* image_url
* created_on

##### HashTags

* id (Primary Key)
* tag (Unique)

##### PostHashTags

* id (Primary Key)
* discussion_id (Foreign Key to Discussions)
* hashtag_id (Foreign Key to HashTags)

##### Comments

* id (Primary Key)
* post_id (Foreign Key to Post)
* user_id (Foreign Key to Users)
* text
* created_on


##### PostLikes

id (Primary Key)
user_id (Foreign Key to Users)
post_id (Foreign Key to Post)

##### CommentLikes

* id (Primary Key)
* user_id (Foreign Key to Users)
* comment_id (Foreign Key to Comments)

##### Replies

* id (Primary Key)
* comment_id (Foreign Key to Comments)
* user_id (Foreign Key to Users)
* text
* created_on



#### Data Flow Diagram

![ezcv logo](https://i.postimg.cc/bryzzCpd/diagram.png)

### Deployment

##### Containerization: All services are containerized using Docker.

##### Docker Compose: Docker Compose file is provided for managing multi-container applications.

##### Instructions: Follow the README for instructions on how to build and run the application.

#### Testing

* Use the provided Postman collection to test the API functionalities.
* you can find a postman collection file in root directory 
* WebSocket connections can be tested using WebSocket client tools.
* Conclusion

The Order API provides a robust platform for managing orders and executing trades on the exchange. Its microservices
architecture ensures scalability and fault tolerance, while the use of modern technologies enables real-time
communication and efficient order matching.

# Installation

To run  this application, follow these steps:

1. Make sure you have Docker installed on your machine.

2. Clone the repository containing the API code.

```
git clone https://github.com/rinshadkv/algotest.git
```

3. Navigate to the root directory of the project.

```
cd /algotest
```

4. Open a terminal window.

5. Run the following command to build and start the Docker containers:

```
docker-compose up --build
```

This command will build the Docker images for each service and start the containers defined in the `docker-compose.yml`
file.

6. Once the containers are up and running, you can access the APIs provided by the User Service on port 8000/users, 
    and Discussion Service On  port 8000/discussion.

- User Service API:http://0.0.0.0:8000/users
- Discussion Service: http://0.0.0.0:8000/discussion

7. You can also interact with the PostgreSQL database directly on port 5432 .

8. To stop the containers, press `Ctrl + C` in the terminal where they are running, and then run the following command
   to remove the containers:



