import http.client, json, nltk, yaml
from nltk.draw.tree import draw_trees


f = open('cbot_hidden.conf', 'r')
config = yaml.safe_load(f)
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': config["MICROSOFT_LINGUISTIC_TOKEN"],
}
f.close()


# Returns a POS tagged & tokenised version of the message input
def getPOS(message):
    body = {
        "language" : "en",
        "analyzerIds" : ["22a6b758-420f-4745-8a3c-46835a67c0d2"],
        "text" : message
    };

    try:
        conn = http.client.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/linguistics/v1.0/analyze", json.dumps(body), headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        conn.close()
        ct = nltk.tree.Tree.fromstring(data[0]['result'][0])
        pos = nltk.tree.Tree.pos(ct)
        return pos;
    except Exception as e: #Error occurred
        print(e)
        return False;

