import requests


def select(query: dict, index: str = "cocos", host: str = "localhost", port: int = 9308):
    with requests.Session() as session:
        with session.post(url=f"http://{host}:{port}/search", json={
            "index": index, "query": query
        }, headers={"Content-Type": "application/json"}) as resp:
            if resp.status_code != 200:
                raise RuntimeError("Error while inserting doc: manticore is not available")

            return resp.json()


def insert(document: dict, index: str = "cocos", host: str = "localhost", port: int = 9308):
    with requests.Session() as session:
        with session.post(url=f"http://{host}:{port}/insert", json={"index": index, "doc": document}, headers={"Content-Type": "application/json"}) as resp:
            if resp.status_code != 200:
                raise RuntimeError("Error while inserting doc: manticore is not available")

            return resp.json()
        

def write_to_file(doc):
    data = select(
        query={
            "match": {
                "title": doc["title"]
            }
        }
    )
    with open("storage/write.txt", "a", encoding="utf-8") as file:
        for i in data['hits']['hits'][0]['_source'].values():
            file.write(f"{i}\n")

