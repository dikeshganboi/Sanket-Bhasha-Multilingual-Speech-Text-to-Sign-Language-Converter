#!/usr/bin/env python3
"""
Script to create a superuser account
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A2SL.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    print("=" * 70)
    print("CREATE NEW SUPERUSER ACCOUNT")
    print("=" * 70)
    
    username = input("\nEnter username: ").strip()
    
    if not username:
        print("❌ Username cannot be empty!")
        return
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"\n⚠️  User '{username}' already exists!")
        make_admin = input("Do you want to make this user a superuser? (yes/no): ").strip().lower()
        
        if make_admin in ['yes', 'y']:
            user = User.objects.get(username=username)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"\n✅ User '{username}' is now a SUPERUSER!")
            print(f"   - Staff: {user.is_staff}")
            print(f"   - Superuser: {user.is_superuser}")
            return
        else:
            print("Operation cancelled.")
            return
    
    email = input("Enter email (optional, press Enter to skip): ").strip()
    password = input("Enter password: ").strip()
    
    if not password:
        print("❌ Password cannot be empty!")
        return
    
    password_confirm = input("Confirm password: ").strip()
    
    if password != password_confirm:
        print("❌ Passwords don't match!")
        return
    
    # Create superuser
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email if email else '',
            password=password
        )
        
        print("\n" + "=" * 70)
        print("✅ SUPERUSER CREATED SUCCESSFULLY!")
        print("=" * 70)
        print(f"\n👤 Username: {user.username}")
        print(f"📧 Email: {user.email if user.email else '(not provided)'}")
        print(f"⭐ Superuser: {user.is_superuser}")
        print(f"🔧 Staff: {user.is_staff}")
        print(f"📅 Created: {user.date_joined}")
        print("\n" + "=" * 70)
        print("You can now login with these credentials!")
        print("Access admin panel at: http://localhost:8000/admin/")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error creating superuser: {e}")

if __name__ == "__main__":
    try:
        create_superuser()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
