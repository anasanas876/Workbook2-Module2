# Project Management System

A Django REST Framework-based backend application that provides secure REST APIs for managing companies, users, projects, and tasks using Json Web Token (JWT) authentication



# Features

- JWT Authentication
- Role-Based Authorization (Admin, Manager, Employee)
- Company-Based Multi-Tenancy
- CRUD Operations for:
- Companies
- Users
- Projects
- Tasks
- Audit Logging
- Background Email Sending using the Django Tasks Framework
- REST API
- Unit Testing
- Entity Relationship Diagram (ERD)



# Tech Stack

- Python 3.14+
- Django 6.x
- Django REST Framework (DRF)
- SQLite
- Simple JWT


# Prerequisites

Before running the project, make sure the following software is installed:

- Python 3.14 or later
- pip


---

# Installation

## 1. Clone the Repository
Open Terminal on your device.

Run the following command
```bash
git clone <repository-url>
```

Move into the project directory.

```bash
cd ProjectManagementSystem
```



## 2. Create a Virtual Environment

On Windows


python -m venv myvenv
You can choose any name for the virtual environment.


Activate it


myvenv\Scripts\activate




## 3. Install Dependencies

```bash
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
```




# Database Setup

Create migrations

Run the following commands to create the database tables.

```bash
python manage.py makemigrations
```


Apply migrations
```bash

python manage.py migrate
```




# Create a Superuser

Create a superuser by running the following command:
```bash
python manage.py createsuperuser
```

Follow the prompts to create an administrator account.



# Run the Development Server
```bash
python manage.py runserver
```


Open


http://127.0.0.1:8000/


# Creating Users

## Method 1 — Django Admin

Log In to the Django Admin Panel

http://127.0.0.1:8000/admin/


Use the superuser credentials.

Create, update, or delete users from the admin interface.



## Method 2 — Django Shell

Open Django Shell


python manage.py shell


You can create users manually here.






# User Roles

The system supports three user roles.

- Admin
- Manager
- Employee

Permissions are applied using custom Django REST Framework(DRF) permission classes.



# Multi-Tenancy

Users can only access data belonging to their own company.

Example

If User A belongs to Company A, they cannot access projects belonging to Company B.



# Audit Logging

Every important action is recorded in the Audit Log.

Examples

- Project Created
- Project Updated
- Project Deleted
- Project Viewed

Each log stores

- User
- Action
- Timestamp
- Related Object



# Background Tasks

Welcome emails are sent using the Django Tasks Framework.

Instead of making the user wait while the email is sent, the API immediately returns a response and the email is sent in the background.

---

# Running Unit Tests

Run all tests by using following command:


python manage.py test


The project contains tests for

- Log in Endpoint
- Signup Endpoint
- Authorization
- Company Data Isolation(Multi Tenancy )


# Project Structure


ProjectManagementSystem/

── config/
── members/
── manage.py
── requirements.txt
── README.md
── ERD.png


---

# Entity Relationship Diagram

The project includes an ERD describing the database structure.

Main entities

- Company
- User
- Project
- Task
- AuditLog

---

# API Endpoints

These are the API Endpoints of the project:
Name: Method: Description

projets/GET/Returns all the projects belonging only to a company of logged in user
signup/POST/Asks users to create an account
login/POST/Allows users to login to their existing account
createprojects/POST/Allows Admins and Managers to create projects.
updateprojects/PUT/Allows Admins and Managers to update projects.
deleteprojects/DELETE/Allows Admins and Managers to delete projects.
tasks/GET/Returns all the tasks belonging to a specific project and company
createtasks/POST/Allows admins and managers to create tasks.
updatetasks/PUT/Allows admins and managers to update tasks.
deletetasks/DELETE/Allows admins and managers to delete tasks.
patchtasks/PATCH/Allows admins and managers to partially update a task.
showtasks/GEt/Shows only tasks to employees  that are assigned to them.
createusers/POST/Allows only admins to create users.
deleteusers/DELETE/Allows only admins to delete users.





# Security Features

- JWT Authentication
- Role-Based Access Control
- Company-Based Data Isolation(Multi Tenancy)
- Permission Classes
- Audit Logging



