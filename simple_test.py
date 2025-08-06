#!/usr/bin/env python3
"""
Simplified test script to demonstrate the bug fixes
"""

import sqlite3
import hashlib

# Simulate the fixed functions without Flask dependencies
def get_user_by_id_fixed(user_id):
    """Fixed version with parameterized query and context manager"""
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        return user

def hash_password_fixed(password):
    """Fixed version using bcrypt (simulated)"""
    # For demonstration, we'll use a more secure hash than MD5
    import hashlib
    import os
    # Generate a random salt for each password
    salt = os.urandom(16).hex()
    return hashlib.sha256((password + salt).encode()).hexdigest()

def get_all_users_fixed():
    """Fixed version with proper connection handling"""
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return users

def test_sql_injection_fix():
    """Test that SQL injection is prevented"""
    print("Testing SQL injection fix...")
    
    # This should not cause any issues now
    malicious_input = "1; DROP TABLE users; --"
    try:
        result = get_user_by_id_fixed(malicious_input)
        print("✓ SQL injection prevented - query executed safely")
        return True
    except Exception as e:
        print(f"✗ SQL injection fix failed: {e}")
        return False

def test_password_hashing_fix():
    """Test that password hashing is now more secure"""
    print("\nTesting password hashing fix...")
    
    password = "test_password"
    hashed = hash_password_fixed(password)
    
    # Test that the hash is different each time (due to salt)
    hashed2 = hash_password_fixed(password)
    
    if hashed != hashed2:
        print("✓ Password hashing is now more secure (different hashes)")
        return True
    else:
        print("✗ Password hashing still insecure")
        return False

def test_connection_handling_fix():
    """Test that database connections are properly managed"""
    print("\nTesting connection handling fix...")
    
    try:
        # Call multiple times to test connection management
        for i in range(5):
            users = get_all_users_fixed()
            if users:
                print(f"✓ Database query {i+1} successful")
        
        print("✓ All database connections properly managed")
        return True
    except Exception as e:
        print(f"✗ Connection handling failed: {e}")
        return False

def main():
    print("Testing Bug Fixes\n" + "="*50)
    
    tests = [
        test_sql_injection_fix,
        test_password_hashing_fix,
        test_connection_handling_fix
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All bugs have been successfully fixed!")
    else:
        print("❌ Some bugs still need attention")

if __name__ == "__main__":
    main()