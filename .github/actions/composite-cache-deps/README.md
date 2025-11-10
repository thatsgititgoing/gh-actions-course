# Composite Action: Cache Node and NPM Dependencies

A composite GitHub Action that caches Node.js dependencies based on `package-lock.json`, with automatic dev/prod mode detection.

## Type

**Composite Action** - Combines multiple workflow steps into a single reusable action.

## Purpose

This action streamlines Node.js project setup by:
1. Installing the specified Node.js version
2. Caching `node_modules` based on `package-lock.json` hash
3. Installing dependencies only when cache misses
4. Supporting both development and production dependency installation

## Location

`.github/actions/composite-cache-deps/`

## Usage

### Basic Example

```yaml
steps:
  - name: Checkout code
    uses: actions/checkout@v4

  - name: Setup Node and Cache Dependencies
    uses: ./.github/actions/composite-cache-deps
    with:
      node-version: 20.x
```

### Full Example with All Options

```yaml
steps:
  - name: Checkout code
    uses: actions/checkout@v4

  - name: Setup Node and Cache Dependencies
    id: setup-deps
    uses: ./.github/actions/composite-cache-deps
    with:
      node-version: 20.x
      working-dir: ./my-app
      target-env: prod

  - name: Check if dependencies were installed
    run: |
      if [ "${{ steps.setup-deps.outputs.installed-deps }}" == "true" ]; then
        echo "Dependencies were freshly installed"
      else
        echo "Dependencies were restored from cache"
      fi
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `node-version` | Node.js version to install (e.g., `18.x`, `20.x`, `21.x`) | Yes | `20.x` |
| `working-dir` | Working directory of the application | No | `.` (root) |
| `target-env` | Target environment: `dev` or `prod` | No | `dev` |

### Input Details

#### `node-version`
- **Type**: String
- **Examples**: `18.x`, `20.x`, `21.x`, `20.11.0`
- **Purpose**: Specifies which Node.js version to install
- **Used by**: `actions/setup-node@v3`

#### `working-dir`
- **Type**: String
- **Purpose**: Directory containing `package.json` and `package-lock.json`
- **Examples**:
  - `.` (default - root directory)
  - `./app`
  - `packages/frontend`

#### `target-env`
- **Type**: String
- **Values**: `dev` | `prod`
- **Purpose**:
  - `dev`: Installs all dependencies including devDependencies (`npm ci`)
  - `prod`: Installs only production dependencies (`npm ci --omit=dev`)
- **Use case**: Set to `prod` for deployment workflows, `dev` for test/build workflows

## Outputs

| Output | Description | Type |
|--------|-------------|------|
| `installed-deps` | Whether dependencies were installed (vs restored from cache) | Boolean |

### Output Details

#### `installed-deps`
- **Value**:
  - `true` - Dependencies were freshly installed (cache miss)
  - `false` - Dependencies were restored from cache (cache hit)
- **Use case**: Measure cache effectiveness, skip steps when cache hits

**Example**:
```yaml
- name: Setup dependencies
  id: deps
  uses: ./.github/actions/composite-cache-deps

- name: Display installation message
  if: steps.deps.outputs.installed-deps == 'true'
  run: echo "Fresh install took: X seconds"
```

## How It Works

### Step-by-Step Flow

```
1. Setup Node.js
   └─> Uses actions/setup-node@v3 with specified version

2. Generate Cache Key
   └─> Key format: node_modules-{target-env}-{hash(package-lock.json)}
   └─> Example: node_modules-dev-a3f9b2c1...

3. Check Cache
   └─> Uses actions/cache@v3 to check if cache exists
   └─> If hit: Restore node_modules from cache
   └─> If miss: Continue to step 4

4. Install Dependencies (only if cache miss)
   └─> Dev mode: npm ci (installs all dependencies)
   └─> Prod mode: npm ci --omit=dev (production only)

5. Set Output
   └─> installed-deps = true (cache miss) or false (cache hit)
```

### Cache Key Strategy

The cache key is generated using:
```yaml
key: node_modules-${{ inputs.target-env }}-${{ hashFiles('package-lock.json') }}
```

**Components**:
- `node_modules` - Prefix for identification
- `{target-env}` - `dev` or `prod` (separate caches for each)
- `{hash}` - SHA-256 hash of `package-lock.json`

**Cache invalidation**:
- ✅ Cache hits when `package-lock.json` is unchanged
- ❌ Cache misses when dependencies change

## Benefits

### 1. Speed Improvement
**Without caching**:
```
Setup Node: 5s
Install Dependencies: 45s
Total: 50s
```

**With caching (cache hit)**:
```
Setup Node: 5s
Restore Cache: 10s
Total: 15s (70% faster!)
```

### 2. Consistency
- Same action used across all workflows
- Centralized caching logic
- Consistent cache key generation

### 3. Flexibility
- Dev vs Prod mode support
- Configurable Node versions
- Works with monorepos (custom `working-dir`)

## Real-World Example

See [17-1-custom-actions-composite.yaml](../../workflows/17-1-custom-actions-composite.yaml) for a complete workflow using this action:

```yaml
name: Build React App with Composite Action

