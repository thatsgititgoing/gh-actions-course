# Docker Action: Ping URL

A Docker-based GitHub Action that health-checks a URL with configurable retry logic, waiting until it returns HTTP 200 or maximum attempts are exceeded.

## Type

**Docker Action** - Containerized action running Python in an isolated environment.

## Purpose

This action is designed for deployment verification workflows:
1. Ping a deployed application URL repeatedly
2. Wait for the application to become available (with delays)
3. Verify HTTP 200 response
4. Fail the workflow if maximum retries are exceeded

**Use cases**:
- Health checks after deployment
- Wait for application startup
- Verify service availability
- Integration test prerequisites

## Location

`.github/actions/docker-ping-url/`

## Usage

### Basic Example

```yaml
steps:
  - name: Deploy Application
    run: ./deploy.sh

  - name: Health Check
    uses: ./.github/actions/docker-ping-url
    with:
      url: https://my-app.example.com
```

### Full Example with All Options

```yaml
steps:
  - name: Deploy to Staging
    run: kubectl apply -f deployment.yaml

  - name: Wait for Application
    id: health-check
    uses: ./.github/actions/docker-ping-url
    with:
      url: https://staging.example.com/health
      max_trails: 20              # Try up to 20 times
      delay: 10                   # Wait 10 seconds between attempts

  - name: Run Integration Tests
    if: steps.health-check.outputs.url-reachable == 'true'
    run: npm run test:integration
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `url` | URL to ping (must return HTTP 200) | Yes | - |
| `max_trails` | Maximum number of retry attempts | No | `10` |
| `delay` | Delay in seconds between attempts | No | `5` |

### Input Details

#### `url`
- **Type**: String
- **Required**: Yes
- **Examples**:
  - `https://example.com`
  - `https://api.example.com/health`
  - `http://localhost:8080/status`
- **Expected Response**: HTTP 200 (any other status is treated as failure)

#### `max_trails`
- **Type**: String (number)
- **Default**: `10`
- **Purpose**: How many times to attempt the request before failing
- **Total wait time**: `max_trails × delay` seconds
- **Examples**:
  - `5` - Try 5 times
  - `20` - Try 20 times
  - `1` - Single attempt (no retries)

#### `delay`
- **Type**: String (number)
- **Default**: `5` seconds
- **Purpose**: How long to wait between retry attempts
- **Examples**:
  - `3` - 3 seconds between attempts
  - `10` - 10 seconds between attempts
  - `30` - 30 seconds between attempts

## Outputs

| Output | Description | Type |
|--------|-------------|------|
| `url-reachable` | Whether the URL returned HTTP 200 | Boolean String |

### Output Details

#### `url-reachable`
- **Values**:
  - `'true'` - URL returned HTTP 200 within max attempts
  - `'false'` - URL did not return HTTP 200 (or timed out)
- **Note**: Value is a string, not a boolean

**Usage**:
```yaml
- name: Ping Application
  id: ping
  uses: ./.github/actions/docker-ping-url
  with:
    url: https://example.com

- name: Continue if reachable
  if: steps.ping.outputs.url-reachable == 'true'
  run: echo "Application is ready!"
```

## How It Works

### Step-by-Step Flow

```
1. Container Starts
   └─> Python Alpine container is built
   └─> Dependencies installed (requests library)

2. Read Inputs
   └─> INPUT_URL (from action inputs)
   └─> INPUT_MAX_TRAILS (default: 10)
   └─> INPUT_DELAY (default: 5)

3. Retry Loop
   └─> For each attempt (1 to max_trails):
       ├─> Send HTTP GET request to URL
       ├─> Check status code
       │   ├─> 200: Success! Set output and exit
       │   └─> Other: Wait {delay} seconds, retry
       └─> If max attempts reached: Fail action

4. Set Output
   └─> url-reachable = true (success) or false (failure)
```

### Timing Examples

**Configuration**:
```yaml
max_trails: 10
delay: 5
```

