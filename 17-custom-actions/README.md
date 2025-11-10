# Lesson 17: Custom Actions

Learn how to create your own reusable GitHub Actions in three different styles: Composite, JavaScript, and Docker. Build production-ready actions that can be shared across workflows and repositories.

## Overview

This lesson demonstrates:
- **Composite Actions**: Combine multiple workflow steps into one action
- **JavaScript Actions**: Use Node.js for complex logic and GitHub API access
- **Docker Actions**: Containerize actions using any programming language
- When to use each type
- Best practices for action development

## Directory Structure

```
17-custom-actions/
├── react-app/                      # Sample React app for testing actions
│   ├── src/
│   ├── package.json
│   └── package-lock.json
└── (See .github/actions/ for custom action code)
```

## Custom Actions in This Course

### 1. Composite Action: cache-deps
**Location**: [../.github/actions/composite-cache-deps/](../.github/actions/composite-cache-deps/)
**Documentation**: [README](../.github/actions/composite-cache-deps/README.md)

**Purpose**: Cache Node.js dependencies with dev/prod mode support

**Type**: Composite (YAML-based, combines existing actions)

**Workflow**: [17-1-custom-actions-composite.yaml](../.github/workflows/17-1-custom-actions-composite.yaml)

---

### 2. JavaScript Action: js-dependency-update
**Location**: [../.github/actions/js-dependency-update/](../.github/actions/js-dependency-update/)
**Documentation**: [README](../.github/actions/js-dependency-update/README.md)

**Purpose**: Check for NPM updates and create pull requests

**Type**: JavaScript (Node.js 20, uses @actions/core and @actions/github)

**Workflow**: [17-2-custom-actions-js.yaml](../.github/workflows/17-2-custom-actions-js.yaml)

---

### 3. Docker Action: docker-ping-url
**Location**: [../.github/actions/docker-ping-url/](../.github/actions/docker-ping-url/)
**Documentation**: [README](../.github/actions/docker-ping-url/README.md)

**Purpose**: Health check URLs with retry logic

**Type**: Docker (Python-based, containerized)

**Workflow**: [17-3-custom-actions-docker.yaml](../.github/workflows/17-3-custom-actions-docker.yaml)

## Workflows

### Workflow 17-1: Composite Action

**File**: [../.github/workflows/17-1-custom-actions-composite.yaml](../.github/workflows/17-1-custom-actions-composite.yaml)

```yaml
jobs:
  build:
    steps:
      - uses: actions/checkout@v4

      # Use the custom composite action
      - name: Setup Node and NPM Dependencies
        id: setup-deps
        uses: ./.github/actions/composite-cache-deps
        with:
          node-version: 20.x
          working-dir: 17-custom-actions/react-app
          target-env: ${{ inputs.target-env }}

      - name: Build
        run: npm run build
```

**What it does**:
1. Uses custom composite action to setup Node + cache deps
2. Action handles: Node setup, caching, dependency installation
3. One action replaces 3-4 separate steps

---

### Workflow 17-2: JavaScript Action

**File**: [../.github/workflows/17-2-custom-actions-js.yaml](../.github/workflows/17-2-custom-actions-js.yaml)

```yaml
jobs:
  check-updates:
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4

      # Use the custom JavaScript action
      - name: Check for Dependency Updates
        uses: ./.github/actions/js-dependency-update
        with:
          working-directory: 17-custom-actions/react-app
          gh-token: ${{ secrets.GITHUB_TOKEN }}
          debug: true
```

**What it does**:
1. Uses custom JS action to check for NPM updates
2. Action runs Node.js code with GitHub API access
3. Validates inputs, runs npm update, detects changes

---

### Workflow 17-3: Docker Action

**File**: [../.github/workflows/17-3-custom-actions-docker.yaml](../.github/workflows/17-3-custom-actions-docker.yaml)

```yaml
jobs:
  health-check:
    steps:
      # Use the custom Docker action
      - name: Ping URL
        uses: ./.github/actions/docker-ping-url
        with:
          url: https://httpbin.org/status/200
          max_trails: 5
          delay: 3
```

**What it does**:
1. Uses custom Docker action to ping a URL
2. Action runs Python script in a container
3. Retries with configurable delay until success

## Action Type Comparison