on:
  workflow_dispatch:
    inputs:
      target-env:
        type: choice
        options: [dev, prod]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup and Cache Dependencies
        uses: ./.github/actions/composite-cache-deps
        with:
          node-version: 20.x
          working-dir: 17-custom-actions/react-app
          target-env: ${{ inputs.target-env }}

      - name: Build Application
        working-directory: 17-custom-actions/react-app
        run: npm run build
```

## Implementation Details

### File Structure

```
.github/actions/composite-cache-deps/
├── action.yaml       # Action definition
└── README.md         # This file
```

### action.yaml Breakdown

```yaml
name: Cache Node and NPM Dependencies
description: "Caches Node and NPM dependencies based on package-lock.json"

inputs:
  # Input definitions...

outputs:
  installed-deps:
    value: ${{ steps.cache.outputs.cache-hit != 'true' }}

runs:
  using: composite  # Indicates this is a composite action
  steps:
    # Step 1: Setup Node
    # Step 2: Check cache
    # Step 3: Install dependencies (conditional)
```

## Comparison: Composite vs Other Action Types

| Feature | Composite | JavaScript | Docker |
|---------|-----------|------------|--------|
| **Speed** | Fast | Fast | Slower (image build) |
| **Complexity** | Low | Medium | High |
| **Reusability** | High | Highest | High |
| **Language** | YAML only | JavaScript | Any language |
| **Use case** | Combine steps | Complex logic | Isolated environment |

**This action** uses composite because:
- Simple step combination (setup + cache + install)
- No complex logic needed
- Fast execution
- Easy to maintain

## Testing the Action

### Test Cache Hit

```bash
# First run - cache miss
gh workflow run 17-1-custom-actions-composite.yaml -f target-env=dev

# Second run - cache hit (no dependency changes)
gh workflow run 17-1-custom-actions-composite.yaml -f target-env=dev
```

### Test Cache Miss

```bash
# Modify package.json to add/remove a dependency
# Then trigger workflow - cache will miss
gh workflow run 17-1-custom-actions-composite.yaml -f target-env=dev
```

### Verify Cache

1. Go to **Actions** tab
2. Click on workflow run
3. Expand "Setup and Cache Dependencies" step
4. Look for:
   - `Cache restored successfully` (cache hit)
   - `Post job cleanup` → `Cache saved successfully` (cache miss)

## Troubleshooting

### Dependencies Not Cached

**Problem**: Every run installs dependencies from scratch

**Checks**:
```yaml
# 1. Verify working-dir matches package-lock.json location
working-dir: 17-custom-actions/react-app  # ✓ Correct
working-dir: .                              # ✗ Wrong if app is in subdirectory

# 2. Ensure package-lock.json exists
- run: ls -la package-lock.json
  working-directory: ${{ inputs.working-dir }}

# 3. Check cache key in logs
# Should see: "Cache key: node_modules-dev-a3f9b2c1..."
```

### Wrong Dependencies Installed

**Problem**: Production build includes devDependencies

**Solution**:
```yaml
# Make sure target-env is set to 'prod'
- uses: ./.github/actions/composite-cache-deps
  with:
    target-env: prod  # Not 'dev'
```

### Cache Not Invalidating

**Problem**: New dependencies not installed after updating `package.json`

**Solution**:
```bash
# Always run npm install locally to update package-lock.json
npm install

# Commit both files
git add package.json package-lock.json
git commit -m "Add new dependency"
git push
```

The cache key uses `package-lock.json` hash, so it must be updated!

## Best Practices

### 1. Always Commit package-lock.json

```bash
# ✓ Good
git add package.json package-lock.json
git commit -m "Update dependencies"

# ✗ Bad
git add package.json
# (package-lock.json not committed - cache won't update!)
```

### 2. Use Appropriate target-env

```yaml
# Test/Build workflows
target-env: dev    # Need devDependencies for tests

# Deployment workflows
target-env: prod   # Only production dependencies
```

### 3. Monitor Cache Effectiveness

```yaml
- name: Setup Dependencies
  id: setup
  uses: ./.github/actions/composite-cache-deps

- name: Log Cache Performance
  run: |
    if [ "${{ steps.setup.outputs.installed-deps }}" == "true" ]; then
      echo "::notice::Cache miss - dependencies installed"
    else
      echo "::notice::Cache hit - restored from cache"
    fi
```

## Related Resources

- **Workflow Example**: [17-1-custom-actions-composite.yaml](../../workflows/17-1-custom-actions-composite.yaml)
- **GitHub Docs**: [Creating Composite Actions](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)
- **Caching Lesson**: [13-caching.yaml](../../workflows/13-caching.yaml)
- **actions/cache**: [GitHub Marketplace](https://github.com/marketplace/actions/cache)

## License

This action is part of the GitHub Actions Course educational materials.
