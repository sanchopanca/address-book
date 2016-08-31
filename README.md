# address-book

address_book is a simple library for storing and querying data about persons

## Usage:

    
    >>> from address_book import AddressBook, Person, Address, PhoneNumber, Email, Group
    
    # Creating new addressbook in memory
    >>> book = AddressBook()
    
    # Or inside file
    >>> book = AddressBook('/home/user/workbook')
    
    # Add new person
    >>> book.add_person(Person('John',
    ...                        'Doe',
    ...                        Address('New York'),
    ...                        Email('john@example.com'),
    ...                        PhoneNumber('88005553535')))
    
    # Persons can have more than one address, email, and phone number (but at least one)
    >>> book.add_person(Person('John',
    ...                        'Doe',
    ...                        [Address('New York'), Address('Chicago')],
    ...                        [Email('john@example.com'), Email('john@gmail.com')]
    ...                        [PhoneNumber('88005553535'), PhoneNumber('88002000600')]))
    
    # Creating groups
    >>> work = Group('work')
    >>> friends = Group('friends')
    >>> family = Group('family')
    
    # Persons can have zero or more groups assigned to them
    # Groups must be added before users
    >>> book.add_person(Person('John',
    ...                        'Doe',
    ...                        Address('New York'),
    ...                        Email('john@example.com'),
    ...                        PhoneNumber('88005553535'),
    ...                        [friends, work]))
    
    # You can search by name
    >>> book.find_by_name('John')
    # or
    >>> book.find_by_name('Doe')
    # or
    >>> book.find_by_name('John Doe')
    # the method returns list of found Persons with such first, last or full name
    
    # You can serach by email
    >>> book.find_by_email('john@example.com')
    # or
    >>> book.find_by_email('john')
    # the method returns list of Persons that have an email address which stars with given string
    
    # You can get list of users in a particular group
    >>> book.get_group_members(work)
    
Public fields:

    Person:
    first_name: str
    last_name: str
    street_addresses: list of Address 
    emails: list of Email
    phone_numbers list of PhoneNumber
    groups: list of Group
    
    Address:
    address: str
    
    Email:
    email: str
    
    PhoneNumber:
    number: str
    
    Group:
    name: str
    
## Running Tests:
    python3 -m unittest
