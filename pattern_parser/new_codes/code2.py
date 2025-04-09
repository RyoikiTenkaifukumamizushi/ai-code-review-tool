def fetch_data(api_url, retries):
    import requests
    for i in range(retries):
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Retrying due to error: {e}")
    return None
