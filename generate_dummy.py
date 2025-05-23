import json
import os
import random

DATA_DIR = "D:\\VSCodes\\test-form\\status-site\\submissions\\"
os.makedirs(DATA_DIR, exist_ok=True)

# Example dummy data generators
first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Evan']
last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown']
emails = ['example1@test.com', 'user2@test.com', 'foo@bar.com', 'hello@world.com']
phones = ['123-456-7890', '987-654-3210', '555-555-5555']
fav_foods = ['Pizza', 'Burger', 'Sushi', 'Pasta', 'Salad']

def get_next_ref_number_for_name(first_name, last_name):
    base_name = f"{first_name.lower()}_{last_name.lower()}"
    files = os.listdir(DATA_DIR)
    matching = [
        int(f.split('_')[-1].split('.')[0])
        for f in files
        if f.startswith(base_name) and f.endswith('.json') and f.split('_')[-1].split('.')[0].isdigit()
    ]
    return max(matching, default=0) + 1

def create_dummy_submission():
    return {
        "firstName": random.choice(first_names),
        "lastName": random.choice(last_names),
        "email": random.choice(emails),
        "phone": random.choice(phones),
        "favfood1": random.choice(fav_foods),
        "favfood2": random.choice(fav_foods),
        "favfood3": random.choice(fav_foods),
    }

def save_dummy_submissions(n):
    for _ in range(n):
        data = create_dummy_submission()
        first_name = data["firstName"].strip()
        last_name = data["lastName"].strip()

        ref_num = get_next_ref_number_for_name(first_name, last_name)
        filename = f"{first_name.lower()}_{last_name.lower()}_{ref_num}.json"
        filepath = os.path.join(DATA_DIR, filename)
        abs_path = os.path.abspath(filepath)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Saved submission #{ref_num} to: {abs_path}")

if __name__ == "__main__":
    num_submissions = 10  # Change this to how many dummy entries you want
    save_dummy_submissions(num_submissions)
