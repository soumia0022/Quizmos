from better_profanity import profanity


class ProfanityFilterMiddleware:
    """Middleware that filters any post request.
        Uses profanity filter to filter out inappropriate/offensive words."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            self.filter_post_data(request)

        response = self.get_response(request)
        return response

    def filter_post_data(self, request):
        post_copy = request.POST.copy()
        keys = list(post_copy.keys())

        for key in keys:
            self.process_field(post_copy, key)

        request.POST = post_copy

    def process_field(self, post_data, key):
        values = post_data.getlist(key)
        cleaned_values = self.clean_values(values)

        post_data.pop(key)

        for value in cleaned_values:
            post_data.appendlist(key, value)

    def clean_values(self, values):
        cleaned_values = []
        for value in values:
            if isinstance(value, str):
                cleaned_values.append(profanity.censor(value))
            else:
                cleaned_values.append(value)
        return cleaned_values