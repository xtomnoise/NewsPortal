class FullOrMobileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # код, выполняемый до формирования ответа (или другого middleware)

        response = self.get_response(request)

        if request.mobile:
            prefix = "mobile/"
        else:
            prefix = "full/"
        response.template_name = prefix + response.template_name

        return response
