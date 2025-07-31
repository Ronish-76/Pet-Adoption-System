import requests

base_url = "http://127.0.0.1:8000"

endpoints = [
    "/api/pets/",
    "/api/pets/featured/",
    "/api/pets/statistics/",
    "/api/accounts/register/",
    "/api/accounts/login/",
    "/api/adoptions/",
    "/swagger/",
    "/redoc/",
    "/docs/"
]

print("Testing API endpoints:")
print("-" * 50)

for endpoint in endpoints:
    try:
        response = requests.get(base_url + endpoint, timeout=5)
        status = response.status_code
        if status == 200:
            print(f"✅ {endpoint} - OK ({status})")
        elif status == 403:
            print(f"🔒 {endpoint} - Forbidden ({status})")
        elif status == 404:
            print(f"❌ {endpoint} - Not Found ({status})")
        elif status == 500:
            print(f"💥 {endpoint} - Server Error ({status})")
        else:
            print(f"⚠️  {endpoint} - Status {status}")
    except Exception as e:
        print(f"❌ {endpoint} - Error: {str(e)}")

print("-" * 50)
print("Test complete!")