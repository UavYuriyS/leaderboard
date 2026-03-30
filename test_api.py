"""
Simple script to test the leaderboard API
Run this after starting the server with: uvicorn main:app --reload
"""
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8888"
API_KEY = os.getenv("API_KEY", "your-secret-api-key-change-this")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "your-admin-api-key-change-this")

# Headers with API key
HEADERS = {
    "X-API-Key": API_KEY
}

# Headers with Admin API key
ADMIN_HEADERS = {
    "X-Admin-API-Key": ADMIN_API_KEY
}


def test_version():
    """Test the version endpoint (no auth required)"""
    print("\n=== Testing GET /version (No Auth) ===")
    response = requests.get(f"{BASE_URL}/version")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_add_user(uid, name):
    """Test adding a user"""
    print(f"\n=== Testing POST /user (uid: {uid}, name: {name}) ===")
    response = requests.post(
        f"{BASE_URL}/user",
        json={"uid": uid, "name": name},
        headers=HEADERS
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_login(uid, name):
    """Test login with uid and username"""
    print(f"\n=== Testing POST /login (uid: {uid}, name: {name}) ===")
    response = requests.post(
        f"{BASE_URL}/login",
        json={"uid": uid, "name": name}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_update_score(name, score):
    """Test updating a user's score"""
    print(f"\n=== Testing PUT /user/score (name: {name}, score: {score}) ===")
    response = requests.put(
        f"{BASE_URL}/user/score",
        json={"name": name, "score": score},
        headers=HEADERS
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_list_leaderboard():
    """Test listing the leaderboard"""
    print("\n=== Testing GET /leaderboard ===")
    response = requests.get(f"{BASE_URL}/leaderboard", headers=HEADERS)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_unauthorized():
    """Test accessing protected endpoint without API key"""
    print("\n=== Testing GET /leaderboard (No API Key) ===")
    response = requests.get(f"{BASE_URL}/leaderboard")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_invalid_key():
    """Test accessing protected endpoint with invalid API key"""
    print("\n=== Testing GET /leaderboard (Invalid API Key) ===")
    response = requests.get(
        f"{BASE_URL}/leaderboard",
        headers={"X-API-Key": "invalid-key"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_delete_user(name):
    """Test deleting a user (admin only)"""
    print(f"\n=== Testing DELETE /user/{name} (Admin API Key) ===")
    response = requests.delete(
        f"{BASE_URL}/user/{name}",
        headers=ADMIN_HEADERS
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_delete_user_wrong_key(name):
    """Test deleting with regular API key (should fail)"""
    print(f"\n=== Testing DELETE /user/{name} (Regular API Key - Should Fail) ===")
    response = requests.delete(
        f"{BASE_URL}/user/{name}",
        headers=HEADERS
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    print("Starting Leaderboard API Tests...")
    print(f"Base URL: {BASE_URL}")
    print(f"API Key: {API_KEY[:10]}... (truncated)")
    print(f"Admin API Key: {ADMIN_API_KEY[:10]}... (truncated)")

    # Test 0: Authentication tests
    test_unauthorized()
    test_invalid_key()

    # Test 1: Get version (no auth required)
    test_version()

    # Test 2: Add users (with auth)
    test_add_user("u-1001", "Alice")
    test_add_user("u-1002", "Bob")
    test_add_user("u-1003", "Charlie")
    test_add_user("u-1004", "David")  # Extra user to delete

    # Test 3: Update scores (with auth)
    test_update_score("Alice", 100)
    test_update_score("Bob", 250)
    test_update_score("Charlie", 175)
    test_update_score("David", 50)

    # Test 5: List leaderboard (should be sorted by score)
    test_list_leaderboard()

    # Test 6: Update Alice's score to be highest
    test_update_score("Alice", 300)

    # Test 7: List leaderboard again
    test_list_leaderboard()

    # Test 8: Try to delete with regular API key (should fail)
    test_delete_user_wrong_key("David")

    # Test 9: Delete user with admin key (should succeed)
    test_delete_user("David")

    # Test 10: List leaderboard (David should be gone)
    test_list_leaderboard()

    # Test 11: Try to delete non-existent user
    test_delete_user("NonExistent")

    print("\n✅ All tests completed!")
