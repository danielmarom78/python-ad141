#!/user/bin/env python3
import os
from guest import Guest
from flask import Flask, request, session, render_template

guestfile = "guests.csv"
app = Flask(__name__)

#python -c 'import secrets;print(secrets.token_hex())'
app.secret_key = b'1fa795a702aa677d6cc6280800ea76e05412d58b8b86c4ab35a742e8b44cfb89'

def init():
    os.makedirs(os.path.dirname(guestfile), exist_ok=True)  # Ensure directories exist
    if not os.path.exists(guestfile):
        print("INFO: Creating new empty guestfile")
        gf = open(guestfile, "w"); gf.close()
    elif not (os.stat(guestfile).st_mode & 0o600) == 0o600:
        raise FileExistsError("ERROR: guest book exists but it does not have R/W permissions")
    else
        print("INFO: File is OK")
        

def find_user(user: Guest):
    print("INFO: Searching for {}".format(str(user)))
    def get_customers():
        with open(guestfile, "r") as gb:
            for customer in gb.readlines():
                yield customer.strip().split(",")
        
    for customer in get_customers():  # Call the function here
        if customer[0] == user.firstname and customer[1] == user.middlename and customer[2] == user.lastname:
            print("INFO: search found customer{}".format(str(customer)))
            return Guest(*customer)

    print("INFO: search found no matches")
    return None

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
                print("INFO: Updating user data{}".format(str(customer)))
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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET" and not 'firstname' in session:
        return render_template("login_form.html")
    
    if request.method == "POST" and not 'firstname' in session:
        user_param = []
        for param in ["firstname", "middlename", "lastname"]:
            session[param] = request.form[param]
            user_param.append(session[param])

        user = find_user(Guest(*user_param))

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