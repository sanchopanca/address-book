import sqlite3


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
class AddressBook:
    def __init__(self, filename=None):
        if filename is None:
            filename = ':memory:'
        self._connection = self._init_db(filename)

    def add_person(self, person):
        c = self._connection.cursor()

        try:
            # We need to be sure that group exists
            for group in person.groups:
                c.execute('SELECT name FROM groups WHERE name = ?', (group.name,))
                _ = c.fetchone()

            c.execute('INSERT INTO persons '
                      '(first_name, last_name) VALUES (?, ?)',
                      (person.first_name, person.last_name))
            person_id = c.lastrowid
            for entry in person.street_addresses:
                c.execute('INSERT INTO addresses '
                          '(address, person_id) VALUES (?, ?)',
                          (entry.address, person_id))
            for entry in person.emails:
                c.execute('INSERT INTO emails '
                          '(email, person_id) VALUES (?, ?)',
                          (entry.email, person_id))
            for entry in person.phone_numbers:
                c.execute('INSERT INTO phone_numbers '
                          '(phone_number, person_id) VALUES (?, ?)',
                          (entry.number, person_id))
            for group in person.groups:
                c.execute('INSERT INTO persons_groups '
                          '(person_id, group_name) VALUES (?, ?)',
                          (person_id, group.name))
            self._connection.commit()
        except sqlite3.Error:
            self._connection.rollback()
            raise

    def add_group(self, group):
        c = self._connection.cursor()
        c.execute('INSERT INTO groups (name) VALUES (?)', (group.name,))
        self._connection.commit()

    def get_group_members(self, group):
        c = self._connection.cursor()
        c.execute('SELECT person_id FROM persons_groups WHERE group_name = ?', (group.name,))
        return [self._get_person(row[0]) for row in c.fetchall()]

    def find_by_name(self, name):
        c = self._connection.cursor()
        c.execute('SELECT id FROM persons WHERE first_name = ? COLLATE NOCASE', (name,))
        ids_by_first_name = {row[0] for row in c.fetchall()}
        c.execute('SELECT id FROM persons WHERE last_name = ? COLLATE NOCASE', (name,))
        ids_by_last_name = {row[0] for row in c.fetchall()}
        # TODO first and last names may contain spaces
        if ' ' in name:
            splitted = name.split()
            first_name, last_name = splitted[0], splitted[1]
            c.execute('SELECT id FROM persons WHERE first_name = ? AND last_name = ? COLLATE NOCASE',
                      (first_name, last_name))
            ids_by_full_name = {row[0] for row in c.fetchall()}
        else:
            ids_by_full_name = set()
        return [self._get_person(id_) for id_ in ids_by_first_name | ids_by_last_name | ids_by_full_name]

    def find_by_email(self, email):
        c = self._connection.cursor()
        c.execute('SELECT person_id FROM emails WHERE email LIKE ?',
                  ('{}%'.format(email),))
        return [self._get_person(row[0]) for row in c.fetchall()]

    def _get_person(self, id_):
        c = self._connection.cursor()
        c.execute('SELECT first_name, last_name '
                  'FROM persons WHERE id = ?', (id_,))
        result = c.fetchone()
        first_name, last_name = result[0], result[1]

        c.execute('SELECT email FROM emails WHERE person_id = ?', (id_,))
        emails = [Email(row[0]) for row in c.fetchall()]

        c.execute('SELECT address FROM addresses WHERE person_id = ?', (id_,))
        addresses = [Address(row[0]) for row in c.fetchall()]

        c.execute('SELECT phone_number FROM phone_numbers WHERE person_id = ?', (id_,))
        phone_numbers = [PhoneNumber(row[0]) for row in c.fetchall()]

        c.execute('SELECT group_name FROM persons_groups WHERE person_id = ?', (id_,))
        groups = [Group(row[0]) for row in c.fetchall()]

        return Person(first_name, last_name, addresses, emails, phone_numbers, groups)

    @staticmethod
    def _init_db(filename):
        connection = sqlite3.connect(filename)
        c = connection.cursor()
        c.execute('PRAGMA foreign_keys = ON')
        c.execute('CREATE TABLE IF NOT EXISTS persons '
                  '(id INTEGER  PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS emails '
                  '(id INTEGER  PRIMARY KEY AUTOINCREMENT, email TEXT, person_id INTEGER, '
                  'FOREIGN KEY(person_id) REFERENCES persons(id))')
        c.execute('CREATE TABLE IF NOT EXISTS addresses '
                  '(id INTEGER  PRIMARY KEY AUTOINCREMENT, address TEXT, person_id INTEGER, '
                  'FOREIGN KEY(person_id) REFERENCES persons(id))')
        c.execute('CREATE TABLE IF NOT EXISTS phone_numbers '
                  '(id INTEGER  PRIMARY KEY AUTOINCREMENT, phone_number TEXT, person_id INTEGER, '
                  'FOREIGN KEY(person_id) REFERENCES persons(id))')
        c.execute('CREATE TABLE IF NOT EXISTS groups (name TEXT PRIMARY KEY)')
        c.execute('CREATE TABLE IF NOT EXISTS persons_groups '
                  '(person_id INTEGER, group_name TEXT,'
                  'FOREIGN KEY(person_id) REFERENCES persons(id) '
                  'FOREIGN KEY(group_name) REFERENCES groups(name))')
        return connection


class Person:
    def __init__(self, first_name, last_name, street_addresses,
                 emails, phone_numbers, groups=None):
        self.first_name = first_name
        self.last_name = last_name
        if isinstance(street_addresses, list):
            self.street_addresses = street_addresses
        else:
            self.street_addresses = [street_addresses]
        if isinstance(emails, list):
            self.emails = emails
        else:
            self.emails = [emails]
        if isinstance(phone_numbers, list):
            self.phone_numbers = phone_numbers
        else:
            self.phone_numbers = [phone_numbers]
        if groups is None:
            self.groups = []
        elif isinstance(groups, list):
            self.groups = groups
        else:
            self.groups = [groups]


class Email:
    def __init__(self, email):
        self.email = email


class Address:
    def __init__(self, address):
        self.address = address


class PhoneNumber:
    def __init__(self, number):
        self.number = number


class Group:
    def __init__(self, name):
        self.name = name
