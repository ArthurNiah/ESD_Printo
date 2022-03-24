# test_invoke_http.py
from invokes import invoke_http

# invoke book microservice to get all books
results = invoke_http("http://localhost:5000/provider", method='GET')

print( type(results) )
print()
print( results )

# invoke provider microservice to create a provider
provider_id = '4'
provider_details = { "username": "sabbie", "tele_id": "@sabbie", "coordinates": 540, "location_name": "marine" }
create_results = invoke_http(
        "http://localhost:5000/provider/" + provider_id, method='POST', 
        json=provider_details
    )

print()
print( create_results )
