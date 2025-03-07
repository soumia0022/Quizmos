from better_profanity import profanity


class ProfanityFilterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            post_copy = request.POST.copy()
            for key, value in post_copy.items():
                if isinstance(value, str):
                    post_copy[key] = profanity.censor(value)
            request.POST = post_copy

        response = self.get_response(request)
        return response