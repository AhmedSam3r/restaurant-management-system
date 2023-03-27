# Restaurant Management System
This is a web-based system designed for managing reservations and tables in a restaurant. It allows restaurant staff to easily manage reservations and track table availability in real-time.

# Prerequisites
1. Ensure that you have python of version greater than or equal 3.8 and pip3 installed on your device
2. Install postgres database on your device and CREATE DATABASE restuarant
3. Install git and github on your device
4. Install postman for API testing
# Installation
To install the project, follow these steps:

1. Clone the repository: git clone https://github.com/AhmedSam3r/restaurant-management-system.git
2. Navigate to the project directory: cd restaurant-management-system
3. Create a virtual environment: python3 -m venv venv
4. Activate the virtual environment: source venv/bin/activate
5. Install dependencies: pip install -r requirements.txt
6. Set up the database: python manage.py migrate
7. Load initial data: python manage.py loaddata fixtures/initial_data.json
8. Run the server: python manage.py runserver


# Usage
To use the API, you can either send HTTP requests directly to the endpoints or import the provided JSON collection file into a tool like Postman to simplify testing.

Running the Server
To run the server locally, navigate to the project directory and run the following command:

Write<br>
`python manage.py runserver`<br>
This will start the development server at http://127.0.0.1:8000/.

# Testing the API
To test the API using the JSON collection file [you will find it in the project with the name of RestuarantManagementAPIs], follow these steps:

1. Import the restaurant-management-system.json collection file into Postman by clicking the "Import" button and selecting the file.
In Postman, navigate to the "Collections" tab and select the "Restaurant Management System" collection.
2. Expand the collection to view the available requests and endpoints.
3. Click on a request to view its details and click the "Send" button to send the request to the server.
4. View the response from the server in the "Response" tab.
Note that you will need to have the server running locally in order to successfully send requests.

# Additional Note

* You can find the project's board here <br>
`https://trello.com/b/olsAMKhq/kanban-template` <br>
* In order to be able to test the APIs correctly you must create at least one initial staff member whose role is admin.<br> 
* Then you can start from there by adding other staff members, tables and reservations<br>
you can do so by `python manage.py shell`


&nbsp;&nbsp;&nbsp;&nbsp;`from staff.models import Staff` <br>
&nbsp;&nbsp;&nbsp;&nbsp;`from staff.models import Role` <br>
&nbsp;&nbsp;&nbsp;&nbsp;`admin_role = Role.objects.get(name='admin')` <br>
&nbsp;&nbsp;&nbsp;&nbsp;`admin_person = Staff(name='adminn', email='adminn@gmail.com',password='123', role=admin_role, secret_key='hello')`<br>
&nbsp;&nbsp;&nbsp;&nbsp;`admin_person.save()` <br>
&nbsp;&nbsp;&nbsp;&nbsp;`emp_role = Role.objects.get(name='employee')` <br>
&nbsp;&nbsp;&nbsp;&nbsp;`emp_person = Staff(name='emp', email='emp@gmail.com',&nbsp;&nbsp;&nbsp;&nbsp;password='123', role=emp_role, secret_key='hello')` <br>
&nbsp;&nbsp;&nbsp;&nbsp;`emp_person.save()`


Kindly note that it's not best practice to save the password in plain form

# TODO
* Add proper testing
* Add error handling in more dynamic way
* Read Dynamic variables from .env file