| Feature | Composite | JavaScript | Docker |
|---------|-----------|------------|--------|
| **Implementation** | YAML (workflow steps) | JavaScript/TypeScript | Any language |
| **Speed** | Fast (~seconds) | Fast (~seconds) | Slower (~30s+ build) |
| **Complexity** | Low | Medium | High |
| **Dependencies** | Uses existing actions | Node.js packages | Full environment |
| **API Access** | Via CLI tools | Full (Octokit) | Via CLI tools |
| **Portability** | GitHub Actions only | GitHub Actions only | Any Docker platform |
| **Debugging** | Easy (YAML) | Medium (Node.js) | Harder (container) |
| **Best for** | Combining steps | Complex logic, API | Any language, isolation |

## When to Use Each Type

### Use Composite Actions When:
- ✅ Combining multiple existing actions/steps
- ✅ Reusing common workflow patterns
- ✅ Need fast execution
- ✅ Logic is simple (no complex conditionals)

**Example use cases**:
- Setup Node + cache dependencies
- Checkout + setup multiple tools
- Common pre/post deployment steps

### Use JavaScript Actions When:
- ✅ Need complex logic or conditionals
- ✅ Require GitHub API access (Octokit)
- ✅ Input validation and processing
- ✅ Action output calculations
- ✅ Familiar with JavaScript/TypeScript

**Example use cases**:
- Creating pull requests programmatically
- Processing JSON/YAML files
- Complex dependency management
- API integrations

### Use Docker Actions When:
- ✅ Need a specific programming language (Python, Go, Ruby, etc.)
- ✅ Require specific tools/dependencies
- ✅ Need complete isolation
- ✅ Want reproducible environment

**Example use cases**:
- Python scripts (data processing, ML)
- Go binaries (performance-critical tasks)
- Legacy tools that need specific versions
- Security scanning tools

## Creating Your Own Action

### Basic Action Structure

All actions need an `action.yaml` file:

```yaml
name: My Custom Action
description: What this action does

inputs:
  my-input:
    description: Input description
    required: true
    default: default-value

outputs:
  my-output:
    description: Output description

runs:
  using: {composite|node20|docker}
  # Additional configuration based on type
```

### Composite Action Template

```yaml
name: My Composite Action
description: Combines multiple steps

inputs:
  example-input:
    required: true

runs:
  using: composite
  steps:
    - name: Step 1
      run: echo "Input: ${{ inputs.example-input }}"
      shell: bash

    - name: Step 2
      uses: actions/checkout@v4
```

**Key points**:
- Must specify `shell` for `run` commands
- Can use other actions with `uses`
- Can reference inputs with `${{ inputs.* }}`

### JavaScript Action Template

```yaml
name: My JavaScript Action
description: Node.js powered action

inputs:
  example-input:
    required: true

outputs:
  result:
    description: Action result

runs:
  using: node20
  main: index.js
```

**index.js**:
```javascript
const core = require('@actions/core');

async function run() {
  try {
    const input = core.getInput('example-input');
    core.info(`Processing: ${input}`);

    // Your logic here

    core.setOutput('result', 'success');
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
```

### Docker Action Template

```yaml
name: My Docker Action
description: Containerized action

inputs:
  example-input:
    required: true

runs:
  using: docker
  image: Dockerfile
```

**Dockerfile**:
```dockerfile
FROM python:alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "/app/main.py"]
```

## Running the Workflows

### Test Composite Action

```bash
gh workflow run 17-1-custom-actions-composite.yaml -f target-env=dev
```

**Expected**: Sets up Node, caches deps, builds app

### Test JavaScript Action

```bash
gh workflow run 17-2-custom-actions-js.yaml
```

**Expected**: Checks for dependency updates, logs results

### Test Docker Action

```bash
gh workflow run 17-3-custom-actions-docker.yaml
```

**Expected**: Pings URL, succeeds when HTTP 200 received

## Running React App Locally

```bash
cd 17-custom-actions/react-app

# Install dependencies
npm install

# Run tests
npm test

# Build
npm run build

# Verify custom actions worked (if run in workflow)
ls -la node_modules  # Should exist if composite action ran
```

## Best Practices

### 1. Clear Documentation

