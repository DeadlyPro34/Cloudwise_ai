from fastapi.testclient import TestClient
from app.main import app
import sys

client = TestClient(app)

# Diagnostic Test
print("=== GET /api/v1/aws/diagnostic ===")
r = client.get('/api/v1/aws/diagnostic')
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}")

# Auth
r = client.post('/api/v1/auth/register', json={'email':'diag2@test.ai','password':'TestPass123'})
if r.status_code in (400, 409): # user exists
    r = client.post('/api/v1/auth/login', data={'username':'diag2@test.ai','password':'TestPass123'})
token = r.json().get('access_token')
if not token:
    print(f"Failed to auth: {r.json()}")
    sys.exit(1)
headers = {'Authorization': f'Bearer {token}'}

tests = [
    {
        "name": "a. Empty access key / secret key",
        "payload": {'aws_access_key_id': '', 'aws_secret_access_key': '', 'region': 'us-east-1', 'use_localstack': False}
    },
    {
        "name": "b. Malformed access key (not starting with AKIA)",
        "payload": {'aws_access_key_id': 'BADKEY123', 'aws_secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY', 'region': 'us-east-1', 'use_localstack': False}
    },
    {
        "name": "c. Valid format but fake key",
        "payload": {'aws_access_key_id': 'AKIAIOSFODNN7EXAMPLE', 'aws_secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY', 'region': 'us-east-1', 'use_localstack': False}
    },
    {
        "name": "d. Valid credentials but wrong region typo",
        # Can't test valid credentials here since we don't have them, but we'll try a fake key with a bad region
        "payload": {'aws_access_key_id': 'AKIAIOSFODNN7EXAMPLE', 'aws_secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY', 'region': 'us-east-999', 'use_localstack': False}
    }
]

for t in tests:
    print(f"\n=== Test: {t['name']} ===")
    r = client.post('/api/v1/aws/connect', headers=headers, json=t['payload'])
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
