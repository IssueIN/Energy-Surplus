import requests

def request(url, params, filename, description):
  try:
    response = requests.get(url, params=params)
    if response.status_code == 200:
      with open(f'{filename}', 'w') as file:
        file.write(response.text)
      print(f"Response data saved for {description}")
    else:
      print(f"Error for {description}: {response.status_code}")
      print(response.text)

  except requests.exceptions.RequestException as e:
    print(f"An error occurred for {description}: {e}")