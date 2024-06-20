# Social Media Microservices Project

This project is a social media platform split into three microservices to manage users, discussions, and an API gateway
for routing. The project uses FastAPI for the backend, PostgreSQL for the database, and Docker for containerization and
orchestration.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Microservices](#microservices) :
    * [User Service](#user-service)
    * [Discussion Service](#discussion-service)
    * [API Gateway](#api-gateway)
3. [Database Schema](#database-schema)
4. [Installation](#installation)
5. [API Endpoints](#api-endpoints)
6. [Functionalities](#functionalities)
7. [Tech Stack](#tech-stack)

## Project Overview

This project implements a social media platform where users can sign up, log in, follow other users, create and interact
with posts, and search for posts or users. The project is divided into three microservices:

* User Service:  Manages user-related operations including authentication, user management, and following features.
* Discussion Service: Handles post CRUD operations, comments, replies, likes, and views.
* API Gateway: Uses NGINX for reverse proxy and routing requests to the appropriate microservice.
* All services use a shared PostgreSQL database and are containerized using Docker. Docker Compose is used for
  orchestration

## Microservices

#### Microservice Diagram
![ezcv logo](https://i.postimg.cc/Znp9Tq7L/diagram-export-20-06-2024-15-29-17.png)

NB:used free alternative of aws-s3 for cloud storage

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

* id (Primary Key)
* user_id (Foreign Key to Users)
* post_id (Foreign Key to Post)

##### PostViews

* id (Primary Key)
* user_id (Foreign Key to Users)
* post_id (Foreign Key to Post)
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

![ezcv logo](https://i.postimg.cc/wBg19HLX/diagram-export-20-06-2024-15-10-11.png)

### Deployment

##### Containerization: All services are containerized using Docker.

##### Docker Compose: Docker Compose file is provided for managing multi-container applications.

##### Instructions: Follow the README for instructions on how to build and run the application.

# Installation

To run this application, follow these steps:

1. Make sure you have Docker installed on your machine.

2. Clone the repository containing the API code.

```
https://github.com/rinshadkv/spyne-assignment.git
```

3. Navigate to the root directory of the project.

```
cd /spyne
```

4. Open a terminal window.

5. Run the following command to build and start the Docker containers:

```
docker-compose up --build
```

This command will build the Docker images for each service and start the containers defined in the `docker-compose.yml`
file.

6. Once the containers are up and running, you can access the APIs provided by the User Service on port 8000/users,
   and Discussion Service On port 8000/discussion.

- User Service API:http://0.0.0.0:8000/users
- Discussion Service: http://0.0.0.0:8000/discussion

7. You can also interact with the PostgreSQL database directly on port 5432 .

8. To stop the containers, press `Ctrl + C` in the terminal where they are running, and then run the following command
   to remove the containers:

## API Endpoints

### User Service

* POST /users/signup: Create a new user
* POST /users/login: User login
* PUT /users/{id}: Update user information
* DELETE /users/{id}: Delete a user
* GET /users: List all users
  - parameters(optional):  search=(name)
* POST /users/follow: Follow a user
* POST /users/unfollow: Unfollow a user
* GET /users/{user_id}/followers : get all followers
* GET /users/{user_id}/following : get all followings

### Discussion Service

* POST /discussion/posts: Create a new discussion
* PUT /discussion/posts/{id}: Update a discussion
* DELETE /discussion/posts/{id}: Delete a discussion
* GET /discussions/posts: List all discussions :
    * **parameters:**
    * search_text (optional) search by text
    * tags(optional) filter by list of tags
    * limit (by default 100 optional) limit the result
    * skip(by default 0) skip number of items


* POST discussion/posts/{id}/comments: Comment on a discussion
* POST /discussion/posts/{post_id}/like: Like a discussion
* POST /comment/{comment_id}/like: Like a comment
* POST /discussion/comments/{comment_id}/replies: Reply to a comment
* DELETE discussion/comments/{id} : delete comments
* DELETE /discussion/replies/{id} : delete reply
* PUT posts/{post_id}/comments/{comment_id} : update comments

## Functionalities

* User Signup/Login: Users can sign up and log in to the platform.
* Search Users: Users can search for other users by name.
* Follow/Unfollow: Users can follow or unfollow other users.
* Post Discussions: Users can create text or text+image posts.
* Comments and Likes: Users can comment on, like, and reply to discussions and comments.
* Modify Posts/Comments: Users can edit or delete their posts and comments.
* Post Views: Users can see the view count of a post.
* Search Posts: Users can search for posts using hashtags or text.

## Tech Stack

* Backend Framework: FastAPI
* Database: PostgreSQL
* Containerization: Docker
* Orchestration: Docker Compose
* API Gateway: NGINX

#### Testing

* Use the provided Postman collection to test the API functionalities.
* you can find a postman collection file in root directory
* or you can find the postman public link
  here https://elements.getpostman.com/redirect?entityId=33669743-231a0a44-a6fb-4c33-a25b-9a74a1059a53&entityType=collection
* also you can find swagger collections of respective service on http://0.0.0.0:9000/docs for discussion service http://0.0.0.0:7000/docs for user service

* Conclusion

This project provides a basic social media platform with a microservices architecture, allowing for easy scaling and
management of different functionalities.

.