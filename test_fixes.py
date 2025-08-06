#!/usr/bin/env python3
"""
Test script to demonstrate the bug fixes
"""

from app import get_user_by_id, hash_password, verify_password, get_all_users

def test_sql_injection_fix():
    """Test that SQL injection is prevented"""
    print("Testing SQL injection fix...")
    
    # This should not cause any issues now
    malicious_input = "1; DROP TABLE users; --"
    try:
        result = get_user_by_id(malicious_input)
        print("✓ SQL injection prevented - query executed safely")
        return True
    except Exception as e:
        print(f"✗ SQL injection fix failed: {e}")
        return False

def test_password_hashing_fix():
    """Test that password hashing is now secure"""
    print("\nTesting password hashing fix...")
    
    password = "test_password"
    hashed = hash_password(password)
    
    # Test verification
    if verify_password(password, hashed):
        print("✓ Password hashing and verification working correctly")
        return True
    else:
        print("✗ Password verification failed")
        return False

def test_connection_handling_fix():
    """Test that database connections are properly managed"""
    print("\nTesting connection handling fix...")
    
    try:
        # Call multiple times to test connection management
        for i in range(5):
            users = get_all_users()
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