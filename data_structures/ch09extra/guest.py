#!/user/bin/env python3
class Guest:
    def __init__(self, firstname, middlename, lastname, 
                address = '', city = '', state = '', country = '', 
                email = '', greeting = '', visits=0):
        self.firstname = str(firstname).strip().capitalize()
        self.middlename = str(middlename).strip().capitalize()
        self.lastname = str(lastname).strip().capitalize()  
        self.address = str(address).strip().capitalize()
        self.city = str(city).strip().capitalize()
        self.state = str(state).strip().capitalize()    
        self.country = str(country).strip().capitalize()
        self.email = str(email).strip().lower()
        self.greeting = str(greeting).strip()
        self.visits = int(visits)

    @property
    def firstname(self):
        return self._firstname
    
    @firstname.setter
    def firstname(self, firstname):
        self._firstname = str(firstname).capitalize()

    @property
    def middlename(self):
        return self._middlename
    
    @middlename.setter  
    def middlename(self, middlename):
        self._middlename = str(middlename).capitalize()

    @property
    def lastname(self):
        return self._lastname
    
    @lastname.setter
    def lastname(self, lastname):
        self._lastname = str(lastname).capitalize()

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = str(address).capitalize()

    @property
    def city(self):
        return self._city
    
    @city.setter
    def city(self, city):
        self._city = str(city).capitalize()

    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state):
        self._state = str(state).capitalize()

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country):
        self._country = str(country).capitalize()

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        self._email = str(email).lower()

    @property
    def greeting(self):
        return self._greeting
    
    @greeting.setter
    def greeting(self, greeting):
        self._greeting = str(greeting).capitalize()

    @property
    def visits(self):
        return self._visits
    
    @visits.setter
    def visits(self, visits):
        self._visits = int(visits)

    # Improving serialization by delegating conversion to list here.
    def as_list(self):
        return [self.firstname, self.middlename, self.lastname,
                    self.address, self.city, self.state, self.country, 
                    self.email, self.greeting, self.visits]

    def __str__(self):
        return "Guset[First: {}, Middle: {}, Last: {}, Address: {}, {}, {}, {}, Email: {}, Greeting: {}, Visits: {}]".format(
            self.firstname, self.middlename, self.lastname, 
            self.address, self.city, self.state, self.country, 
            self.email, self.greeting, self.visits)  
          
    def __eq__(self, obj):
        if type(obj) != Guest:
            return False
        return (self._firstname == obj.firstname and self._middlename == obj.middlename and 
                self._lastname == obj.lastname and self.address == obj.address 
                and self.city == obj.city and self._state == obj.state and 
                self.country == obj.country and self.email == obj.email and
                self._greeting == obj.greeting and self.visits == obj.visits)

    def main():
        print ("This is a module, not meant to be run standalone")