import json
from poll_management.models.poll_model import Poll
from user_management.models.user_model import User


def create_default_test_polls() -> None:
    """This function parses the default_polls.json fixture and creates Poll objects in the database."""

    # Currently, there is only one poll but can add more default polls later to the JSON
    with open('poll_management/tests/fixtures/default_poll.json', 'r') as file:
        polls = json.load(file)

        for poll_data in polls:
            poll_fields = poll_data.get('fields', {})

            # Convert user to a User instance (instead of just username in JSON)
            username = poll_fields.pop('user', None)  # Extract username
            if username:
                try:
                    user = User.objects.get(username=username)
                    poll_fields['user'] = user  # Assign the user object
                except User.DoesNotExist:
                    print(f"User with ID {username} does not exist. Skipping poll creation.")
                    continue

            poll, _ = Poll.objects.get_or_create(**poll_fields)
