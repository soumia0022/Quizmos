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
            user_id = poll_fields.pop('user', None)  # Extract user ID

            if user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    poll_fields['user'] = user  # Assign the user object
                except User.DoesNotExist:
                    print(f"User with ID {user_id} does not exist. Skipping poll creation.")
                    continue

            poll, _ = Poll.objects.get_or_create(**poll_fields)
