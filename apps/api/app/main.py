import logging
import time
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("compliance-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Compliance as Code API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/controls")
def get_controls():
    return [
        {"id": "ISO-A.9.4.2", "framework": "ISO 27001", "name": "MFA Enforcement", "status": "Compliant"},
        {"id": "PCI-8.3", "framework": "PCI DSS", "name": "Secure Access", "status": "Non-Compliant"},
        {"id": "NIST-AC-1", "framework": "NIST CSF", "name": "Access Control Policy", "status": "Compliant"}
    ]

@app.get("/scores/summary")
def get_scores_summary():
    return {
        "global_compliance_score": 88.4,
        "iso_readiness": 92.0,
        "pci_alignment": 74.5,
        "nist_maturity": 85.2,
        "trend": "+1.2%"
    }

@app.get("/findings")
def get_findings():
    return [
        {"id": "F-001", "control": "MFA", "status": "Open", "severity": "Critical", "owner": "Team-Alpha"},
        {"id": "F-002", "control": "Encryption", "status": "Resolved", "severity": "High", "owner": "Team-Bravo"},
        {"id": "F-003", "control": "Logging", "status": "Open", "severity": "Medium", "owner": "Team-Charlie"}
    ]

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "active_assessments": 12,
        "open_findings": 45,
        "evidence_count": 1420,
        "last_scan": "2026-04-27T22:15:00Z"
    }