**Best case** (app responds immediately):
- Attempt 1: HTTP 200 ✓
- Total time: ~1 second

**Worst case** (app never responds):
- Attempt 1-10: All fail
- Total time: ~50 seconds (10 attempts × 5 seconds)

**Typical case** (app takes 20 seconds to start):
- Attempts 1-3: Fail (15 seconds elapsed)
- Attempt 4: HTTP 200 ✓
- Total time: ~20 seconds

## Implementation Details

### File Structure

```
.github/actions/docker-ping-url/
├── action.yaml          # Action definition
├── Dockerfile           # Container definition
├── main.py              # Python ping script
├── requirements.txt     # Python dependencies
├── .dockerignore        # Files to exclude from build
└── README.md            # This file
```

### Dockerfile Breakdown

```dockerfile
FROM python:alpine3.19    # Lightweight Python image (~50MB)
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "/app/main.py" ]
```

**Why Alpine**:
- Small image size (50MB vs 900MB for standard Python)
- Faster action startup
- Sufficient for HTTP requests

### Python Script (main.py)

```python
import os
import requests
import time

url = os.getenv('INPUT_URL')
max_trails = int(os.getenv('INPUT_MAX_TRAILS', 10))
delay = int(os.getenv('INPUT_DELAY', 5))

for attempt in range(1, max_trails + 1):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Success on attempt {attempt}")
            print(f"::set-output name=url-reachable::true")
            exit(0)
    except Exception as e:
        print(f"Attempt {attempt} failed: {e}")

    if attempt < max_trails:
        time.sleep(delay)

print(f"Failed after {max_trails} attempts")
print(f"::set-output name=url-reachable::false")
exit(1)
```

**Key features**:
- Reads inputs from environment variables (`INPUT_*`)
- Uses `requests` library for HTTP
- Sets output with `::set-output`
- Exits with code 1 on failure

## Real-World Example

Typical deployment workflow:

```yaml
name: Deploy and Verify

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Production
        run: |
          # Deploy application
          ./scripts/deploy.sh
          echo "Deployment initiated"

      - name: Wait for Application
        uses: ./.github/actions/docker-ping-url
        with:
          url: https://production.example.com/health
          max_trails: 30      # Wait up to 2.5 minutes
          delay: 5

      - name: Run Smoke Tests
        run: npm run test:smoke

      - name: Notify Success
        run: echo "Deployment verified!"
```

## Comparison: Docker vs Other Action Types

| Feature | Docker | Composite | JavaScript |
|---------|--------|-----------|------------|
| **Language** | Any | YAML only | JavaScript |
| **Speed** | Slower (build) | Fast | Fast |
| **Isolation** | Full | Shared | Shared |
| **Dependencies** | Self-contained | Uses runner | Uses runner |
| **Use case** | Any language | Combine steps | Node.js logic |

**This action** uses Docker because:
- Python script (not JavaScript)
- Self-contained dependencies
- Reproducible environment
- No Node.js required

## Testing the Action

### Local Testing (Optional)

```bash
cd .github/actions/docker-ping-url

# Build container
docker build -t ping-url .

# Test against a URL
docker run \
  -e INPUT_URL=https://httpbin.org/status/200 \
  -e INPUT_MAX_TRAILS=5 \
  -e INPUT_DELAY=2 \
  ping-url
```

### GitHub Actions Testing

```yaml
name: Test Ping Action

on: workflow_dispatch

jobs:
  test-ping:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Test with healthy URL
        uses: ./.github/actions/docker-ping-url
        with:
          url: https://httpbin.org/status/200
          max_trails: 3
          delay: 1

      - name: Test with unhealthy URL (will fail)
        continue-on-error: true
        uses: ./.github/actions/docker-ping-url
        with:
          url: https://httpbin.org/status/500
          max_trails: 2
          delay: 1
```

## Troubleshooting

### Action Fails Immediately

**Problem**: "Failed after 1 attempt"

**Possible causes**:

