# Microservices with FastAPI
- This repo is composed of three small microservices to be used with Kong API Gateway on K8s.
- Users, Items and Shops microservices are capable of handling CRUD functionality. 
- Pydantic and SQL Alchemy were used as model providers.
- Sqlite were used as local database for each microservice.

## Running
- To run in local environment for testing purposes:
- docker-compose up --build
- visit => http://localhost:{8001,8002,8003}/docs

## Deploying to Kubernetes with Kong
- I have a series with two stories to deploy on Kubernetes behind a Kong API Gateway.
- Kong will handle authentication & authorization in that scenario with JWT and ACL plugins.
- Part I --> https://medium.com/@emrah-t/kong-api-gateway-with-microservices-part-i-how-to-install-and-config-kong-on-kubernetes-9e196621d757
- Part II --> https://medium.com/@emrah-t/kong-api-gateway-with-microservices-part-ii-handling-authentication-and-authorization-with-kong-4f2471b899b0
