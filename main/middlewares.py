from django.http import HttpResponseRedirect


class TestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if ("AuthToken" not in request.COOKIES and
                request.path != "/login/" and request.path != "/sign-up/" and
                request.method != "POST"):
            return HttpResponseRedirect('/login/')

        response = self.get_response(request)

        return response
