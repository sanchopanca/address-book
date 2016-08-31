class AddressBook:
    def __init__(self, filename=None):
        pass

    def add_person(self, person):
        pass

    def add_group(self, group):
        pass

    def get_group_members(self, group):
        pass

    def find_by_name(self, name):
        pass

    def find_by_email(self, email):
        pass


class Person:
    def __init__(self, firstname, lastname, street_addresses,
                 emails, phone_numbers, groups=None):
        pass


class Email:
    def __init__(self, email):
        pass


class Address:
    def __init__(self, address):
        pass


class PhoneNumber:
    def __init__(self, number):
        pass


class Group:
    def __init__(self, name):
        pass

