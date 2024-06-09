# firebase imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# my imports
import user_auth


#Functions---------------------------------------------------------------------------
def printmenu(menu_num, label_string): # TODO look in here to find todo's for unimplemented menu options
    match menu_num:
        case 0:
            label_string  = 'Register/login'
            print(f"\n========= {label_string} ==========\n"
                  "option-----------description-------\n"
                  "new             (for new user)\n"
                  "login           (for existing user)\n"
                  "-----------------------------------")
        case 1:
            print(f"\n====== {label_string}'s Task-lists =====\n" # use a username for this label string
                  "option-------description----\n"
                  "----------------------------\n"
                  "v            view task lists\n"
                  "a            add new list\n"
                  "o            open task list\n"
                  "d            delete task list\n"
                  "----------------------------")
        case 2:
            print(f"\n====== {label_string} ======\n" # use a task list title for this label string
                  "option-------description\n"
                  "---------------------- -\n"
                  "v            view tasks\n"
                  "a            add task\n"
                  "m            mark task\n"
                  "e            edit task\n"  #TODO
                  "d            delete task\n"
                  "b            go back\n"
                  "------------------------")

def show_lists(db, uid):
    """
    Display a user's task lists
    """
    # get user field "numLists"
    user_d_ref = db.collection("Users").document(uid)
    doc = user_d_ref.get()
    if doc.exists:
        print("\n----- Task lists ------")
        num_lists = doc.to_dict().get("numLists") # get the number of lists 
        for i in range(num_lists): # visit each list and display its name and number of tasks TODO show completed tasks list doc needs new completed field
            list_d_ref = user_d_ref.collection("Lists").document(str(i))
            doc = list_d_ref.get() # put list doc contents in variable
            if doc.exists:
                print(doc.to_dict().get("title")) # print its title
            else:
                print(f"List doc {i} doesn't exist")
    else:
        print("User doc doens't exist")
    
def get_list_c_ref(db, uid):
    return db.collection("Users").document(uid).collection("Lists")

def get_document_by_title(c_ref, doc_title):
    """
    returns a reference to a specific document inside a collection by performing a query on its title.
    
    Document in collection must have the field "title" to be found
    """
    query = c_ref.where(filter=FieldFilter("title", "==", doc_title))
    results = query.stream()
    # get reference to list doc (currently gets last doc with title. Avoid adding lists with duplicate names)
    for doc in results:
        d_ref = c_ref.document(doc.id) # target doc reference
    return d_ref

def show_tasks(db, uid, list_title):
    """Display tasks in list"""
    lists_c_ref = get_list_c_ref(db, uid) # reference to current user's collection of lists
    list_d_ref = get_document_by_title(lists_c_ref, list_title) # reference to the specified list
    doc = list_d_ref.get() # put list contents in variable
    if doc.exists:
        print(f"----- {list_title} Tasks -----------------")
        num_tasks = doc.to_dict().get("numTasks") # get number of tasks value
        for i in range(num_tasks): # visit each task and display its name, completion status, and details
            task_d_ref = list_d_ref.collection("Tasks").document(str(i))
            doc = task_d_ref.get() # put task doc contents in variable
            if doc.exists:
                doc = doc.to_dict() # convert doc to dictionary
                # Set some variables based on task fields
                task_title = doc.get("title")
                completion_icon = ":-)" if doc.get("complete") else "X" # smiley for complete tasks, X for incomplete
                details = doc.get("details")
                print(f"\n{task_title} -- {completion_icon}\n" # show task, completion status, and details
                      f"Details: {details}")
            else:
                print(f"Task {i} doesn't exist")

    else:
        print(f"List with name '{list_title}' does not exist")

def toggle_field(d_ref, bool_field):
    """ takes a task reference and reverses a boolean field. """
    doc = d_ref.get()
    if doc.exists:
        value = doc.to_dict().get(bool_field) # get boolean value from document field
        d_ref.update({bool_field: not value}) # update with inverted value
    else:
        print("document does not exist")

def create_User_data(db, uid, display_name):
    """
    Creates a document in collection "Users" with the user's account uid as the document id.
    """
    # field data for new user document. Contains name and empty array of list id's (none yet)
    data = {"name": display_name, "numLists": 0}
    # create document in collection "Users" with data
    db.collection("Users").document(uid).set(data)

def add_new_list(db, uid, list_title):
    """
    Add a new list doc to the user's Lists collection with list_title as Title. 
    Track number of lists and determine list id using the user doc's field, numTasks. Update numTasks
    """
    user_d_ref = db.collection("Users").document(uid)
    # get the user doc contents
    doc = user_d_ref.get()
    
    if doc.exists:
        # get numLists value
        num_lists = doc.to_dict().get("numLists")
        # add new list in sub-collection "Lists" using num_lists as id
        list_d_ref = user_d_ref.collection("Lists").document(str(num_lists))
        list_d_ref.set({"title": list_title, "numTasks": 0})
        # increment num_lists
        num_lists += 1
        # update user document
        user_d_ref.update({"numLists": num_lists})
    else:
        print("doc doesn't exist")
    
def add_new_task(list_d_ref, task_title):
    """
    Add a new task doc to a user's list doc using the list doc's "title" field. 
    """
    # get reference to the collection of Lists
    # lists_c_ref = get_list_c_ref(db, uid)
    # list_d_ref = get_list_by_title(lists_c_ref, list_title) # get reference to target list
    # Add a task to the target list doc
    doc = list_d_ref.get() # get list doc contents
    if doc.exists:
        num_tasks = doc.to_dict().get("numTasks") # get number of tasks value
        # add new task in sub-collection "Tasks"
        task_d_ref = list_d_ref.collection("Tasks").document(str(num_tasks))
        task_d_ref.set({"title": task_title, "complete": False, "details": input("Enter task details: ")})
        # increment number of tasks
        num_tasks +=1
        list_d_ref.update({"numTasks": num_tasks})
    else:
        print(f"The current list does not exist")

