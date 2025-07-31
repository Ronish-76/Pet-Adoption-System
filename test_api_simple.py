from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test_api(request):
    return JsonResponse({
        'status': 'success',
        'message': 'API is working',
        'endpoints': {
            'pets': '/api/pets/',
            'accounts': '/api/accounts/',
            'adoptions': '/api/adoptions/',
            'chat': '/api/chat/'
        }
    })