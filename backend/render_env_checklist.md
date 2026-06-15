# Render Environment Variables Checklist

Set these in Render Dashboard → Your Service → Environment before deploying.

## Required (app will not start without these)

| Variable | How to generate |
|---|---|
| DATABASE_URL | Provided automatically by Render PostgreSQL — copy the "Internal Database URL" |
| JWT_SECRET | python -c "import secrets; print(secrets.token_hex(32))" |
| ENCRYPTION_KEY | python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" |

## Required for full functionality

| Variable | Value |
|---|---|
| CORS_ORIGINS | Your Render frontend URL e.g. https://cloudwise-ai.onrender.com |
| GROQ_API_KEY | Get free key at https://console.groq.com |
| GROQ_MODEL | llama-3.3-70b-versatile |
| AWS_REGION | us-east-1 (or your preferred region) |

## Optional (features disabled if not set)

| Variable | Value |
|---|---|
| WOLFRAM_APP_ID | Get free key at products.wolframalpha.com/api |

## Do NOT set on Render (local dev only)

- DEBUG=true (leave unset, defaults to false in production)
- CORS_ORIGINS with localhost values

## Notes

- Never commit .env to git
- Rotate JWT_SECRET and ENCRYPTION_KEY if you suspect compromise
- ENCRYPTION_KEY must be a valid Fernet key (44 characters, base64)
- If ENCRYPTION_KEY changes after users have connected AWS accounts,
  existing stored credentials will fail to decrypt — users must reconnect
