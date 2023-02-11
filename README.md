# Hometap Engineering Manager Exercise API 

The purpose of this API is to serve as the intermediary layer between the web client and the third party House Canary API. 

### Quick Start 

#### Secrets
This API is making authenticated requests to the House Canary API. 

For the purposes of this tutorial, you need to create a local secrets folder at the root
of the repository named <api_key>.txt that contains yous <api_secret>.

In order to do so, run the following commands at the root of the repository:

```
mkdir secrets
echo "my_api_secret" >> secrets/my_api_key.txt
```

Validate that you now have the secrets folder and the secret above is correctly placed inside the folder. 

#### Running the Service

This tutorial expects that you have docker installed locally and have understanding on how to use it. If you don't have docker installed, please follow instructions [here](https://docs.docker.com/engine/install): 

```
docker compose build hometap-api
docker compose up hometap-api
```

#### Making Requests
```
curl http://localhost:5000/api/has_septic_system?address=123+Main+St+Natick+MA+01748
```

Expected response:

```
{"has_septic_system":false}
```
