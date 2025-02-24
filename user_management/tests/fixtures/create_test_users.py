import json
from user_management.models.user_model import User

# May require refactoring (I think it can be)

def create_default_test_user() -> None:
    """This function parses the default_user.json fixture and creates User objects in the database. """

    with open('user_management/tests/fixtures/default_user.json', 'r') as file:
        users = json.load(file)

        # Will require this for loop later as we add a student default user (and perhaps more)
        for user_data in users:
            user_fields = user_data.get('fields', {}) # Extract fields from fields key in JSON
            user, _ = User.objects.get_or_create(**user_fields) # Get or create the user using the extracted fields