def delete_docs_in_Collection(c_ref, num_docs):
    """
    Don't use this on collections containing documents with sub-collections. Delete subcollection documents first.
    This is for deleting documents who's ids are zero indexed (as strings)
    """
    for i in range(num_docs): # loop through my numbered IDs in  the colection person
        c_ref.document(str(i)).delete() # delete document
        # db.collection(collection).document(str(i)).delete() # delete document using i as a string

# Used to represent the currently logged in user
class User:
    """
    Used to represent a logged in user. 
    
    Since this program uses admin credentials you can't actually log in as a user. """
    def __init__(self, email):
        user = user_auth.get_user(email)
        self.uid = user.uid
        self.name = user.display_name
        self.email = user.email

#main start============================================================================================================
def main():
    # Use a service account
    cred = credentials.Certificate(".././practicefirestore-a4ca4-firebase-adminsdk-vnup5-67f9634197.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()


# Log in/ Register
    printmenu(0, "") # display login/register menu
    selector = input("Enter an option: ")
    valid = False
    while not valid:
        match selector:
            case "new": # register new user
                valid = True
                name = input("Enter name: ")
                email = input("Enter email: ")
                password = input("Enter password: ")
                user = user_auth.register_new_user(name, email, password) # creates new user and "logs in"(see readme)
                active_user = User(user.email) # we use this to immitate a logged in user
                # Add user to database 
                create_User_data(db, active_user.uid, name)
                # Add first list
                print("Add your first list")
                list_title = input("Enter list name: ")
                add_new_list(db, active_user.uid, list_title)
                # Add first task to list
                print("Add first task to list")
                lists_c_ref = get_list_c_ref(db, active_user.uid)
                list_d_ref = get_document_by_title(lists_c_ref, list_title) # get reference to target list
                add_new_task(list_d_ref, input("Enter task name: "))

            case "login": # "log in" existing user
                valid = True
                email = input("Enter email: ")
                password = input("Enter password: ") # since this is a mock login, the password isn't actually used here
                # uid = user_auth.get_uid(email)
                active_user = User(email) # We will still access the uid through the active user object which is just a representation for a logged in user
            case _:
                valid = False
                selector = input("Invalid enter again: ")

# List actions
    while True:
        # display lists menu 
        printmenu(1, active_user.name)
        selector = input("Enter an option: ")
        valid = False
        while not valid:
            match selector:
                case 'v': # view task lists
                    valid = True
                    show_lists(db, active_user.uid)

                    pass
                case 'a': # add new list
                    valid = True
                    list_title = input("Enter list name: ")
                    add_new_list(db, active_user.uid, list_title)
                    print("Add first task to list")
                    lists_c_ref = get_list_c_ref(db, active_user.uid)
                    list_d_ref = get_document_by_title(lists_c_ref, list_title) # get reference to target list
                    add_new_task(list_d_ref, input("Enter task name: "))
                case 'o': # open list
                    # input list to open and handle
                    list_title = input("Enter list name to open: ")
                    list_c_ref = get_list_c_ref(db,active_user.uid)
                    list_d_ref = get_document_by_title(list_c_ref, list_title)
                    while selector != 'b':
                        #print menu 2
                        printmenu(2, list_title)
                        selector = input("Enter an option: ")
                        valid = False
                        # Task actions
                        while not valid:
                            match selector:
                                case 'v': # view tasks
                                    valid = True
                                    show_tasks(db, active_user.uid, list_title)
                                case 'a': # add task
                                    valid = True
                                    add_new_task(list_d_ref, input("Enter task name: "))
                                case 'm': # mark task done/undone
                                    valid = True
                                    task_d_ref = get_document_by_title(list_d_ref.collection("Tasks"), input("Enter task name to mark: "))
                                    toggle_field(task_d_ref, "complete")
                                case 'e': # edit task
                                    valid = True
                                case 'd': # delete task
                                    valid = True
                                    task_c_ref = list_d_ref.collection("Tasks")
                                    task_d_ref = get_document_by_title(task_c_ref, input("Enter task name to delete: "))
                                    task_d_ref.delete() # delete from firebase
                                    # decrement list doc field, numTasks
                                    doc = list_d_ref.get()
                                    if doc.exists:
                                        num_tasks = doc.to_dict().get("numTasks") # get value
                                        num_tasks -= 1 # decrement
                                        list_d_ref.update({"numTasks": num_tasks}) # store updated value
                                    else:
                                        print("List document does not exist.")
                                    
                                case 'b': # go back to previous menu by exiting loop
                                    valid = True
                                case _:
                                    valid = False
                                    selector = input("Invalid enter again: ")
                case 'd': # delete tasks in list and list document
                    valid = True
                    list_c_ref = get_list_c_ref(db,active_user.uid)
                    list_d_ref = get_document_by_title(list_c_ref, input("Enter list name to delete: "))
                    task_c_ref = list_d_ref.collection("Tasks")
                    # get number of docs in collection
                    doc = list_d_ref.get()
                    if doc.exists:
                        num_tasks = doc.to_dict().get("numTasks")
                        delete_docs_in_Collection(task_c_ref, num_tasks) # delete all task docs in list collection
                        # now delete list doc
                        list_d_ref.delete()
                    else:
                        print("doc doesn't exist")
                    
                    pass
                case _:
                    valid = False
                    selector = input("Invalid enter again: ")


#main end****************************************************************************************************************
main()
