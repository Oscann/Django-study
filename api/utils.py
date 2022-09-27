import json


def parsePost(body):
    body = body.split("&")
    for i in range(len(body)):
        body[i] = body[i].split("=")

    print(body)
    result = dict()

    for i in range(len(body)):
        result[body[i][0]] = body[i][1]
        print(result)

    return json.dumps(result)
