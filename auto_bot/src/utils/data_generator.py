from faker import Faker
from faker.providers import person, internet, phone_number, lorem
from random import choice, choices, randint


fake = Faker('en_US')
fake.add_provider(internet)
fake.add_provider(person)
fake.add_provider(phone_number)
fake.add_provider(lorem)

def generate_customer():
    not_required_keys = [
        "firstname",
        "lastname",
        "phoneNum",
        "birthday",
        "username",
        "subscribed_for_newsletter",
    ]
    customer =  {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "email": fake.free_email(),
        "phoneNum": fake.phone_number(),
        "birthday": "2011-01-26",
        "username": fake.user_name(),
        "subscribed_for_newsletter": choice([True, False]),
        "password": "itIsAPassword",
        "password_confirmation": "itIsAPassword"
    }

    for key in set(choices(not_required_keys, k=randint(0, len(not_required_keys)))):
        del customer[key]
    
    return customer

def generate_post():
    return {
        "title": fake.paragraph(nb_sentences=2),
        "description": fake.paragraph(nb_sentences=20)
    }
