import json

def main():
    with open('config.json', 'r') as file:
        config = json.load(file)

    query = config["query"]
    wd_config = config["wd_config"]
    wx_config = config["wx_config"]
    prompts = config["prompts"]

    return {
        "api_status": "successful"
    }

if __name__ == '__main__':
    print(json.dumps(main(), indent=4))