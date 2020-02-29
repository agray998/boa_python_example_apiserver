# Python Flask Example API
## Setup
The `./hack/deploy.sh` script will be able to deploy this application.

```bash
mkdir -p ~/projects/gitlab.com/qacdevops && cd $_
git clone https://gitlab.com/qacdevops/python-flask-example-api
cd python-flask-example-api
sudo ./hack/deploy.sh
```

## Routes
The API setup is running on port `5000` and has the following routes configured:

| Route | Description |
|--|--|
|`/get/text`|Return a simple text message: *"Hello from Flask"*|
|`/post/text`|Return the data from request back as a part of a string: *"Data you sent: `[DATA_YOU_SENT]`"*|
|`/get/json`|Return a JSON object containing a `data` property with a message: `{"data": "Hello from Flask"}`|
|`/post/json`|Return the data from request back as a `data` property inside of a JSON: `{"data": "[DATA_THAT_WAS_SENT]"}`|

