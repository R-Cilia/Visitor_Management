Visitor Management System

Overview

The Visitor Management System is a Django web application that allows organizations to manage and track visitors who visit their premises. The system allows employees to check in and check out visitors and also allows administrators to view and manage the visitor logs.

Summary

This is a Django web application for managing employees and visitors' attendance at a premise. The application allows employees and visitors to check in and out of the premise by updating their status in the database. The status of the employees and visitors can be checked in real-time by the administrator of the premise.

Features

    • Visitors can be checked in and checked out.
    • The system maintains a log of all visitors who have visited the premises.
    • The system allows employees to search for visitors based on their name or ID.
    • The system allows administrators to view and manage visitor logs.
    • The system has a SOS feature which sends an emergency evacuation message to all visitors and employees on the premises.

Project Structure

The application consists of the following models:
    • Employee: 
This model stores the details of employees such as name, employee ID, mobile number, and status (whether the employee is checked in or checked out).
    • Visitor:
This model stores the details of visitors such as name, mobile number, date of visit, and status (whether the visitor is checked in or checked out).

The application also has the following views:
    • employee_in: 
This view allows employees to check in to the premise by updating their status to "checked-in" in the database.
    • employee_out: 
This view allows employees to check out of the premise by updating their status to "checked-out" in the database.
    • Sos:
This view sends an SOS message to all employees and visitors currently checked in to the premise.
    • present_employee_search: 
This view returns a list of all employees currently checked in to the premise, in the form of a JSON response.

Requirements

    Python 3.x
    Django 2.x
    Twilio API
    Django Crispy Forms
    Django Messages

Installation

    1. Clone the repository: 
git clone https://github.com/[your_username]/employee_management_system.git
    2. Navigate to the project directory: 
cd employee_management_system
    3. Create a virtual environment: 
python -m venv env
    4. Activate the virtual environment: 
source env/bin/activate
    5. Install the required packages: 
pip install -r requirements.txt
    6. Migrate the database: 
python manage.py migrate
    7. Create a superuser: 
python manage.py createsuperuser
    8. Run the development server: 
python manage.py runserver

How to Run the Project

    1. Clone the repository to your local machine.
    2. Install the required software and libraries mentioned in the "Requirements" section.
    3. Run the following command in the terminal/command prompt to install the project dependencies:
pip install -r requirements.txt
    4. Run the following command in the terminal/command prompt to run the development server:
python manage.py runserver
    5. Access the application in your web browser at http://localhost:8000/

Deployment

    1. Create a Linode account.
    2. Create a new Linode instance.
    3. Connect to the instance using SSH.
    4. Clone the Visitor Management System repository to your Linode instance.
    5. Create a virtual environment for the project.
    6. Install the required dependencies using pip.
    7. Update the settings.py file with your Twilio API credentials and other required information.
    8. Run migrations to create the necessary database tables.
    9. Run the Django development server.
    10. Access the Visitor Management System in your browser using the public IP address of your Linode instance.

Usage

To use the Visitor Management System, follow these steps:

    1. Register as an administrator.
    2. Log in to the system.
    3. Add employees to the system.
    4. Check in visitors and view visitor logs.
    5. Use the employee search feature to search for visitors.
    6. Use the SOS feature in case of an emergency evacuation.

Documentation

The documentation for the Visitor Management System is provided in the form of inline comments in the code. The documentation includes information on the functions, variables, and class methods used in the project. The documentation is written in a professional and conventional manner, making it easy for developers to understand the code.

Conclusion

This project provides a simple and user-friendly way to manage the attendance of employees and visitors at a premise. The real-time status of employees and visitors can be easily accessed by the administrator, making it easy to keep track of who is currently checked in to the premise. The SOS feature adds an extra layer of security to the application, ensuring the safety of employees and visitors in case of an emergency.

License

The Visitor Management System is open-source software licensed under the MIT license.