1. **URL not reachable**
   ```bash
   # Test URL manually
   curl -I https://your-url.com
   ```

2. **Wrong URL format**
   ```yaml
   # ✓ Correct
   url: https://example.com

   # ✗ Wrong
   url: example.com  # Missing protocol
   ```

3. **Application not deployed yet**
   ```yaml
   # Make sure deployment completes first
   - name: Deploy
     run: ./deploy.sh

   - name: Wait for deployment to propagate
     run: sleep 10  # Add buffer time

   - name: Health check
     uses: ./.github/actions/docker-ping-url
   ```

### Action Times Out

**Problem**: Reaches `max_trails` without success

**Solutions**:

```yaml
# Increase attempts
max_trails: 30    # From 10 to 30

# Increase delay
delay: 10         # From 5 to 10 seconds

# Total wait time: 30 × 10 = 300 seconds (5 minutes)
```

### Non-200 Response Treated as Failure

**Problem**: URL returns 301/302 redirect or 404

**Solution**: Ensure URL returns HTTP 200

```bash
# Check status code
curl -I https://your-url.com

# If redirect, use final URL
url: https://final-destination.com
```

### Docker Build Fails

**Problem**: "ERROR: failed to solve with frontend dockerfile.v0"

**Checks**:
```bash
# 1. Verify Dockerfile exists
ls -la .github/actions/docker-ping-url/Dockerfile

# 2. Verify requirements.txt exists
ls -la .github/actions/docker-ping-url/requirements.txt

# 3. Check Dockerfile syntax
cd .github/actions/docker-ping-url
docker build -t test .
```

## Best Practices

### 1. Set Appropriate Timeouts

```yaml
# Quick health checks
max_trails: 5
delay: 3
# Total: 15 seconds

# Slow-starting applications
max_trails: 30
delay: 10
# Total: 5 minutes
```

### 2. Use Health Check Endpoints

```yaml
# ✓ Good - dedicated health endpoint
url: https://api.example.com/health

# ✗ Less ideal - full page load
url: https://example.com
```

### 3. Handle Failures Gracefully

```yaml
- name: Health Check
  id: health
  continue-on-error: true  # Don't fail workflow
  uses: ./.github/actions/docker-ping-url
  with:
    url: ${{ env.APP_URL }}

- name: Notify if failed
  if: steps.health.outputs.url-reachable != 'true'
  run: |
    echo "::warning::Application health check failed"
    # Send notification to Slack, email, etc.
```

### 4. Use with Environments

```yaml
jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy
        run: ./deploy.sh staging

      - name: Verify Staging
        uses: ./.github/actions/docker-ping-url
        with:
          url: https://staging.example.com

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy
        run: ./deploy.sh production

      - name: Verify Production
        uses: ./.github/actions/docker-ping-url
        with:
          url: https://production.example.com
          max_trails: 30  # More retries for prod
```

## Performance Considerations

### Container Build Time

**First run** (cold):
- Build Docker image: ~30 seconds
- Run Python script: ~5-50 seconds
- **Total**: ~35-80 seconds

**Subsequent runs** (cache hit):
- Reuse cached image: ~5 seconds
- Run Python script: ~5-50 seconds
- **Total**: ~10-55 seconds

### Optimization Tips

```dockerfile
# Layer caching optimization
COPY requirements.txt .          # Copy deps first
RUN pip install -r requirements.txt  # Install (cached layer)
COPY . .                         # Copy code (changes frequently)
```

This ensures dependency installation is cached even when `main.py` changes.

## Related Resources

- **Workflow Example**: [17-3-custom-actions-docker.yaml](../../workflows/17-3-custom-actions-docker.yaml)
- **GitHub Docs**: [Creating Docker Actions](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)
- **Python Requests**: [Documentation](https://requests.readthedocs.io/)
- **Deployment Patterns**: [Deployment Environments (Lesson 16)](../../workflows/16-environments.yaml)

## License

This action is part of the GitHub Actions Course educational materials.
