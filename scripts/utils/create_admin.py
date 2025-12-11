import os
import sys
import django

# Add the project directory to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_admin():
    User = get_user_model()
    email = 'admin@woma.com'
    password = 'admin123'
    username = 'admin'
    first_name = 'Admin'
    last_name = 'Woma'

    try:
        if not User.objects.filter(email=email).exists():
            print(f"Creating superuser {email}...")
            user = User.objects.create_superuser(
                email=email,
                password=password,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            # Ensure the role is set to admin
            user.role = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print("✅ Superuser created successfully.")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            print(f"   Role: {user.role}")
        else:
            print(f"User {email} already exists. Updating password and ensuring admin role...")
            user = User.objects.get(email=email)
            user.set_password(password)
            user.role = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            print("✅ Admin user updated successfully.")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            print(f"   Role: {user.role}")
    except Exception as e:
        print(f"❌ Error creating/updating admin user: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_admin()
