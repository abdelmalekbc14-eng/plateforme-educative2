import os
import requests
import socket
import uuid

CONSUL_HOST = os.environ.get("CONSUL_HOST", "localhost")
CONSUL_PORT = os.environ.get("CONSUL_PORT", "8500")

def get_ip_address():
    # Allow manual override via .env (Crucial for multi-NIC PCs)
    if os.environ.get("SERVICE_HOST"):
        return os.environ.get("SERVICE_HOST")
    
    try:
        # Best effort to find LAN IP (not 127.0.0.1)
        # We connect to a UDP address (doesn't send data) to find the interface used for routing
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def register_service(service_name, service_port, service_id=None):
    # Use exact ID format requested: {SERVICE_NAME}-{SERVICE_PORT}
    if not service_id:
        service_id = f"{service_name}-{service_port}"
    
    url = f"http://{CONSUL_HOST}:{CONSUL_PORT}/v1/agent/service/register"
    
    address = get_ip_address()
    print(f"Service Discovery: Detected Host IP is {address}")


    # Define Traefik tags based on service name
    tags = ["django", "microservice", f"role-{service_name}", "traefik.enable=true"]
    
    # Routing logic
    # Traefik router names must be unique, so we usage service_id or service_name
    router_name = f"{service_name}-router"
    
    if service_name == "accounts":
        tags.append(f"traefik.http.routers.{router_name}.rule=PathPrefix(`/api/auth`)")
    elif service_name == "cours":
        tags.append(f"traefik.http.routers.{router_name}.rule=PathPrefix(`/api/cours`)")
    elif service_name == "timetable":
        tags.append(f"traefik.http.routers.{router_name}.rule=PathPrefix(`/api/timetable`)")
    elif service_name == "messaging":
        tags.append(f"traefik.http.routers.{router_name}.rule=PathPrefix(`/api/messaging`)")
    elif service_name == "frontend":
        # catch-all for frontend, but be careful not to override API
        tags.append(f"traefik.http.routers.{router_name}.rule=PathPrefix(`/`)")
    
    payload = {
        "ID": service_id,
        "Name": service_name,
        "Tags": tags,
        "Address": address,
        "Port": int(service_port),
        "Check": {
            "HTTP": f"http://{address}:{service_port}/health/",
            "Interval": "10s",
            "Timeout": "1s",
            "DeregisterCriticalServiceAfter": "1m"
        }
    }
    
    try:
        print(f"Attempting to register {service_name} at {address}:{service_port} to Consul...")
        res = requests.put(url, json=payload)
        if res.status_code == 200:
            print(f"Successfully registered {service_name} (ID: {service_id})")
            return service_id
        else:
            print(f"Failed to register service: {res.text}")
    except Exception as e:
        print(f"Consul connection error: {e}")
    return None

def deregister_service(service_id):
    if not service_id:
        return
    url = f"http://{CONSUL_HOST}:{CONSUL_PORT}/v1/agent/service/deregister/{service_id}"
    try:
        requests.put(url)
        print(f"Deregistered service {service_id}")
    except Exception as e:
        print(f"Error deregistering: {e}")
