import random
import time
import math
import uuid
import string

first_names = [
    "John", "Jane", "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Helen", "Ivan",
    "Ivy", "Jack", "Kate", "Liam", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Ryan", "Sophia",
    "Sarah", "Tom", "Uma", "Victor", "Wendy", "Xander", "Yvonne", "Zack", "Amelia", "Ben", "Chloe",
    "Cathy", "Dylan", "Ella", "Finn", "Gina", "Henry", "Iris", "Jake", "Kelly", "Luke", "Megan",
    "Molly", "Nathan", "Olive", "Paul", "Quincy", "Riley", "Samantha", "Toby", "Ursula", "Violet",
    "Will", "Xena", "Yara", "Zane", "Ava", "Bella", "Caleb", "Daisy", "Ethan", "Fiona", "Gavin",
]

last_names = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez",
    "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King",
    "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter",
    "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards",
    "Collins", "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy",
]

email_domains = [
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "protonmail.com",
    "sharif.edu", "mit.edu", "harvard.edu", "oxford.ac.uk", "cam.ac.uk", "stanford.edu",
]

roles = ['admin', 'customer', 'driver', 'restaurant_admin']

address_lines_1 = [
    "123 Main St", "456 Elm St", "789 Oak St", "101 Pine St", "202 Maple St",
    "303 Cedar St", "404 Walnut St", "505 Spruce St", "606 Birch St", "707 Ash St",
    "808 Hickory St", "909 Cherry St", "111 Chestnut St", "222 Poplar St", "333 Sycamore St",
    "444 Dogwood St", "555 Willow St", "666 Magnolia St", "777 Locust St", "888 Mulberry St", "999 Cedar St",
]

address_lines_2 = [
    "Apt 101", "Apt 202", "Apt 303", "Apt 404", "Apt 505",
    "Apt 606", "Apt 707", "Apt 808", "Apt 909", "Apt 111",
    "Apt 222", "Apt 333", "Apt 444", "Apt 555", "Apt 666",
    "Apt 777", "Apt 888", "Apt 999",
]

food_items = [pizza, burger, kebab, sushi, pasta, salad, sandwich, steak, taco, waffle, wrap, yogurt]

prices = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

base_location = [
    "latitude": 35.741228,
    "longitude": 51.399940,
]
radius_m = 5000


def generate_location() -> dict:
    latitude = base_location["latitude"] + random.uniform(-1, 1) * (radius_m/6378137e3) * (180/math.pi)
    longitude = base_location["longitude"] + random.uniform(-1, 1) * (radius_m/6378137e3) * (180/math.pi) / math.cos(base_location["latitude"] * math.pi/180)
    return {
        "latitude": latitude,
        "longitude": longitude
    }

def generate_first_name() -> str:
    return random.choice(first_names)

def generate_last_name() -> str:
    return random.choice(last_names)

def generate_email(first_name: str, last_name: str) -> str:
    domain = random.choice(email_domains)
    random_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    return f"{first_name.lower()}.{last_name.lower()}.{random_str}@{domain}"

def generate_password(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_national_id() -> str:
    return ''.join(random.choice(string.digits) for _ in range(10))

def generate_phone_number() -> str:
    return '09' + ''.join(random.choice(string.digits) for _ in range(9))




def generate_user(role: str) -> dict:
    if role not in roles:
        raise ValueError(f"Invalid role: {role}. Must be one of {roles}.")

    first_name = generate_first_name()
    last_name = generate_last_name()
    email = generate_email(first_name, last_name)
    password = generate_password()
    national_id = generate_national_id()
    phone_number = generate_phone_number()

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "role": role,
        "national_id": national_id,
        "phone_number": phone_number,
    }

def generate_vehicle(driver_id) -> dict:
    license_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    plate_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    return {
        "driver_id": driver_id,
        "license_number": license_number,
        "plate_number": plate_number,
    }
    
def generate_restaurant(restaurant_admin_id: str) -> dict:
    name = random.choice(first_names) + "'s " + random.choice(["Pizza", "Burger", "Kebab", "Sushi", "Pasta", "Salad", "Sandwich", "Steak", "Taco", "Waffle", "Wrap", "Yogurt", "Ziti"])
    location = generate_location()
    return {
        "restaurant_id": restaurant_admin_id,
        "name": name,
        **location,
    }

def generate_address(user_id: str) -> dict:
    address_line_1 = random.choice(address_lines_1)
    address_line_2 = random.choice(address_lines_2)
    city = "Tehran"
    country = "IR"
    postal_code = ''.join(random.choice(string.digits) for _ in range(10))
    location = generate_location()
    return {
        "user_id": user_id,
        "address_line_1": address_line_1,
        "address_line_2": address_line_2,
        "city": city,
        "postal_code": postal_code,
        **location,
    }

def generate_menu(restaurant_id: str) -> dict:
    menu = []
    for _ in range(random.randint(5, 10)):
        menu.append(generate_food_item())


    return {
        "restaurant_id": restaurant_id,
        "menu": menu,
    }

def generate_food_item(restaurant_id: str) -> dict:
    name = random.choice(food_items)
    price = random.choice(prices)
    count = random.randint(1, 10)
    return {
        "restaurant_id": restaurant_id,
        "name": name,
        "price": price,
        "count": count,
        "description": f"{name} with {random.choice(['extra cheese', 'extra sauce', 'extra meat', 'extra veggies', 'extra spice'])}",
    }



class Driver:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.vehicles = []
        self.location = generate_location()
        self.current_order = None
        self.status = 'deactive'
        self.random_walk_step = 10

    def random_walk(self, time_interval: int):
        for _ in range(time_interval):
            self.location['latitude'] = self.location['latitude'] + random.uniform(-1, 1) * (self.random_walk_step/6378137e3) * (180/math.pi)
            self.location['longitude'] = self.location['latitude'] + random.uniform(-1, 1) * (self.random_walk_step/6378137e3) * (180/math.pi)

    def take_steps_towards(self, destination: dict, step_size: float):
        dx = destination["latitude"] - self.location["latitude"]
        dy = destination["longitude"] - self.location["longitude"]

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            step_lat = dx / distance * (step_size / 6378137) * (180 / math.pi)
            step_lon = dy / distance * (step_size / 6378137) * (180 / math.pi) / math.cos(
                self.location["latitude"] * math.pi / 180)
        else:
            step_lat = 0
            step_lon = 0

        self.location["latitude"] += step_lat
        self.location["longitude"] += step_lon


