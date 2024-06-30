import os
import docker
from dotenv import load_dotenv

def get_dynamic_port(container_name, internal_port):
    load_dotenv()

    client = docker.from_env()
    container = client.containers.get(container_name)
    ports = container.attrs['NetworkSettings']['Ports']
    dynamic_port = ports[f"{internal_port}/tcp"][0]['HostPort']
    return dynamic_port
