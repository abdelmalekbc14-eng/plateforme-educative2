from django.http import JsonResponse
import os

def health_check(request):
    """
    Health check endpoint for Consul.
    Returns 200 OK.
    """
    return JsonResponse({
        "status": "ok", 
        "service": os.environ.get("SERVICE_NAME", "unknown")
    })
