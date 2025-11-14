import os
import sys
from django.apps import AppConfig
from django.conf import settings

class ServiceDiscoveryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service_discovery'
    service_id = None

    def ready(self):
        # Register ONLY if we are running as a server (and not just reloading)
        # Django's auto-reloader sets RUN_MAIN='true' in the new process.
        # We want to run this logic in that process.
        
        # Check if we are running via "runserver"
        is_runserver = 'runserver' in sys.argv
        is_reload = os.environ.get('RUN_MAIN') == 'true'
        is_noreload = '--noreload' in sys.argv

        # Condition:
        # 1. runserver + auto-reload (default) -> registers only when RUN_MAIN='true'
        # 2. runserver + --noreload -> registers immediately (RUN_MAIN not set)
        
        should_register = False
        if is_runserver:
            if is_noreload:
                should_register = True
            elif is_reload:
                should_register = True
        
        if should_register:
            from .utils import register_service, deregister_service
            import atexit

            service_name = os.environ.get("SERVICE_NAME")
            service_port = os.environ.get("SERVICE_PORT")

            if service_name and service_port:
                print(f"Service Discovery: Registering {service_name}:{service_port}...")
                self.service_id = register_service(service_name, service_port)
                if self.service_id:
                    atexit.register(deregister_service, self.service_id)
            else:
                print("Service Discovery: SERVICE_NAME or SERVICE_PORT not set. Skipping registration.")
