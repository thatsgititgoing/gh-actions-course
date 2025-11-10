# Lesson 13: Caching Dependencies

Learn how to dramatically speed up workflows by caching NPM dependencies, reducing build times from minutes to seconds.

## Overview

This lesson demonstrates:
- Using `actions/cache` to cache `node_modules`
- Cache key generation based on `package-lock.json`
- Conditional caching with workflow inputs
- Measuring cache effectiveness
- Dev vs Prod dependency management

## Directory Structure

```
13-caching/
└── react-app/              # Sample React application
    ├── src/                # React source code
    ├── public/             # Static assets
    ├── package.json        # Dependencies and scripts
    └── package-lock.json   # Dependency lock file (used for cache key)
```

## Workflow

**File**: [../.github/workflows/13-caching.yaml](../.github/workflows/13-caching.yaml)

### What It Does

```yaml
on:
  workflow_dispatch:
    inputs:
      use-cache:
        type: boolean
        default: true
        description: Whether to execute cache step

      node-version:
        type: choice
        options: [18.x, 20.x, 21.x]
        default: 20.x

jobs:
  build:
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v3
        with:
          node-version: ${{ inputs.node-version }}

      # Cache dependencies
      - name: Download cached dependencies
        uses: actions/cache@v3
        if: ${{ inputs.use-cache }}
        id: cache
        with:
          path: 13-caching/react-app/node_modules
          key: node_modules-${{ inputs.node-version }}-${{ hashFiles('13-caching/react-app/package-lock.json') }}

      # Install only if cache miss
      - name: Install dependencies
        if: steps.cache.outputs.cache-hit != 'true'
        run: npm ci
```

## Key Concepts

### 1. Cache Action

**Syntax**:
```yaml
- uses: actions/cache@v3
  with:
    path: {directory-to-cache}
    key: {unique-cache-key}
```

**How it works**:
1. **Cache Hit**: Restores `node_modules` from cache (~10-15 seconds)
2. **Cache Miss**: Runs `npm ci` and saves to cache (~45-60 seconds)

### 2. Cache Key Strategy

```yaml
key: node_modules-${{ inputs.node-version }}-${{ hashFiles('package-lock.json') }}
```

**Components**:
- `node_modules` - Cache identifier/prefix
- `{node-version}` - Separate caches per Node version
- `{hash}` - SHA-256 hash of `package-lock.json`

**Cache invalidation**:
- ✅ Hits when dependencies unchanged
- ❌ Misses when `package-lock.json` changes

**Example keys**:
```
node_modules-20.x-a3f9b2c1d4e5f6...
node_modules-18.x-a3f9b2c1d4e5f6...
node_modules-20.x-b2c3d4e5f6a7b8...  ← Different hash (deps changed)
```

### 3. Conditional Installation

```yaml
- name: Install dependencies
  if: steps.cache.outputs.cache-hit != 'true'
  run: npm ci
```

**Logic**:
- Skip `npm ci` if cache restored
- Run `npm ci` only on cache miss

**Output values**:
- `cache-hit: 'true'` - Dependencies restored from cache
- `cache-hit: 'false'` (or undefined) - Cache miss, need to install

## Performance Comparison

### Without Caching

```
Setup Node:    5s
Install deps:  45s
Build:         20s
Test:          10s
────────────────────
Total:         80s
```

### With Caching (Cache Hit)

```
Setup Node:    5s
Restore cache: 12s  ← Fast!
Build:         20s
Test:          10s
────────────────────
Total:         47s  ← 41% faster
```

### With Caching (Cache Miss)

```
Setup Node:    5s
Install deps:  45s
Save cache:    8s
Build:         20s
Test:          10s
────────────────────
Total:         88s  ← Slightly slower (one-time cost)
```

**Key insight**: First run is slower (saving cache), but subsequent runs are much faster!

## Running the Workflow

### Trigger with Inputs

**Option 1: GitHub UI**
1. Go to **Actions** → "13 - Using Caching"
2. Click **Run workflow**
3. Configure:
   - ✅ use-cache: `true` (test caching)
   - 📦 node-version: `20.x`
4. Click **Run workflow**

**Option 2: GitHub CLI**
```bash
# With cache enabled
gh workflow run 13-caching.yaml -f use-cache=true -f node-version=20.x

# Without cache (for comparison)
gh workflow run 13-caching.yaml -f use-cache=false -f node-version=20.x
```

### Compare Results

**First run** (cache miss):
```
Download cached dependencies
- Cache not found for key: node_modules-20.x-abc123...
...
Post Download cached dependencies
- Cache saved with key: node_modules-20.x-abc123...
```

**Second run** (cache hit):
```
Download cached dependencies
- Cache restored from key: node_modules-20.x-abc123...
...
Post Download cached dependencies
- Cache already exists, skipping save
```

## Testing Cache Effectiveness

### Experiment 1: Cache Hit

