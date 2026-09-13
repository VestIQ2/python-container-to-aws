# Docker Troubleshooting Lab

## Objective

This lab documents three controlled Docker failures introduced into a working Python web application. The goal was to practice using container status, logs, port mappings, HTTP responses, and health-check history to identify root causes.

## Working baseline

I first ran the existing image with port 8001 on my Mac mapped to port 8000 inside the container:

```bash
docker run -d \
  --name zeek-lab-baseline \
  -p 127.0.0.1:8001:8000 \
  zeek-python-app:latest
```

I verified the health endpoint:

```bash
curl -i http://localhost:8001/health
```

Observed result:

```text
HTTP/1.0 200 OK
Content-Type: text/plain

OK
```

This established that the image and application worked before any faults were introduced.

## Failure 1: Container exits during startup

### Fault introduced

I overrode the image's normal startup command with a command that referenced a nonexistent Python file:

```bash
docker run -d \
  --name zeek-lab-broken-startup \
  zeek-python-app:latest \
  python missing_app.py
```

### Symptoms

The broken container did not appear in `docker ps`, which only shows running containers. It appeared in `docker ps -a` with:

```text
Exited (2)
```

### Investigation

I inspected the container logs:

```bash
docker logs zeek-lab-broken-startup
```

The relevant error was:

```text
python: can't open file '/app/missing_app.py':
[Errno 2] No such file or directory
```

### Root cause

The container's main process tried to run a file that did not exist. When the Python process exited, the container stopped.

### Fix

I removed the stopped container and recreated it using the correct filename:

```bash
docker rm zeek-lab-broken-startup
```

```bash
docker run -d \
  --name zeek-lab-broken-startup \
  zeek-python-app:latest \
  python app.py
```

The corrected container appeared in `docker ps` with a status beginning with `Up`.

### Lesson

A container remains running only while its main process remains running. Container logs are an important first check when a container exits unexpectedly.

## Failure 2: Application runs but cannot be reached

### Fault introduced

I ran the corrected container without publishing its application port to the Mac.

### Symptoms

The container remained running, but this request failed:

```bash
curl -i http://localhost:8002/health
```

The error was:

```text
curl: (7) Failed to connect to localhost port 8002
```

The following command returned no port mapping:

```bash
docker port zeek-lab-broken-startup
```

### Root cause

The application listened on port 8000 inside the container, but there was no host-to-container port mapping. `EXPOSE 8000` documents the container port but does not publish it to the host.

### Fix

I recreated the container with an explicit port mapping:

```bash
docker run -d \
  --name zeek-lab-fixed \
  -p 127.0.0.1:8002:8000 \
  zeek-python-app:latest
```

Docker then reported:

```text
8000/tcp -> 127.0.0.1:8002
```

The same curl request returned HTTP 200 and `OK`.

### Lesson

A running process does not guarantee network access. The application's listening port, container port, and published host port must connect correctly.

## Failure 3: Working application marked unhealthy

### Fault introduced

I added a Docker health check that requested `/missing`, a route that intentionally returns HTTP 404:

```dockerfile
HEALTHCHECK --interval=5s --timeout=3s --retries=2 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/missing')"
```

I built and ran the image:

```bash
docker build -t zeek-python-app:broken-health .
```

```bash
docker run -d \
  --name zeek-lab-broken-health \
  -p 127.0.0.1:8003:8000 \
  zeek-python-app:broken-health
```

### Symptoms

The real health endpoint still returned HTTP 200:

```bash
curl -i http://localhost:8003/health
```

However, Docker reported:

```text
Container=running Health=unhealthy
```

This proved that the application process was running while Docker's separate health check was failing.

### Investigation

I inspected Docker's health-check history:

```bash
docker inspect \
  --format='{{range .State.Health.Log}}ExitCode={{.ExitCode}} Output={{printf "%q" .Output}}{{println}}{{end}}' \
  zeek-lab-broken-health
```

The recorded attempts showed:

```text
ExitCode=1
urllib.error.HTTPError: HTTP Error 404: Not Found
```

### Root cause

Docker repeatedly checked `/missing`. The application correctly returned HTTP 404 for that route, causing the health-check command to exit with code 1. After repeated failures, Docker marked the container unhealthy.

### Fix

I changed the Dockerfile health-check path from `/missing` to `/health`:

```dockerfile
HEALTHCHECK --interval=5s --timeout=3s --retries=2 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

I rebuilt and ran the corrected image:

```bash
docker build -t zeek-python-app:healthy .
```

```bash
docker run -d \
  --name zeek-lab-healthy \
  -p 127.0.0.1:8003:8000 \
  zeek-python-app:healthy
```

The final verification command was:

```bash
docker inspect \
  --format='Container={{.State.Status}} Health={{.State.Health.Status}}' \
  zeek-lab-healthy
```

Observed corrected result:

```text
Container=running Health=healthy
```

### Lesson

Container status and health status measure different conditions. A container can keep running while an incorrectly configured health check reports it as unhealthy.

## Troubleshooting method

I used the same process for each failure:

1. Establish a working baseline.
2. Observe the container's status.
3. Identify whether the failure involves the process, network, or health check.
4. Inspect logs, port mappings, HTTP responses, or health-check history.
5. Correct one suspected cause.
6. Repeat the original test to verify the fix.

## Scope and attribution

These were controlled troubleshooting exercises performed with AI guidance. I ran the commands, reviewed the evidence, identified the failure types, and applied the corrections.