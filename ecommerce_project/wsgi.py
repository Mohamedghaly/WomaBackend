import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')

application = get_wsgi_application()

# Run migrations on startup to ensure DB is up to date
try:
    print("Running migrations...")
    call_command('migrate')
    print("Migrations completed!")
except Exception as e:
    print(f"Migration failed: {e}")
