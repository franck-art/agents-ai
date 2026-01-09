from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from kubernetes import client, config, watch
from kubernetes.config import ConfigException
import os


# def load_kube_config():
#     try:
#         config.load_incluster_config()
#     except ConfigException:
#         # fallback local dev
#         config.load_kube_config()
config.load_incluster_config()
v1_api = client.CoreV1Api()

SUSPICIOUS_EVENT_REASONS = {
    "Failed",
    "BackOff",
    "CrashLoopBackOff",
    "Unhealthy",
    "Killing",
    "OOMKilled",
    "Evicted",
}

def watch_events():
    # load_kube_config()
    w = watch.Watch()
    for event in w.stream(v1_api.list_event_for_all_namespaces):
        if event["object"].reason in SUSPICIOUS_EVENT_REASONS:
            yield event["object"]

def list_pods_all_namespaces() -> list[str]:
    """List all pods in all namespaces."""
    # load_kube_config()
    return [ pod.metadata.name for pod in v1_api.list_pod_for_all_namespaces().items ]

def get_pod_logs(namespace: str, pod_name: str) -> str:
    """Get the logs of a pod."""
    # load_kube_config()
    return v1_api.read_namespaced_pod_log(pod_name, namespace, tail_lines=200)

def list_pods(namespace: str) -> list[str]:
    """List all pods in a namespace."""
    # load_kube_config()
    return [ pod.metadata.name for pod in v1_api.list_namespaced_pod(namespace).items ]

def get_events(namespace: str) -> list[str]:
    """Get the events of a namespace."""
    # load_kube_config()
    return [ event.message for event in v1_api.list_namespaced_event(namespace).items ]


# class MyCustomToolInput(BaseModel):
#     """Input schema for MyCustomTool."""
#     argument: str = Field(..., description="Description of the argument.")

# class MyCustomTool(BaseTool):
#     name: str = "Name of my tool"
#     description: str = (
#         "Clear description for what this tool is useful for, your agent will need this information to use it."
#     )
#     args_schema: Type[BaseModel] = MyCustomToolInput

#     def _run(self, argument: str) -> str:
#         # Implementation goes here
#         return "this is an example of a tool output, ignore it and move along."
