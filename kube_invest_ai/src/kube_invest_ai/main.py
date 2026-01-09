#!/usr/bin/env python
import sys
import warnings
import time
from datetime import datetime, timedelta
from kube_invest_ai.crew import KubeInvestAi
from kube_invest_ai.tools.custom_tool import watch_events, get_pod_logs

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

SEVERITY_THRESHOLD = 3
INCIDENT_TTL = timedelta(minutes=15)

PRIORITY_EVENTS_REASON = {"Failed", "ErrImagePull", "CrashLoopBackOff", "ImagePullBackOff"}

ERROR_KEYWORDS = [
    "error",
    "fatal",
    "exception",
    "panic",
    "oomkilled",
    "crashloopbackoff",
]
# Cache anti-bruit
INCIDENT_CACHE = {}

# ----------------------------
# UTILS
# ----------------------------
def has_error(log: str) -> bool:
    if not log or log == "No container logs available.":
        return False
    log = log.lower()
    return any(k in log for k in ERROR_KEYWORDS)

def compute_severity(event_reason: str, error_count: int) -> int:
    score = error_count * 2
    if event_reason in PRIORITY_EVENTS_REASON:
        score += 5
    return score

def recently_reported(key: str) -> bool:
    return key in INCIDENT_CACHE and \
        datetime.now() - INCIDENT_CACHE[key] < INCIDENT_TTL

def mark_reported(key: str):
    INCIDENT_CACHE[key] = datetime.now()

# ----------------------------
# MAIN LOOP
# ----------------------------
def run():
    print("🚀 DevOps IA Agent started (LLM = last resort)")
    crew_instance = KubeInvestAi().crew()
    # fake_incident = """
    #         Namespace: default
    #         Pod: nginx-test-agent-ai
    #         Reason: ErrImagePull
    #         Severity: 10
    #         Message: Failed to pull image "nginx:testtag": not found

    #         Logs:
    #         No container logs available.
    #         """

    # try:
    #     crew_instance.kickoff(inputs={"incident": fake_incident})
    # except Exception as e:
    #     print("error")

    for event in watch_events():
        print(event)
        if not event.involved_object:
            continue

        namespace = event.involved_object.namespace
        pod_name = event.involved_object.name
        reason = event.reason or "Unknown"

        incident_id = f"{namespace}:{pod_name}:{reason}"

        logs = ""
        try:
            logs = get_pod_logs(namespace, pod_name)
        except Exception:
            logs = "No container logs available."

        # Détection soit par logs, soit par event
        incident_detected = has_error(logs) or reason in PRIORITY_EVENTS_REASON

        if not incident_detected:
            continue

        error_count = sum(
            logs.lower().count(k) for k in ERROR_KEYWORDS
        )

        severity = compute_severity(reason, error_count)

        if severity < SEVERITY_THRESHOLD:
            continue

        if recently_reported(incident_id):
            continue

        context = f"""
        Namespace: {namespace}
        Pod: {pod_name}
        Reason: {reason}
        Severity: {severity}
        Message: {event.message}

        Logs:
        {logs[-1500:]}
        """
        print(f"🔥 Escalating incident {incident_id} to crewAI")

        try:
            crew_instance.kickoff(inputs={"incident": context})
        except Exception as e:
            print(f"⚠️ crewAI failed for {incident_id}: {e}")

        mark_reported(incident_id)
        time.sleep(1)

if __name__ == "__main__":
    run()
