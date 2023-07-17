import json

# read the config.json file and return it as a dictionary 
def read_config():
    with open('config.json', 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    print(read_config())