# Security Policy

# CloudWise AI

Version: 3.0

Last Updated: June 2026

---

# Overview

CloudWise AI is a FinOps SaaS platform designed to analyze cloud infrastructure, identify optimization opportunities, forecast cloud spending, and provide actionable recommendations.

Security is treated as a foundational requirement throughout the application lifecycle.

This document defines the security architecture, authentication model, cloud access controls, infrastructure protections, and operational safeguards implemented within CloudWise AI.

---

# Security Principles

CloudWise AI follows the following principles:

* Least Privilege
* Defense In Depth
* Secure By Default
* Zero Trust
* Data Minimization
* Auditability
* Transparency
* Privacy By Design

---

# Security Objectives

CloudWise AI is designed to:

* Protect user accounts
* Protect cloud account metadata
* Prevent unauthorized access
* Secure API communications
* Protect application secrets
* Ensure infrastructure visibility without modification
* Maintain compliance-ready audit trails

---

# Authentication Security

## Authentication Model

Current MVP Authentication:

Email + Password

↓

Argon2 Password Hashing

↓

JWT Authentication

↓

HTTP-Only Secure Cookies

---

## Password Storage

CloudWise AI never stores plaintext passwords.

Supported Hashing Algorithms:

* Argon2 (Primary)
* Bcrypt (Fallback)

Database Storage:

password_hash

Passwords are hashed before persistence.

---

## Forgot Password Flow

Implemented Features:

* Forgot Password
* Password Reset Tokens
* Expiring Reset Links

Security Controls:

* Single-use reset tokens
* Expiration enforcement
* Token invalidation after use

---

# Session Security

## JWT Authentication

JWT Tokens contain:

* User ID
* Organization ID
* Expiration Time

Tokens never contain:

* Passwords
* AWS Credentials
* API Keys
* Secrets

---

## Cookie Security

Authentication cookies use:

* HTTPOnly
* Secure
* SameSite Protection

Benefits:

* XSS mitigation
* Session theft reduction
* Browser isolation

---

# Transport Security

## HTTPS Enforcement

All production traffic must use HTTPS.

Protected Components:

* Frontend
* Backend APIs
* Authentication Endpoints
* Cloud Connections
* AI Services

Deployment Platforms:

* Vercel
* Render

HTTP traffic is redirected to HTTPS.

---

# Cloud Account Security

## Supported Connection Modes

CloudWise AI supports:

### AWS Mode

Uses:

* Access Key
* Secret Access Key
* STS Validation

Credentials are validated immediately and never exposed in logs.

---

### LocalStack Mode

Used for:

* Development
* Testing
* Demonstrations

Endpoint:

http://localhost:4566

LocalStack credentials are isolated from production environments.

---

# AWS Security Model

## Current MVP

CloudWise AI supports AWS credential authentication.

Recommended Permissions:

* Read-Only Access
* Cost Explorer Access
* CloudWatch Read Access
* EC2 Describe Access
* EBS Describe Access

---

## Future Production Model

Preferred Architecture:

Customer AWS Account

↓

Cross Account IAM Role

↓

CloudWise AI

Benefits:

* No long-term credential storage
* Reduced attack surface
* Improved enterprise compliance

---

# Resource Access Scope

Current Resource Discovery:

* EC2
* EBS

Future Discovery:

* S3
* RDS
* Lambda
* ECS
* CloudFront

CloudWise AI never modifies infrastructure resources automatically.

---

# Secret Management

## Environment Variables

Secrets must be stored in environment variables.

Examples:

DATABASE_URL

JWT_SECRET

OPENAI_API_KEY

AWS_REGION

LOCALSTACK_URL

---

## Prohibited Practices

Never commit:

.env

.env.local

.env.production

credentials.json

secrets.json

AWS credential files

---

# Database Security

## Database Platform

Production:

Render PostgreSQL

Development:

SQLite

---

## Access Controls

Database access is restricted to backend services.

Requirements:

* SSL Connections
* Strong Credentials
* Environment Variable Configuration
* Restricted Network Access

---

# Data Protection

## Sensitive Data

Protected Data Includes:

* User Information
* Cloud Metadata
* Forecast Data
* Recommendations
* Reports

---

## Never Stored

CloudWise AI must never store:

* Plaintext Passwords
* JWT Secrets
* API Provider Secrets
* LocalStack Tokens
* Session Secrets

---

# API Security

## Input Validation

All requests must use Pydantic validation.

Validation Areas:

* Authentication
* Cloud Connections
* Reports
* Copilot Requests

---

## Rate Limiting

Recommended Limits:

Login

5 requests/minute

Register

5 requests/minute

Forgot Password

3 requests/minute

AI Copilot

30 requests/minute

Suggested Library:

slowapi

---

## CORS Policy

Production Origins:

https://cloudwise.ai

https://app.cloudwise.ai

Wildcard origins are prohibited in production.

---

# Security Headers

Required Headers:

* Strict-Transport-Security
* X-Frame-Options
* X-Content-Type-Options
* Referrer-Policy
* Content-Security-Policy

Purpose:

* XSS Protection
* Clickjacking Prevention
* MIME Protection
* HTTPS Enforcement

---

# Audit Logging

## Logged Events

Authentication:

* Registration
* Login
* Logout
* Password Reset

Cloud Events:

* AWS Connection
* LocalStack Connection
* Resource Scan Start
* Resource Scan Complete

Platform Events:

* Report Generation
* Recommendation Creation
* Forecast Generation

---

# AI Security

## Prompt Protection

CloudWise AI never sends:

* Passwords
* AWS Credentials
* Access Keys
* Secret Keys
* JWT Secrets
* Environment Variables

to AI providers.

---

## Allowed Context

AI Providers may receive:

* Resource Metadata
* Cost Data
* Forecast Data
* Recommendation Data
* Health Scores

Only analytical information is transmitted.

---

# Dependency Security

Recommended Tools:

* pip-audit
* Safety
* GitHub Dependabot

Dependency scanning should run continuously.

---

# Backup & Recovery

## Database Backups

Production PostgreSQL should support:

* Daily Backups
* Point-In-Time Recovery
* Backup Retention Policies

---

## Disaster Recovery

Recovery Goals:

* Minimal downtime
* Database restoration capability
* Service continuity

---

# OWASP Security Controls

CloudWise AI follows controls aligned with:

OWASP Top 10

Protection Areas:

* Broken Access Control
* Cryptographic Failures
* Injection Attacks
* Security Misconfiguration
* Authentication Failures
* Vulnerable Components

---

# Future Security Roadmap

Planned Enhancements:

* Google OAuth
* GitHub OAuth
* Microsoft OAuth
* MFA
* SSO
* RBAC
* Security Monitoring
* Secret Rotation
* Compliance Reporting
* SOC 2 Readiness

---

# Security Commitment

CloudWise AI is committed to protecting customer data, enforcing least-privilege access, maintaining secure cloud integrations, and continuously improving platform security through industry-standard best practices.

Status: Approved

Version: 3.0