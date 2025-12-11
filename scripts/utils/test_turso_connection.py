import libsql_client
import os

# Test Turso connection using environment variables
url = os.getenv('TURSO_DATABASE_URL', 'libsql://your-database.turso.io')
token = os.getenv('TURSO_AUTH_TOKEN', 'your-token-here')

print("Testing Turso Database Connection...")
print(f"URL: {url}")
print("")

# Convert to HTTPS as our backend does
https_url = url.replace('libsql://', 'https://')
print(f"Converted URL: {https_url}")
print("")

try:
    print("Creating client...")
    client = libsql_client.create_client_sync(https_url, auth_token=token)
    
    print("Entering client context...")
    client.__enter__()
    
    print("Executing simple query...")
    result = client.execute("SELECT 1 as test")
    
    print("✅ Connection successful!")
    print(f"Result: {result.rows}")
    
    client.__exit__(None, None, None)
    
except Exception as e:
    print(f"❌ Connection failed!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    
    if hasattr(e, '__dict__'):
        print(f"Error details: {e.__dict__}")
    
    import traceback
    traceback.print_exc()
