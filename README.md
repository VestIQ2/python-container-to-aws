# Python Container to AWS

A hands-on learning project: build a Python web application,
package it with Docker, and deploy it to AWS.

## Current progress

- Built and ran a Docker image locally.
- Published the container's port to localhost.
- Inspected running containers and application logs.
- Verified HTTP responses with a browser and curl.
- Added a health endpoint and handling for unknown paths.

Successfully deployed to Amazon ECS on AWS Fargate, verified all
application routes, and confirmed application logs in CloudWatch.
The demo task was stopped after testing to control costs.

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
## Troubleshooting lab

I deliberately introduced startup, port-mapping, and health-check
failures into the container. I used Docker status, logs, port
inspection, HTTP responses, and health history to diagnose and fix
each problem.

[Read the troubleshooting walkthrough](TROUBLESHOOTING.md)

## Scope and attribution

Built as a guided learning project with AI assistance.
Uses Python's built-in HTTP server for demonstration, not
as a production-ready web server.

## AWS deployment completed

- Pushed the Docker image to a private Amazon ECR repository.
- Created an Amazon ECS cluster.
- Configured an IAM task execution role for image pulls and logging.
- Deployed one ARM64 Fargate task with 0.25 vCPU and 512 MiB of memory.
- Used a public subnet and restricted inbound TCP port 8000 to my public IP.
- Sent application logs to CloudWatch with a seven-day retention period.
- Verified `/` and `/health` returned HTTP 200.
- Verified `/missing` returned HTTP 404.
- Stopped the task after testing and confirmed its status was STOPPED.

## Deployment status

This is a completed learning deployment, currently stopped.
The application is not continuously hosted.

The ECR image and CloudWatch logs remain stored and may incur
small storage charges.

## What I learned on AWS

ECR stores container images. ECS manages tasks, and Fargate provides
the compute to run them. The task definition specifies the image,
CPU, memory, architecture, execution role, and logging configuration.

Security groups control network access. CloudWatch logs helped me
verify that the deployed application handled requests correctly.