# CloudWise AI - IMPLEMENTATION.md v2.0

## Project Status

Version: 2.0

Status: Active Development

Deployment Target: Production

Last Updated: June 2026

---

# 1. Project Overview

CloudWise AI is a FinOps SaaS platform that enables organizations to analyze cloud infrastructure, identify cost optimization opportunities, forecast spending, and generate actionable recommendations.

The platform supports:

* Real AWS Accounts
* LocalStack Development Environment
* Demo Mode
* AI-Assisted Cost Analysis
* Infrastructure Discovery
* Cost Forecasting
* Executive Reporting

---

# 2. Core Objectives

Users should be able to:

Register
→ Login
→ Connect AWS or LocalStack
→ Scan Infrastructure
→ Discover Resources
→ View Dashboard
→ Analyze Costs
→ Review Recommendations
→ Generate Reports
→ Interact with AI Copilot

without technical intervention.

---

# 3. Current Feature Set

## Authentication

Implemented:

* User Registration
* User Login
* JWT Authentication
* Protected Routes
* Session Validation
* Forgot Password
* Reset Password

Database Tables:

* users
* password_resets

---

## Cloud Account Management

Implemented:

* AWS Credential Validation
* STS Identity Verification
* Multi-Account Support Structure

Database Tables:

* cloud_accounts

---

## AWS Integration

### Supported Discovery Services

Currently Active:

* EC2
* EBS

Future:

* S3
* RDS
* Lambda
* ECS
* CloudFront

---

## LocalStack Support

Implemented:

Frontend Toggle:

Use LocalStack

Backend Behavior:

AWS Mode:

endpoint_url=None

LocalStack Mode:

endpoint_url=http://localhost:4566

Supported Through:

* STS
* EC2
* EBS
* CloudWatch
* Cost Collection Layer

---

# 4. Resource Discovery Engine

## Flow

Connect Cloud Account
↓
Validate Credentials
↓
Create Session
↓
Discover EC2
↓
Discover EBS
↓
Normalize Resource Data
↓
Store Resource Inventory
↓
Generate Metrics
↓
Generate Recommendations

---

## Discovery Functions

backend/app/services/aws_service.py

Functions:

connect_aws()

discover_ec2()

discover_ebs()

get_cost_data()

get_cloudwatch_metrics()

---

## Resource Inventory

Stores:

* Resource ID
* Resource Name
* Resource Type
* Status
* Region
* Tags
* Metadata

Supported Types:

* EC2
* EBS

---

# 5. Recommendation Engine

## Version 1 Rules

### EC2

Idle Instance Detection

Condition:

CPU Utilization < 5%

Recommendation:

Resize or Terminate

Priority:

High

---

Stopped Instance Detection

Condition:

Instance Status = Stopped

Recommendation:

Delete Unused Resource

Priority:

Medium

---

Oversized Instance Detection

Condition:

Instance Size > Usage Pattern

Recommendation:

Rightsize Instance

Priority:

High

---

### EBS

Unattached Volume Detection

Condition:

No Attachments

Recommendation:

Delete Volume

Priority:

High

---

Oversized Volume Detection

Condition:

Low Utilization

Recommendation:

Reduce Volume Size

Priority:

Medium

---

# 6. Dashboard System

## Dashboard KPIs

### Total Resources

Source:

resource_inventory

Includes:

* EC2
* EBS

---

### Monthly Spend

Source:

Cost Engine

---

### Potential Savings

Source:

Recommendation Engine

---

### Cloud Health Score

Calculated Using:

* Resource Efficiency
* Cost Efficiency
* Optimization Coverage

Range:

0 – 100

---

# 7. Forecasting Engine

Supported Windows:

* 7 Days
* 30 Days
* 90 Days

Outputs:

* Forecasted Spend
* Trend Direction
* Cost Risk Level

---

# 8. AI Copilot

Purpose:

Explain cloud spending in natural language.

Supported Questions:

* Why is spending increasing?
* Which resource costs the most?
* How can I reduce costs?
* Explain this recommendation.
* What should I optimize first?

Context Sources:

* Resources
* Metrics
* Recommendations
* Forecasts

---

# 9. Reports Module

Supported Reports

Executive Report

Contains:

* Spend Overview
* Savings Opportunities
* Forecast
* Health Score

---

Technical Report

Contains:

* Resource Inventory
* Metrics
* Recommendations
* Infrastructure Summary

Formats:

* PDF
* CSV

---

# 10. Demo Mode

Purpose:

Prevent empty dashboards during demonstrations.

Environment Variable:

DEMO_MODE=true

Behavior:

true

Loads Seed Data

false

Uses Real Cloud Integrations

---

## Seed Dataset

EC2

* Idle Instance
* Healthy Instance
* Oversized Instance
* Stopped Instance

EBS

* Attached Volume
* Unattached Volume
* Archive Candidate Volume

---

Commands

Seed Database:

python seed_demo_data.py

Populate LocalStack:

python setup_localstack.py

---

# 11. Frontend Modules

Public Pages

* Landing Page
* Login
* Register
* Forgot Password

---

Authenticated Pages

* Dashboard
* Resources
* Recommendations
* Forecasting
* Reports
* AI Copilot
* Settings

---

# 12. Deployment Strategy

Frontend

Platform:

Vercel

---

Backend

Platform:

Render

---

Database

Platform:

Render PostgreSQL

---

Environment Variables

DATABASE_URL=

JWT_SECRET=

OPENAI_API_KEY=

AWS_REGION=us-east-1

LOCALSTACK_URL=http://localhost:4566

DEMO_MODE=false

---

# 13. Logging & Observability

Temporary Debug Logging

Track:

* EC2 Resources Discovered
* EBS Resources Discovered
* Resources Saved
* Dashboard Records Returned
* Recommendation Count
* Forecast Generation

Purpose:

Verify complete AWS → Database → Dashboard pipeline.

---

# 14. Testing Checklist

Authentication

* Register
* Login
* Forgot Password
* Reset Password

---

AWS

* Connect AWS
* Validate STS
* Discover EC2
* Discover EBS

---

LocalStack

* Connect LocalStack
* Discover EC2
* Discover EBS
* Seed Data Verification

---

Dashboard

* Total Resources
* Monthly Spend
* Potential Savings
* Health Score

---

Recommendations

* Idle EC2
* Stopped EC2
* Unattached EBS
* Oversized EBS

---

Reports

* PDF Export
* CSV Export

---

# 15. Phase 2 Roadmap

Additional Services

* S3
* RDS
* Lambda
* ECS
* CloudFront

Advanced FinOps

* Budget Tracking
* Cost Anomaly Detection
* Multi-Cloud Support
* Team Workspaces
* Notification Center
* Optimization Simulator

---

# 16. Definition of Done

CloudWise AI is production-ready when:

✓ Authentication works

✓ AWS connection works

✓ LocalStack connection works

✓ Resource discovery works

✓ Dashboard shows live data

✓ Recommendations generate correctly

✓ Forecasting works

✓ Reports export successfully

✓ AI Copilot responds with infrastructure context

✓ Application deployed on Render + Vercel

✓ No empty dashboard states exist

---

Status: Approved

Version: 2.0