```bash
# Run 1
gh workflow run 13-caching.yaml -f use-cache=true
# Note the total duration

# Run 2 (no changes to package-lock.json)
gh workflow run 13-caching.yaml -f use-cache=true
# Compare duration - should be much faster
```

### Experiment 2: Cache Miss

```bash
# Modify a dependency
cd 13-caching/react-app
npm install lodash
git add package.json package-lock.json
git commit -m "Add lodash dependency"
git push

# Trigger workflow
gh workflow run 13-caching.yaml -f use-cache=true
# Cache will miss due to new hash
```

### Experiment 3: No Cache

```bash
# Run without cache
gh workflow run 13-caching.yaml -f use-cache=false

# Compare duration with cache-enabled runs
```

## Cache Management

### View Caches

**GitHub UI**:
1. Go to repository **Settings**
2. Navigate to **Actions** → **Caches**
3. View all caches with keys and sizes

**GitHub CLI**:
```bash
gh cache list
```

### Delete Caches

```bash
# Delete specific cache
gh cache delete <cache-id>

# Delete all caches (for testing)
gh cache delete --all
```

**Note**: Caches are automatically deleted after 7 days of no access.

## Common Issues

### Cache Not Restoring

**Problem**: Always seeing "Cache not found"

**Checks**:
1. **Verify path is correct**:
   ```yaml
   path: 13-caching/react-app/node_modules  # ✓ Absolute from repo root
   path: node_modules                        # ✗ Wrong if in subdirectory
   ```

2. **Check key format**:
   ```yaml
   # ✓ Includes full path to package-lock.json
   key: node_modules-${{ hashFiles('13-caching/react-app/package-lock.json') }}

   # ✗ Wrong path
   key: node_modules-${{ hashFiles('package-lock.json') }}
   ```

3. **Ensure package-lock.json exists**:
   ```bash
   ls -la 13-caching/react-app/package-lock.json
   ```

### Dependencies Not Installing

**Problem**: Workflow skips installation but tests fail

**Cause**: Cache restored but has old/corrupt dependencies

**Solution**:
```bash
# Delete the cache
gh cache delete <cache-id>

# Or change the cache key prefix
key: node_modules-v2-${{ ... }}  # 'v2' invalidates old cache
```

### Cache Size Limit

**Problem**: "Cache size exceeds limit"

**Limit**: 10 GB per repository
**Total**: 5 GB for all caches combined (LRU eviction)

**Solution**: Cache only essential directories
```yaml
# ✓ Good - cache dependencies
path: node_modules

# ✗ Bad - don't cache build outputs
path: |
  node_modules
  build
  dist
```

## Best Practices

### 1. Always Use Package Lock File in Key

```yaml
# ✓ Good - invalidates when deps change
key: deps-${{ hashFiles('**/package-lock.json') }}

# ✗ Bad - never invalidates
key: deps-static-key
```

### 2. Include Relevant Factors in Key

```yaml
# If different OS or Node versions
key: ${{ runner.os }}-node-${{ matrix.node-version }}-${{ hashFiles('...') }}
```

### 3. Use Conditional Installation

```yaml
# Skip install if cache hit
if: steps.cache.outputs.cache-hit != 'true'
```

### 4. Set Reasonable Restore Keys (Fallback)

```yaml
- uses: actions/cache@v3
  with:
    path: node_modules
    key: deps-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      deps-  # Partial match if exact key not found
```

### 5. Monitor Cache Effectiveness

```yaml
- name: Log cache status
  run: |
    if [ "${{ steps.cache.outputs.cache-hit }}" == "true" ]; then
      echo "::notice::Cache hit! Dependencies restored from cache"
    else
      echo "::notice::Cache miss - installing dependencies"
    fi
```

## Running Locally

The React app works the same as lesson 04:

```bash
cd 13-caching/react-app
npm install
npm test
npm run build  # Optional
```

**Note**: Local runs don't use GitHub Actions cache - that's CI-only!

## Next Steps

After mastering caching:

1. **Lesson 14: Artifacts** - Learn to cache build outputs (different from dependencies)
2. **Lesson 17: Custom Actions** - Create a reusable caching action (see `composite-cache-deps`)
3. **Combine caching with matrices** - Cache for multiple Node versions

## Related Resources

- **Workflow**: [13-caching.yaml](../.github/workflows/13-caching.yaml)
- **Custom Action**: [composite-cache-deps](../.github/actions/composite-cache-deps/) - Reusable caching action
- **actions/cache**: [GitHub Marketplace](https://github.com/marketplace/actions/cache)
- **GitHub Docs**: [Caching Dependencies](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)

## Exercise

Try these experiments:

1. **Compare timings**: Run with and without cache, measure the difference
2. **Change Node version**: See how cache keys separate per version
3. **Update a dependency**: Observe cache miss behavior
4. **Create your own cache**: Cache a different directory (e.g., `.next`, `.nuxt`)

---

**← Previous**: [04 - Using Actions](../04-using-actions/) | **Next**: [14 - Artifacts](../14-artifacts/) →
