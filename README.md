# Star Network - A Simple Social Network App
#### Video Demo:  <https://youtu.be/ZIh49blUJoA>
#### Description:
Star Network is a user-friendly social networking application that enables seamless communication and interaction among users. It offers an array of features to connect, share, and engage within a secure environment.

## Table of Contents

- [Introduction](#introduction)
- [Overview](#overview)
    - [Features Enriching User Experience](#features-enriching-user-experience)
- [Features](#features)
    - [User Authentication and Profile Management](#user-authentication-and-profile-management)
    - [Social Interaction](#social-interaction)
    - [Post Management](#post-management)
- [Technologies Used](#technologies-used)
- [Files Created](#files-created)
- [Dependencies](#dependencies)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributions](#contributing)

## Introduction

Star Network, spearheaded by Rahul R from Thiruvananthapuram, India, is a visionary project aimed at revolutionizing social networking experiences. With a focus on user interaction and connectivity, this platform offers an intuitive interface that empowers users to effortlessly connect, share, and engage.

## Overview

### Features Enriching User Experience
- **User Authentication & Profile Management:** 

- **Post Management:** 
- **Additional Functionalities:** 
## Features

### User Authentication and Profile Management
- **Sign Up:** Users can register by providing necessary details including their email, first name, last name, and password. This information is securely stored to create a unique user account.
- **Login:** Registered users can securely log in using their credentials to access the platform's features.
- **Profile Customization:** Users have complete control over their profile information. They can easily edit and update their email address, profile picture, first name, last name, and password as needed.

### Social Interaction

- **Follow and Unfollow:** Users have the ability to follow or unfollow other users, allowing them to curate their feed and stay updated on content from specific individuals.
- **View Following Posts:** A dedicated feed displays posts exclusively from followed users, providing an easy way to stay connected and engaged with preferred content.
- **View Liked Posts:** Users can access a compilation of posts they've liked, enabling them to revisit and interact with favored content.

### Post Management
- **Create Posts:** Users can effortlessly share thoughts, images, updates, or links with their followers, fostering communication and expression.
- **Edit or Delete Posts:** Users have full control over their shared content. They can easily edit or delete their own posts, ensuring content accuracy and relevance.
- **Like Posts:** The 'like' feature enables users to express their appreciation for posts shared by others, encouraging a positive and interactive community. Each post shows the likes received.
- **Comment on Posts:** Users can engage in discussions by commenting on posts, promoting interaction and exchange of ideas.
- **View Comments:** This feature allows users to view comments on their own posts or posts from others, enhancing engagement and facilitating conversations.

### Additional Features
- **View Posts:** Users can explore a feed displaying posts from various users, enabling them to discover new content and connections. Each post shows the comments they received.
- **Change Email, Profile Picture, First Name, Last Name, and Password:** Users have the flexibility to modify and update their profile information, ensuring their account remains current and accurate.

## Technologies Used
- Frontend: HTML, CSS, JavaScript
- Backend: Python , Flask
- Database: SQLite

## Files Created
- **app.py :** The Heart of the app. Contains the db models and Views.
    - db Models : Users, Posts, Comments, Likes
    - app.index : Show the front pages displaying all posts.
    - app.login : Deals the login section.
    - app.register : Checking requirements and saves user.
    - app.profile : Shows the user information and their posts and gives the option to edit profile.
    - app.follow : Displays all followed posts.
    - app.newpost : Create a new post.
    - app.view_post : Shows current post, their likes and option to comment on them and view all the comments.
    - app.post_manipulation : Used to edit or delete posts by their owner.
    - app.liked_posts : Shows the current user liked posts in reverse chronological order.

    - **APIs** 
        - app.follow_unfollow : Used to follow or unfollow an user using JS
        - app.like_unlike : Used to like or Unlike a post JS.
        - app.post_data : Gives information about a specific post.
- **helpers.py :** Houses the login required function.
- **starnetwork.db :** The main database contains the user information, posts, likes and comments.

## Dependencies

The Star Network - The Social Network uses the following libraries:

- `Flask`: For backend.
- `Javascript`: For Handling client-side interactions and live price updating.
- `Bootstrap.css and bootstrap.js`: For User Dynamic Interfaces.
- `SQLite`: For Database.
- `Flask Dependencies` :
    1. flask_session
    2. Werkzeug
    3. flask_sqlalchemy
    4. flask_migrate

Make sure to install these dependencies before running the game using pip:

```bash
pip install Werkzeug Flask-Session Flask-SQLAlchemy Flask-Migrate
```

## Getting Started

To run the the Social Network locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/rahulrofficial/socialnetwork.git
   ```
2. Navigate to the project directory:
   ```bash
   cd socialnetwork   
   ```
3. Run Flask Server :
   ```bash
   flask run
   ```

## Usage
Upon installation and setup, users can access the application through an intuitive interface. Sign up or log in to begin exploring, creating posts, like them and customizing profiles.

## Contributing
Contributions to Star Network are encouraged! Fork the repository, make changes, and submit a pull request.


