#!/user/bin/env python3
import os
from guest import Guest
from flask import Flask, request, session, render_template

guestfile = "data_structures/ch09extra/guests.csv"
app = Flask(__name__)

# Thius will be used as the cryptographic key for session data, which
# must be encrypted to be safe. You can generate a new key using:
# python -c 'import secrets; print(secrets.token_hex())'
app.secret_key = b'1fa795a702aa677d6cc6280800ea76e05412d58b8b86c4ab35a742e8b44cfb89'

# Make sure the guest file exists and is read-write
def init():
    if not os.path.exists(guestfile):
        print("INFO: Creating new empty guestfile.")
        gf = open(guestfile, "w"); gf.close()
    elif not (os.stat(guestfile).st_mode & 0o600) == 0o600:
        raise FileExistsError("ERROR: guest book exists but it does not have R/W permissions")
      
# Use a generator in a nested functionto search records one by one,
# untill we find the matching one. Return a new Guest or name
def find_user(user: Guest):
    print("INFO: Searching for {}".format(str(user)))
    def get_customers():
        with open(guestfile, "r") as gb:
            for customer in gb.readlines():
                yield customer.strip().split(",")
        
    for customer in get_customers():  # Call the function here
        if customer[0] == user.firstname and customer[1] == user.middlename and customer[2] == user.lastname:
            print("INFO: search found {}".format(customer))
            return Guest(*customer)

    print("INFO: search found no matches")
    return None

# for now, there is no smart way to do this. Just copy the entire
# file into new one, looking at each record to see if this is our
# current user. If no, write the new data instead, if not, just copy
# the record and move on. When finished, if there was no update, add
# our current user at the end of the file, and replace the old file
# with the new one
def store_user_date(user: Guest):
    print("INFO: Storing user data{}".format(str(user)))
    def get_customers():
        with open(guestfile, "r") as gb:
            for customer in gb.readlines():
                yield customer.strip().split(",")

    updated = False
    with open(guestfile + ".tmp", "w") as wb:
        for customer in get_customers():
            if customer[0] == user.firstname and customer[1] == user.middlename and customer[2] == user.lastname:
                print("INFO: Updating existing record{}".format(str(customer)))
                updated = True
                print(*user.as_list(), sep=",", file=wb)
            else:
                print(*customer, sep=",", file=wb)

    #Replace the old guest file with the new one
    os.replace(guestfile + ".tmp", guestfile)

    if updated:
        return
    
    with open(guestfile, "a") as ab:
        print("INFO: Adding new user data{}".format(str(user)))
        print(*user.as_list(), sep=",", file=ab)

# Everything happens at the root url. the user cound land here:
# - opening the page for the first time, with no session
#      -> We need to present them with a "login" form
# - After creating a session by sending their login data
#      -> We need to find the user in the guest book or add them
@app.route("/", methods=["GET", "POST"])
def index():
    # If the request is a GET and there is no session, show the login form
    if request.method == "GET" and not 'firstname' in session:
        return render_template("login_form.html")
    
    # If the request is a POST and there is no session. Expect login Data
    if request.method == "POST" and not 'firstname' in session:
        # Store the user data in the session, but also to create a Guest
        user_param = []
        for param in ["firstname", "middlename", "lastname"]:
            session[param] = request.form[param]
            user_param.append(session[param])

        # Check if the user is in the guest book
        user = find_user(Guest(*user_param)) # the * openes the list in to 3 params

        # User not found, show the user data form
        if not user:
            return render_template("user_data.html", fn = session['firstname'],
                                                       mn = session['middlename'], 
                                                       ln = session['lastname'])
        
        #User found, increment the visit count
        user.visits += 1

        # Store aditional user data in the session
        session['address'] = user.address
        session['city'] = user.city
        session['state'] = user.state
        session['country'] = user.country
        session['email'] = user.email
        session['greeting'] = user.greeting
        session['visits'] = user.visits
        store_user_date(user)

        #Greet the user
        return render_template("greet_user.html", user = user)
    
    # The request is a POST and the session exists. We got more user data
    if request.method == "POST":
        user_param = []
        # Store aditional data in the session
        for param in ["firstname", "middlename", "lastname",
                        "address", "city", "state", "country",
                        "email", "greeting"]:
            session[param] = request.form[param]
            user_param.append(session[param])

        # first visit, append 1
        user_param.append(1)
        session['visits'] = 1

        # Store the user data
        user = Guest(*user_param)
        store_user_date(user)

        #Greet the user
        return render_template("greet_user.html", user = user)
    
    # The request is Niether the above. Just show a greeting page
    user_param = []
    for param in ["firstname", "middlename", "lastname",
                   "address", "city", "state", "country",
                     "email", "greeting", "visits"]:
        if param in session:
            if param == "visits":
                user_param.append(int(session[param]))  # Ensure visits is an integer
            else:
                user_param.append(session[param])
        else:
            if param == "visits":
                user_param.append(0)  # Default visits to 0 if not in session
            else:
                user_param.append('')
    user = Guest(*user_param)

    return render_template("greet_user.html", user = user)

# custom err page
@app.errorhandler(404)
def page_not_found(e):
    return "ERROR: This url is not recognized. \n", 404

@app.route("/del", methods=["GET"])
def delete_guestfile():
    if os.path.exists(guestfile):
        os.remove(guestfile)
        return "Guest file deleted successfully.", 200
    else:
        return "Guest file does not exist.", 404

if __name__ == "__main__":
    init()  # Call the init function to ensure the file is created
    print("ERROR: This script is not meant to be run directly")