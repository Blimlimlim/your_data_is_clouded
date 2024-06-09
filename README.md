# Overview

This program lets a user enter task lists with tasks into a cloud database. It runs in a command line. To use, run the program and follow the prompts. To try it out for yourself you will need to create your own firebase project as it currenlty uses admin priveledges and you need your own service key json file and database. When you have your service key file and Firebase project, update the path on the first line of the main function in "lost_in_the_cloud.py" to be the path to your json file. You will need the to use "pip install firebase-admin" to import the libraries used in this project.

I did this project to learn about cloud database storage and applications.


[Software Demo Video](https://youtu.be/H1_Q234NPqc)

# Cloud Database

This project uses Firebase Firestore which is a noSQL database.

The data is organized into nested collections of documents. The top level seperates user data with a collection of user documents with each using the user's account id as its id. Each user's document contains a collection of task list documents which are the second level. On bottom level, each task list document contains a collection of task documents which contain fields for task info. The user and task list documents also contain a field for tracking items in their second collection.

# Development Environment

This project uses a Google Firebase project. Specifically, the authentication and firestore (nosql database) products.

This program is written in Python. It uses modules from google cloud and firebase_admin.

# Useful Websites

- [Firebase, Cloud Firestore](https://firebase.google.com/docs/firestore)
- [Firebas Admin Auth module documentation](https://firebase.google.com/docs/reference/admin/python/firebase_admin.auth)
- [Stack Overflow](https://stackoverflow.comy)

# Future Work

- Complete TODO feature, edit task
- Add field to task list docs that tracks number of completed tasks in addition to total tasks and display this on "show_lists".
- Add handling for edge cases where errors can occur
- Add code to prevent duplicate names from being entered
- Create a legitimate user side program with real sign in.
