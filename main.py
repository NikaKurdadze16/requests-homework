import requests
import json
import concurrent.futures

urls = []

for i in range(100):
    urls.append(f'https://dummyjson.com/products/{i+1}')


def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return url, response.text
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return url, None
    
results_dict = {}
result_list = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    future_to_url = {executor.submit(fetch_data, url): url for url in urls}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            url, data = future.result()
            if data is not None:
                result_line = {url: data}
                result_list.append(data)
        except Exception as e:
            print(f"Error processing data from {url}: {e}")


with open('data.json', 'w') as json_file:
    for result_line in result_list:
        json_file.write(json.dumps(result_line) + '\n')