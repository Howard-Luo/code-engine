import requests
import json
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urljoin, urlparse
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from selenium import webdriver
import time

wd_api_key = "xxx"
wd_project_id = "667e04b9-5b94-412b-b31a-02f91d9195fb" 
wd_version = "2023-03-31"

def get_main_content(url):
    def extract_with_hyperlinks(element):
        for a in element.find_all('a', href=True):
            a.replace_with(f"{a.get_text()} ({a['href']})")
        return element.get_text(strip=True)

    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(3)  
    page_source = browser.page_source
    browser.quit()

    soup = BeautifulSoup(page_source, 'html.parser')

    article_title = soup.find('h1', class_='article-title')
    article_content = soup.find('div', class_='article-content')
    main_content = " "

    if article_title and article_content:
        title_text = article_title.get_text(strip=True)
        content_text = extract_with_hyperlinks(article_content)
        main_content = title_text + " " + content_text
        return {
            "main_content" : main_content,
            "title" : title_text,
            "url" : url
        }
    else:
        return {
            "main_content" : "N/a",
            "title" : "N/a",
            "url" : url
        }


def fetch_all_documents(discovery, project_id, collection_id):
    offset = 0
    count = 1
    more_results = True
    while more_results:
        response = discovery.query(
            project_id=project_id,
            collection_ids=[collection_id], 
            query='', 
            count=count,
            offset=offset
        ).get_result()

        results = response['results']
        for result in results:
            yield result
        offset += count
        more_results = offset < response['matching_results']

def upload_document(discovery, project_id, collection_id, document_data):
    filename=document_data["title"]
    response = discovery.add_document(
        project_id=project_id, 
        collection_id=collection_id, 
        file=json.dumps(document_data["main_content"]),
        filename=filename,
        metadata = json.dumps({"url" : document_data["url"]}),
        file_content_type='application/json'
    ).get_result()
    return response


authenticator = IAMAuthenticator(wd_api_key)
discovery = DiscoveryV2(
    version=wd_version,
    authenticator=authenticator
)

discovery.set_service_url('https://api.us-south.discovery.watson.cloud.ibm.com')

collection_id = "8ca001f2-b793-93a3-0000-018d392d35c7"
collection_id_clean = "834db6d6-f15d-a910-0000-018d636cf33c"
count = 1


for result in fetch_all_documents(discovery, wd_project_id, collection_id):
    url = result.get('metadata').get('source').get('url')
    if url: 
        print(url)
        document_id = result.get('document_id')
        document_collection_id = result.get('result_metadata').get("collection_id")
        web_main_content = get_main_content(url)
        print(web_main_content)

        upload_response = upload_document(
            discovery, 
            wd_project_id, 
            collection_id_clean, 
            web_main_content
        )
        print(f'--- Uploaded crawled webpage from #{url} ---')


    else:
        print("WD Error")




    print(f'Uploaded doc #{count}')
    count+=1


