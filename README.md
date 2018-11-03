# Online-Hostel-Allotment
Hostel Management System made for our IIITV hostel. Specific to requirements.
A desktop application aimed to manage hostel. The application was made using Bootstrap, Django and sqllite for Database.
This was a personal project made during summer.
## Objective:
Hostel Management System is an web application which aims at the computerization of hostel management letting the complete process of allotment and its management be dependent on computer. As the working of any hostel is almost same, I’ve chosen our very own “Indian Institute of Infomation Technolgy, Vadodara Hostel” to present the software and its design. Without computers, everything goes on registers causing a lot of paper work with very less efficiency, which is where this software can dramatically improve the overall management. My purpose in developing this application was to provide a very simple interface to the requirement that will be easy to navigate and operate, proper record keeping and reporting, and an application that can be implemented on desktop or client/server architecture i.e. providing with the following features:
Highly user-friendly Cross-platform Easy-to-use Tested system to track unnoticed error

## Hostel Accountant
This user account is meant for the head clerk who maintains the complete database of students, maintains the room allotments.
The privileges allowed to the head clerk/hostel accountant are:
1. Allot a new room
2. Empty an allotted room
3. Swap rooms between students
4. Shift student to empty room
5. View or Update Details of student
6. Change Password
7. Search through complete database

## Clone project
 first fork the repository
$ git clone https://github.com/singhshubham98/Online-Hostel-Allotment.git

## Install requirements
$ cd Online-Hostel-Allotment          
$ sudo -H pip install -r requirements.txt

## Migrate Database
$ python manage.py makemigrations   
$ python manage.py migrate

## Create Super User
$ python manage.py createsuperuser

## Run CLI
$ python manage.py runserver

## License
This project is licensed under the MIT license. See LICENSE file for more details.
