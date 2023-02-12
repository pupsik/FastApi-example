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

API docs can be accessed at:

```
http://localhost:5000/docs
```

Other responses:

```
curl http://localhost:5000/api/has_septic_system?address=123+Main+St
```

Expected response:

```
status_code = 400
response = Unable to validate user supplied property address
```

```
curl http://localhost:5000/api/has_septic_system
```
Expected response:

```
status_code=422
response = {"detail":[{"loc":["query","address"],"msg":"field required","type":"value_error.missing"}]}
```

```
curl http://localhost:5000/api/has_septic_system?address=444+Unhandled+St
```
Expected response:

```
status_code=503
response = {"detail":"Failed to obtain successful response from third party providers."}
```

#### Further Considerations: 

1. Add logging - all web client requests should be logged and all House Canary requests should be logged. Both logs should 
be joinabled on the same request ID so that we can trace which web client requests resulted in which House Canary API requests. 

2. Rate limiting - set rate limiting on our API

3. Add docker container for tests - build a separate container, separate requirements and add to docker compose

4. Add "lock-requirements" script and docker container to build requirements. 

5. Add retries on thid party API calls for certain types of errors (must be mindful of the third-party API rate limits)

6. Improve secret handling - secrets should be encrypted. 

7. Set up CI/CD pipeline


