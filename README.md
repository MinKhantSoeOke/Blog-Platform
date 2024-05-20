# Blog Platform

**by**: Min Khant Soe Oke

## Overview

This is a simple blog platform built using Python, Flask, and SQLite. The platform allows users to register, log in, create posts, update their account information and like & comment to other users posts. It also includes features such as password change and email notifications using SMTP.

## Dependencies

**To run this project, you need to have the following dependencies installed:**

* Python 3
* Flask
* SQLite
* Bootstrap
* smtplib

## Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/blog-platform.git
cd blog-platform
```

2. Create a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install the dependencies:
```
pip install Flask
```

4. Set up the database:
```
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

5. Run the application:
```
flask run
```

6. **Access the application**:
   Open your web browser and go to 'http://127.0.0.1:5000'

## Features

**User Registration**
Users can register by providing their username, email, and password.

**User Login**
Registered users can log in by providing their email and password.

**Create New Post**
Users can create a new blog post by providing a title and content.

**View Blog Posts**
Users can view all blog posts on the main page.

**Like & Comment**
Users can like and comment on other users posts.

**Update Account**
Users can update their account information and change their password.
