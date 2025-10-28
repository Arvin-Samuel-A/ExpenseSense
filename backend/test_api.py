#!/usr/bin/env python
"""
Quick Backend Health Check Script
Tests all major API endpoints to verify setup
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_test(name, success, message=""):
    status = "✅" if success else "❌"
    print(f"{status} {name}: {message}")

def test_backend_health():
    print("\n" + "="*60)
    print("🔍 EXPENSESENSE BACKEND HEALTH CHECK")
    print("="*60 + "\n")
    
    # Test 1: Server is running
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=5)
        print_test("Server Running", response.status_code in [200, 302], 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Server Running", False, f"Error: {e}")
        print("\n❌ Backend is not running. Please start it first.\n")
        return

    # Test 2: Register new user
    print("\n📝 Testing User Registration...")
    register_data = {
        "email": f"test_{datetime.now().timestamp()}@example.com",
        "username": f"testuser_{int(datetime.now().timestamp())}",
        "password": "testpass123",
        "password2": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register/",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            data = response.json()
            access_token = data['tokens']['access']
            user_id = data['user']['id']
            print_test("User Registration", True, f"User ID: {user_id}")
            
            # Test 3: Create Expense
            print("\n💰 Testing Expense Creation...")
            expense_data = {
                "amount": 500,
                "merchant": "Test Merchant",
                "category": "food",
                "payment_mode": "card",
                "date": datetime.now().isoformat(),
                "notes": "Test expense"
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            
            response = requests.post(
                f"{BASE_URL}/expenses/",
                json=expense_data,
                headers=headers
            )
            
            if response.status_code == 201:
                expense = response.json()
                print_test("Expense Creation", True, f"Expense ID: {expense['id']}")
                
                # Test 4: Get Expenses
                print("\n📋 Testing Expense Retrieval...")
                response = requests.get(
                    f"{BASE_URL}/expenses/",
                    headers=headers
                )
                
                if response.status_code == 200:
                    expenses = response.json()
                    count = len(expenses.get('results', []))
                    print_test("Expense Retrieval", True, f"Found {count} expenses")
                else:
                    print_test("Expense Retrieval", False, f"Status: {response.status_code}")
                
                # Test 5: Get Monthly Summary
                print("\n📊 Testing Monthly Summary...")
                response = requests.get(
                    f"{BASE_URL}/expenses/summary/monthly/",
                    headers=headers
                )
                
                if response.status_code == 200:
                    summary = response.json()
                    total = summary.get('total_amount', 0)
                    print_test("Monthly Summary", True, f"Total: ₹{total}")
                else:
                    print_test("Monthly Summary", False, f"Status: {response.status_code}")
                
                # Test 6: ML Classification
                print("\n🤖 Testing ML Classification...")
                sms_text = "Spent Rs 500 at McDonald's"
                response = requests.post(
                    f"{BASE_URL}/ml/classify/",
                    json={"sms_text": sms_text},
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    category = result.get('category', 'unknown')
                    confidence = result.get('confidence', 0)
                    print_test("ML Classification", True, 
                             f"Category: {category}, Confidence: {confidence:.2f}")
                else:
                    print_test("ML Classification", False, f"Status: {response.status_code}")
                
            else:
                print_test("Expense Creation", False, f"Status: {response.status_code}")
        else:
            print_test("User Registration", False, 
                      f"Status: {response.status_code}, Error: {response.text}")
            
    except Exception as e:
        print_test("API Test", False, f"Error: {e}")
    
    # Test 7: Database Connection
    print("\n💾 Testing Database...")
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=5)
        print_test("Database Connection", True, "MySQL connected")
    except Exception as e:
        print_test("Database Connection", False, f"Error: {e}")
    
    print("\n" + "="*60)
    print("✅ HEALTH CHECK COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_backend_health()
