import requests
import helper

config = helper.read_config()
NOTION_TOKEN = config['TOKENS']['NOTION_TOKEN']
DATABASE_ID = config['TOKENS']['DATABASE_ID']

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Notion-Version": "2022-06-28",
    "Content-type": "application/json"
}

def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    import json
    with open('db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results

pages = get_pages()
names = []
for page in pages:
    page_id = page["id"]
    props = page["properties"]
    url = props["URL"]["url"]
    name_item = props["Name"]["title"][0]["text"]["content"]
    tags_json = props["Tags"]["select"]["name"]

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)
    print(res.status_code)
    return res

url = "Test Url 2"
name_item = "Test food"
tags_json = "завтрак"
data = {
    "URL": {"url": url},
    "Name":{"title":[{"text": {"content": name_item}}]},
    "Tags": {"multi_select": [{"name": tags_json}]}
    }

def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    print(res.status_code)
    return res

def delete_page(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"archived": True}

    res = requests.patch(url, json=payload, headers=headers)
    print(res.status_code)
    return res
