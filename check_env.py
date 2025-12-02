import os

print("=== Checking Turso Configuration ===\n")

turso_url = os.getenv('TURSO_DATABASE_URL')
turso_token = os.getenv('TURSO_AUTH_TOKEN')

print(f"TURSO_DATABASE_URL: {'✅ Set' if turso_url else '❌ Not set'}")
if turso_url:
    print(f"  Value: {turso_url[:50]}...")  # Show first 50 chars

print(f"\nTURSO_AUTH_TOKEN: {'✅ Set' if turso_token else '❌ Not set'}")
if turso_token:
    print(f"  Value: {turso_token[:20]}...")  # Show first 20 chars

if not turso_url or not turso_token:
    print("\n⚠️  WARNING: Turso credentials are not properly configured!")
    print("Please ensure your .env file contains:")
    print("  - TURSO_DATABASE_URL")
    print("  - TURSO_AUTH_TOKEN")
else:
    print("\n✅ Turso credentials are configured!")
