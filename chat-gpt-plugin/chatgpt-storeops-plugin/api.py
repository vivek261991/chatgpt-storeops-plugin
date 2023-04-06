import json

import quart
import quart_cors
from quart import request

# Note: Setting CORS to allow chat.openapi.com is required for ChatGPT to access your plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

StoreDB = {
    "1": [
        {
            "storeManager": "Eve" ,
            "storeNumber": 1, 
            "noOfPackers": 50, 
            "noOfShippers": 50,
            "lastUpdatedTimeStamp": "",
            "state": "AR"
        }
    ],
    "100": [
        {
            "storeManager": "Adam" ,
            "storeNumber": 100, 
            "noOfPackers": 50, 
            "noOfShippers": 50, 
            "lastUpdatedTimeStamp": "",
            "state": "AR"
        }
    ],
}

@app.get("/store/<string:storeNumber>")
async def get_todos(storeNumber):
    return quart.Response(response=json.dumps(StoreDB.get(storeNumber, [])), status=200)


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("ai-plugin.json") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the manifest
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the OpenAPI spec
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5002)


if __name__ == "__main__":
    main()