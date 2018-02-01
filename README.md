# pm01 :: Postmates Take Home Coding Test 01

Geocoding Proxy Service


# API

| method | URL                                 | description                                           |
| ------ | ----------------------------------- | ----------------------------------------------------- |
| GET    | /location/geocode?address={address} | Return the latitude & longitude for the given address |

## Example Usage

Locally, when starting Flask in debug/development mode:

```bash
curl -v -G http://127.0.0.1:5000/location/geocode \
	--data-urlencode 'address=425 Market St #8, San Francisco, CA 94105'
```

... or using [this link](http://127.0.0.1:5000/location/geocode?address=425%20Market%20St%20%238%2C%20San%20Francisco%2C%20CA%2094105).

# Local Development

Install dependencies:

```bash
# switch to any virtual Python environment you like, if any, and then:
pip install -r requirements.txt
```

Run tests:

```bash
make test
```

Start Flask using the CLI in debug mode:

```bash
./dev_server.sh
```

# Deploying & Running with Kubernetes

If you have minikube configured, you can build the Docker image and deploy in
one step, which will give the locally accessible endpoint when done:

```bash
make
# ... or:
make minikube
```

Example endpoint output (*use your own value, not this or localhost*):

```
SERVICE ENDPOINT:
http://192.168.64.3:30164
```

This will set the variable `SETTINGS` to "production" and will enable live
queries.

**NOTE:** You will need to specify your API keys as Kubernetes secrets. There
is a `secrets.yaml` template for this purpose. This file should not be checked
in.

Secrets must be encoded in base64. For example:

```bash
echo -n "1f2d1e2e67df" | base64
```
