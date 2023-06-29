# Library Management Web Application

## Requirements:
A local library is in dire need of a web application to ease their work. The library management system must allow a librarian to track books and their quantity, books issued to members, book fees.

For the sake of simplicity, you don't have to implement sessions and roles, you can assume that the app will be used by the librarian only.

The following functionalities are expected from the application:

- Base Library System

Librarians must be able to maintain:

- Books with stock maintained
- Members
- Transactions
The use cases included here are to:

- Perform general CRUD operations on Books and Members
- Issue a book to a member
- Issue a book return from a member
- Search for a book by name and author
- Charge a rent fee on book returns
- Make sure a member’s outstanding debt is not more than KES.500

## Prerequisites:
To run the project, a virtual environment is created and Flask, a Python framework, has been installed in it. SQLAlchemy has been also been used for the project and sqlite3 database since this is a light-weight application. Docker has also been used to containerize the application.

To set-up the virtual environment, install the virtual environment using:
```commandline
pip install virtualenv
```
Then create a directory to setup virtual environment
```commandline
 mkdir <name_of_folder>
 cd <name_of_folder>
 python3.8 -m venv env
```
To activate the virtual environment run:
On mac
``` source env/bin/activate ```
On linux
``` source virtualenv_name/bin/activate ```
Note: source is a shell command for linux
On Windows, cd into the directory and run
``` <virtual_env>/Scripts/activate ```

Add flask, and flask sqlalchemy run
```pip install flask-sqlalchemy```

To get libraries in virtual environment, run in the terminal,
```commandline
pip freeze > requirements.txt
```

### Perform general CRUD operations on Books and Members
Books
#### Create
![alt text](images\add_kane_and_abel.JPG)
The result is viewed from view book page and results as:
![alt text](images\book_added.JPG)
#### Read
![alt text](images\books_available.JPG)
![alt text]
#### Update
![alt text](images\update_book_price.JPG)
#### Delete
![alt text](images\kna_deleted.JPG)

Members
#### Create
![alt text](
images\add_member_june.JPG)
The result is viewed from view book page and results as:
![alt text]()
#### Read
![alt text](images\members_page.JPG)
#### Update
![alt text](images\update_member_jsl_balance.JPG)
![alt text](images\updated_member.JPG)

#### Delete
![alt text](images\deleted_jsl_entry.JPG)
References:
[virtual_env setup](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)