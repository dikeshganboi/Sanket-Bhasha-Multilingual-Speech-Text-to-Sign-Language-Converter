#!/usr/bin/env python3
"""Quick script to show user data"""
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

cursor.execute('''
    SELECT id, username, email, is_staff, is_superuser, date_joined 
    FROM auth_user 
    ORDER BY id
''')

users = cursor.fetchall()

print("=" * 100)
print(" " * 35 + "USER DATABASE")
print("=" * 100)
print(f"\n📊 Total Users: {len(users)}\n")
print("-" * 100)
print(f"{'ID':<4} {'Username':<18} {'Email':<30} {'Staff':<7} {'Admin':<7} {'Joined':<12}")
print("-" * 100)

for user in users:
    user_id, username, email, is_staff, is_superuser, date_joined = user
    staff_icon = "✅" if is_staff else "❌"
    admin_icon = "⭐" if is_superuser else "❌"
    email_display = email if email else "(none)"
    date_display = date_joined[:10]
    
    print(f"{user_id:<4} {username:<18} {email_display:<30} {staff_icon:<7} {admin_icon:<7} {date_display:<12}")

print("-" * 100)
print(f"\n🔑 Admins: {sum(1 for u in users if u[4])}")
print(f"👥 Regular users: {sum(1 for u in users if not u[4])}")
print("=" * 100)

conn.close()
