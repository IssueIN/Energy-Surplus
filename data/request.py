import requests

# Define the base URL for the API
base_url = "https://web-api.tp.entsoe.eu/api"

# Replace with your actual security token
security_token = '1d9cd4bd-f8aa-476c-8cc1-3442dc91506d'

# Define the parameters for your request
params = {
    "securityToken": security_token,
    "documentType": "A65",  # Example: Actual Total Load
    "processType": "A16",   # Example process type
    "outBiddingZone_Domain": "10YCZ-CEPS-----N",  # Example: CZ Bidding Zone
    "periodStart": "201601010000",  # Start period in yyyyMMddHHmm format
    "periodEnd": "201601020000"     # End period in yyyyMMddHHmm format
}

try:
    # Make the GET request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response here
        print("Response received:")
        print(response.text)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    # Handle any errors that occur during the request
    print(f"An error occurred: {e}")
