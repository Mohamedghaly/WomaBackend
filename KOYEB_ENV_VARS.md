# Koyeb Environment Variables

Copy these environment variables to your Koyeb deployment:

## Required Environment Variables

### Django Configuration
```
SECRET_KEY=i0m%r$+l&4x9rn4nimx@q5b%_c*7(atd*y968tc2im7dz&-ywv
DEBUG=False
ALLOWED_HOSTS=*
```

### Database Configuration (Turso)
```
TURSO_DATABASE_URL=https://womaclothes-mohamedghaly.aws-ap-northeast-1.turso.io
TURSO_AUTH_TOKEN=eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJleHAiOjE3OTYwMjYzNjMsImlhdCI6MTc2NDQ5MDM2MywiaWQiOiJkNWE3YTQ4NS0wZTFhLTRmZGYtYThlMi1lYzg3YzA5NzU5MTIiLCJyaWQiOiI1ZmY1MTU1NS0zNDI2LTRlMDAtYmFjNy02Yjg3OGQ1NWIxOTcifQ.GcwFibhXQ8VTtiBB9L7S1Thv0gUqGNUV6-o4IIAklc_Q8w80-6sx8jouMUHZeE7T7bkV18P5BqOtRdKCg-uaDg
```

### Python Version
```
PYTHON_VERSION=3.9.0
```

## How to Add These in Koyeb

1. Go to your Koyeb service settings
2. Navigate to "Environment variables"
3. Click "Add variable" for each one
4. Copy the name and value exactly as shown above
5. Click "Deploy" to apply changes

## Security Notes

⚠️ **IMPORTANT**: The SECRET_KEY shown above is generated for you. Keep it secure and never commit it to your repository.

⚠️ **Database Token**: The TURSO_AUTH_TOKEN is already configured. Make sure it's kept secret.

## Optional: Update ALLOWED_HOSTS

Once you know your Koyeb domain, you can update ALLOWED_HOSTS for better security:

```
ALLOWED_HOSTS=woma-backend-YOUR-ORG.koyeb.app,*.koyeb.app
```
