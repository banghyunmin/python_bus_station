import requests
import json
import time

url = "https://us1.locationiq.com/v1/search.php"

address_book = []
user_list = []
address_list = []

f = open("./source.txt", 'r')
lines = f.readlines()
f.close()
for index, line in enumerate(lines) :
    if index % 2:
        address_list.append(line[:-1])
    else :
        user_list.append(line[:-1])

# file write start
for index, address in enumerate(address_list) :
    time.sleep(3)
    data = {
        'key': 'pk.b3db7890aed8df517be541bc1faeabb4',
        'q': address,
        'format': 'json'
     }
    response = requests.get(url, params=data)
    res_json = json.loads(response.text)

    # test print
    print(index, address, res_json)

    address_book.append({"user": user_list[index], "lat": res_json[0]["lat"], "lon": res_json[0]["lon"]})

with open("./address.json", 'w') as outfile:
    json.dump(address_book, outfile)
print("finish")
