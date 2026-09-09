# Python Container to AWS

A hands-on learning project: build a Python web application,
package it with Docker, and deploy it to AWS.

## Current progress

- Built and ran a Docker image locally.
- Published the container's port to localhost.
- Inspected running containers and application logs.
- Verified HTTP responses with a browser and curl.
- Added a health endpoint and handling for unknown paths.

AWS deployment is the next stage and is not completed yet.

## Routes

| Path | Response | HTTP status |
|------|----------|-------------|
| `/` | Hello from Zeek's container! | 200 |
| `/health` | OK | 200 |
| Any other path | Not found | 404 |

## Run locally

Requires Docker to be installed and running.
Run these commands from the project folder:

```bash
docker build -t zeek-python-app .
docker run --rm --name zeek-web -p 127.0.0.1:8000:8000 zeek-python-app
```

Open http://localhost:8000 in your browser.

## Inspect and verify

In a second Terminal:

```bash
docker ps
docker logs zeek-web
curl -i http://localhost:8000/health
curl -i http://localhost:8000/missing
```

## Stop the container

```bash
docker stop zeek-web
```

The container is removed automatically because it was started
with `--rm`. The image remains available locally.

## What I learned

An image packages the application and its runtime.
A container runs that image. After changing the source code,
I rebuilt the image and replaced the container to apply the update.

## Scope and attribution

Built as a guided learning project with AI assistance.
Uses Python's built-in HTTP server for demonstration, not
as a production-ready web server.

## Next steps

- Push the image to Amazon ECR.
- Deploy the container using Amazon ECS on Fargate.
- Document deployment, verification, costs, and cleanup. 