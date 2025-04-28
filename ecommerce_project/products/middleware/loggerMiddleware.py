class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Corrected string interpolation
        print(f'[Middleware] {request.path} - {request.method}')

        # Call the response
        response = self.get_response(request)

        print(f'[Middleware] Status code: {response.status_code}')

        return response