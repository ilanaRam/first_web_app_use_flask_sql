
import os.path

import requests
import json

def rest_api_get_retrive_data_by_url_from_github_site():
    # this way we access send REST APIs to the site - for accessing the apis of the site
    # here we use REST API - GET(url) to get resources (all questions that were asked)
    URL = "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow"
    resp = requests.get(URL)
    print(len(resp.json()['items']))

    #here we parse the retrieved data
    for data in resp.json()['items']:
        if data['answer_count'] == 0:
            print(f"The data is: {data['title']}")
            print(data['link'])
            print() # this way we actually print blank line
        else:
            print("Skipped")



if __name__ == '__main__':
    rest_api_get_retrive_data_by_url_from_github_site()


