import unittest

from address_book import AddressBook, Person, Address, PhoneNumber, Email, Group


class TestAddressBook(unittest.TestCase):
    def test_find_by_first_name(self):
        book = AddressBook()
        book.add_person(Person('John', 'Doe', Address('New York'),
                               Email('john@example.com'),
                               PhoneNumber('88005553535')))
        entries = book.find_by_name('John')
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry.first_name, 'John')
        self.assertEqual(entry.last_name, 'Doe')
        self.assertEqual(entry.street_addresses[0].address, 'New York')
        self.assertEqual(entry.emails[0].email, ['john@example.com'])
        self.assertEqual(entry.phone_numbers[0].number, ['88005553535'])
        self.assertEqual(entry.groups, [])

    def test_find_by_last_name(self):
        book = AddressBook()
        book.add_person(Person('John', 'Doe', Address('New York'),
                               Email('john@example.com'),
                               PhoneNumber('88005553535')))
        book.add_person(Person('Jane', 'Doe', Address('Chicago'),
                               Email('jane@example.com'),
                               PhoneNumber('2128506')))
        entries = book.find_by_name('Doe')
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].last_name, 'Doe')
        self.assertEqual(entries[1].last_name, 'Doe')

        self.assertEqual(len(book.find_by_name('Ivanov')), 0)

    def test_find_by_full_name(self):
        book = AddressBook()
        book.add_person(Person('John', 'Doe', Address('New York'),
                               Email('john@example.com'),
                               PhoneNumber('88005553535')))
        book.add_person(Person('Jane', 'Doe', Address('Chicago'),
                               Email('jane@example.com'),
                               PhoneNumber('2128506')))
        entries = book.find_by_name('John Doe')
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry.first_name, 'John')
        self.assertEqual(entry.last_name, 'Doe')

        self.assertEqual(len(book.find_by_name('Ivan Ivanov')), 0)

    def test_find_by_email(self):
        book = AddressBook()
        book.add_person(Person('John', 'Doe', Address('New York'),
                               Email('john@example.com'),
                               PhoneNumber('88005553535')))
        book.add_person(Person('Jane', 'Doe', Address('Chicago'),
                               Email('jane@example.com'),
                               PhoneNumber('2128506')))
        entries = book.find_by_email('john@example.com')
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry.first_name, 'John')
        self.assertEqual(entry.last_name, 'Doe')
        entries = book.find_by_email('jan')
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry.first_name, 'Jane')
        self.assertEqual(entry.last_name, 'Doe')

    def test_get_group_members(self):
        book = AddressBook()
        family = Group('family')
        friends = Group('friends')
        work = Group('work')
        book.add_group(family)
        book.add_group(friends)
        book.add_group(work)

        book.add_person(Person('John', 'Doe', Address('New York'),
                               Email('john@example.com'),
                               PhoneNumber('88005553535'),
                               friends))
        book.add_person(Person('Jane', 'Doe', Address('Chicago'),
                               Email('jane@example.com'),
                               PhoneNumber('2128506'),
                               [friends, work]))

        entries = book.get_group_members(work)
        self.assertEqual(len(entries), 2)
        self.assertEqual({entries[0].first_name, entries[1].first_name}, {'John', 'Jane'})

        entries = book.get_group_members(friends)
        self.assertEqual(len(entries), 1)

        entries = book.get_group_members(family)
        self.assertEqual(len(entries), 0)
