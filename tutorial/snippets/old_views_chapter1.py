# FUNCTION-BASED VIEWS WITHOUT API FUNCTIONALITY

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

@csrf_exempt # This decorator marks a view as being exempt from the protection ensured by the middleware.

# The CSRF middleware and template tag provides easy-to-use protection against Cross Site Request Forgeries. This type of attack occurs when a malicious website contains a link, a form button or some JavaScript that is intended to perform some action on your website, using the credentials of a logged-in user who visits the malicious site in their browser. A related type of attack, ‘login CSRF’, where an attacking site tricks a user’s browser into logging into a site with someone else’s credentials, is also covered.

# NOTE: "Because we want to be able to POST to this view from clients that won't have a CSRF token we need to mark the view as csrf_exempt. This isn't something that you'd normally want to do, and REST framework views actually use more sensible behavior than this, but it'll do for our purposes right now."

def snippet_list(request): # function-based list view
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True) # many=True option to retrieve a list of objects instead of a single object instance
        return JsonResponse(serializer.data, safe=False) # TODO: Research safe option for JsonResponse

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201) # 201 Created: The request has been fulfilled, resulting in the creation of a new resource.
        return JsonResponse(serializer.errors, status=400) # 400 Bad Request: The server cannot or will not process the request due to an apparent client error (e.g., malformed request syntax, size too large, invalid request message framing, or deceptive request routing).

@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk) # Fetch the object from the Snippet model
    except Snippet.DoesNotExist:
        return HttpResponse(status=404) # 404 Not Found: The requested resource could not be found but may be available in the future. Subsequent requests by the client are permissible.

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet) # Serialize the retrieved object
        return JsonResponse(serializer.data) # Return the server response (data) in JSON format to the client

    elif request.method == 'PUT': # Akin to SQL update clause
        data = JSONParser().parse(request) # Parse the client request into a JSON object
        serializer = SnippetSerializer(snippet, data=data) # Passing snippet instance before data=data instantiates serializer with the existing information in snippet, before updating it with the information stored in data

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204) # 204 No Content: The server successfully processed the request and is not returning any content.
