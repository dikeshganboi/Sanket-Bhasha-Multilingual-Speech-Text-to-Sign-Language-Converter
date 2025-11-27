#!/usr/bin/env python3
"""
Script to show all tables in db.sqlite3 and their row counts
"""
import sqlite3
import os

db_path = 'db.sqlite3'

if not os.path.exists(db_path):
    print(f"❌ Database file '{db_path}' not found!")
    exit(1)

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()

print("=" * 70)
print("DATABASE TABLES IN db.sqlite3")
print("=" * 70)

if not tables:
    print("No tables found in database.")
else:
    print(f"\nTotal tables: {len(tables)}\n")
    
    for table in tables:
        table_name = table[0]
        
        # Get row count for each table
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        
        # Get column info
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        print(f"📋 Table: {table_name}")
        print(f"   Rows: {count}")
        print(f"   Columns: {', '.join([col[1] for col in columns])}")
        print()

# Show sample data from auth_user if it exists
print("=" * 70)
print("USER ACCOUNTS (auth_user)")
print("=" * 70)

try:
    cursor.execute("SELECT id, username, email, is_staff, is_superuser, date_joined FROM auth_user;")
    users = cursor.fetchall()
    
    if users:
        print(f"\nTotal users: {len(users)}\n")
        for user in users:
            print(f"  ID: {user[0]}")
            print(f"  Username: {user[1]}")
            print(f"  Email: {user[2]}")
            print(f"  Staff: {user[3]}, Superuser: {user[4]}")
            print(f"  Joined: {user[5]}")
            print()
    else:
        print("\nNo users found in database.")
        print("Create a user by visiting: http://localhost:8000/signup/")
except sqlite3.OperationalError:
    print("\n⚠️  auth_user table not found. Run migrations first.")

conn.close()

print("=" * 70)
print("✅ Database inspection complete!")
print("=" * 70)