```yaml
name: Descriptive Action Name
description: Clear description of what the action does

inputs:
  my-input:
    description: Detailed description of this input
    required: true
    default: sensible-default
```

### 2. Input Validation

**JavaScript**:
```javascript
const core = require('@actions/core');

const input = core.getInput('my-input');
if (!input) {
  core.setFailed('my-input is required');
  return;
}

if (!/^[a-zA-Z0-9-]+$/.test(input)) {
  core.setFailed('my-input contains invalid characters');
  return;
}
```

### 3. Meaningful Outputs

```yaml
outputs:
  cache-hit:
    description: Whether cache was hit (true/false)
  installed-deps:
    description: Whether dependencies were installed
```

### 4. Error Handling

```javascript
try {
  // Action logic
  core.info('Success message');
} catch (error) {
  core.setFailed(`Action failed: ${error.message}`);
}
```

### 5. Logging

```javascript
core.info('Informational message');
core.warning('Warning message');
core.error('Error message');
core.debug('Debug message (only if ACTIONS_STEP_DEBUG=true)');
```

## Common Issues

### Action Not Found

**Problem**: "Unable to resolve action"

**Cause**: Wrong path to action

**Solution**:
```yaml
# ✓ Correct - relative path from repo root
uses: ./.github/actions/my-action

# ✗ Wrong
uses: ./my-action  # Missing .github/actions/
```

### Composite Action Shell Error

**Problem**: "Shell must be specified"

**Solution**:
```yaml
# ✓ Must specify shell in composite actions
- run: echo "Hello"
  shell: bash

# ✗ Missing shell
- run: echo "Hello"
```

### JavaScript Dependencies Not Found

**Problem**: "Cannot find module '@actions/core'"

**Solution**:
```bash
cd .github/actions/my-js-action
npm install
git add node_modules  # Or use @vercel/ncc to bundle
```

### Docker Build Fails

**Problem**: "Failed to build docker image"

**Checks**:
1. Dockerfile exists in action directory
2. All COPY paths are correct
3. requirements.txt or package.json exists
4. Build locally to debug: `docker build -t test .`

## Advanced Topics

### Publishing Actions

**To GitHub Marketplace**:
1. Create public repository
2. Add `action.yaml` at root
3. Create release with tag (v1, v1.0.0)
4. GitHub automatically lists it

**To use**:
```yaml
uses: username/action-repo@v1
```

### Versioning

```yaml
uses: ./.github/actions/my-action@v1      # Major version
uses: ./.github/actions/my-action@v1.2    # Minor version
uses: ./.github/actions/my-action@v1.2.3  # Patch version
uses: ./.github/actions/my-action@main    # Branch
uses: ./.github/actions/my-action@abc123  # Commit SHA
```

### Testing Actions Locally

**Composite**: Test individual steps
**JavaScript**: Run with Node.js and environment variables
**Docker**: Build and run container locally

## Next Steps

After mastering custom actions:

1. **Lesson 18: Reusable Workflows** - Call workflows like functions
2. **Publish an action** - Share your action on GitHub Marketplace
3. **Combine techniques** - Use custom actions in reusable workflows

## Related Resources

### Custom Actions
- [composite-cache-deps](../.github/actions/composite-cache-deps/README.md)
- [js-dependency-update](../.github/actions/js-dependency-update/README.md)
- [docker-ping-url](../.github/actions/docker-ping-url/README.md)

### Workflows
- [17-1-custom-actions-composite.yaml](../.github/workflows/17-1-custom-actions-composite.yaml)
- [17-2-custom-actions-js.yaml](../.github/workflows/17-2-custom-actions-js.yaml)
- [17-3-custom-actions-docker.yaml](../.github/workflows/17-3-custom-actions-docker.yaml)

### GitHub Docs
- [Creating Actions](https://docs.github.com/en/actions/creating-actions)
- [Metadata Syntax](https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions)
- [Publishing Actions](https://docs.github.com/en/actions/creating-actions/publishing-actions-in-github-marketplace)

## Exercise

Try creating your own action:

1. **Composite**: Create an action that sets up Python + installs pip dependencies
2. **JavaScript**: Create an action that validates JSON files
3. **Docker**: Create an action that runs a simple shell script

---

**← Previous**: [14 - Artifacts](../14-artifacts/) | **Next**: [Main README](../README.md) →
