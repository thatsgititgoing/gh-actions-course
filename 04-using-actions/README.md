# Lesson 04: Using Actions

Learn how to use GitHub Marketplace actions in your workflows by building and testing a React application.

## Overview

This lesson demonstrates:
- Using `actions/checkout` to clone repository code
- Using `actions/setup-node` to install Node.js
- Installing NPM dependencies
- Running unit tests in CI

## Directory Structure

```
04-using-actions/
└── react-app/              # Sample React application
    ├── src/                # React source code
    ├── public/             # Static assets
    ├── package.json        # Dependencies and scripts
    └── package-lock.json   # Locked dependency versions
```

## Workflow

**File**: [../.github/workflows/04-using-actions.yaml](../.github/workflows/04-using-actions.yaml)

### What It Does

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: 04-using-actions/react-app

    steps:
      # 1. Checkout code using marketplace action
      - name: Checkout Code
        uses: actions/checkout@v5

      # 2. Setup Node.js using marketplace action
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'

      # 3. Install dependencies
      - name: Install Dependencies
        run: npm ci

      # 4. Run tests
      - name: Run Unit Tests
        run: npm run test
```

## Key Concepts

### 1. Using Marketplace Actions

**Syntax**:
```yaml
- uses: {owner}/{repo}@{version}
  with:
    {input-name}: {value}
```

**Examples in this workflow**:
- `actions/checkout@v5` - Clones the repository
- `actions/setup-node@v4` - Installs Node.js

**Benefits**:
- No need to write installation scripts
- Maintained by the community
- Version pinning for stability

### 2. Working Directory

```yaml
defaults:
  run:
    working-directory: 04-using-actions/react-app
```

**Purpose**: All `run` commands execute from this directory
**Alternative**: Use `working-directory` on individual steps

### 3. npm ci vs npm install

**This workflow uses `npm ci`**:
- ✅ Faster (skips some checks)
- ✅ Uses exact versions from `package-lock.json`
- ✅ Better for CI/CD pipelines
- ✅ Deletes `node_modules` first (clean install)

**npm install**:
- For local development
- Can update `package-lock.json`

## Running Locally

### Prerequisites

```bash
# Install Node.js 18+ (if not installed)
node --version
npm --version
```

### Setup and Test

```bash
# Navigate to the React app
cd 04-using-actions/react-app

# Install dependencies
npm install

# Run tests
npm test

# Build the application (optional)
npm run build

# Start development server (optional)
npm start
```

## Running in GitHub Actions

### Trigger the Workflow

**Option 1: Via GitHub UI**
1. Go to **Actions** tab
2. Select "04 - Using Actions"
3. Click **Run workflow** → **Run workflow**

**Option 2: Via GitHub CLI**
```bash
gh workflow run 04-using-actions.yaml
```

### View Results

1. Click on the workflow run
2. Expand the "build" job
3. Check each step:
   - ✓ Checkout Code
   - ✓ Setup Node
   - ✓ Install Dependencies
   - ✓ Run Unit Tests

## What You'll Learn

### Actions from GitHub Marketplace

**actions/checkout@v5**:
- Clones your repository code
- Checks out the specific commit/branch
- Required for almost all workflows

**actions/setup-node@v4**:
- Installs specified Node.js version
- Configures npm registry
- Caches global npm packages (when configured)

### Workflow Execution Flow

```
1. GitHub provisions runner (ubuntu-latest)
2. Checkout code (empty runner → has your code)
3. Setup Node.js (install Node 20.x)
4. Install dependencies (npm ci)
5. Run tests (npm test)
6. Clean up and report results
```

## Common Issues

### Tests Fail Locally but Pass in CI

**Cause**: Different Node.js versions
**Solution**: Use the same version as in workflow
```bash
nvm install 20
nvm use 20
npm test
```

### npm ci Fails

**Problem**: `package-lock.json` is missing or out of sync

**Solution**:
```bash
# Regenerate package-lock.json
rm package-lock.json
npm install
git add package-lock.json
git commit -m "Update package-lock.json"
```

### Working Directory Errors

**Problem**: "ENOENT: no such file or directory"

**Check**:
```yaml
# Ensure path is correct
working-directory: 04-using-actions/react-app  # ✓
working-directory: react-app                    # ✗ Missing parent dir
```

## Next Steps

After completing this lesson:

1. **Lesson 13: Caching** - Speed up workflows by caching `node_modules`
2. **Lesson 14: Artifacts** - Store build outputs
3. **Lesson 17: Custom Actions** - Create your own reusable actions

## Related Resources

- **Workflow**: [04-using-actions.yaml](../.github/workflows/04-using-actions.yaml)
- **actions/checkout**: [GitHub Marketplace](https://github.com/marketplace/actions/checkout)
- **actions/setup-node**: [GitHub Marketplace](https://github.com/marketplace/actions/setup-node)
- **GitHub Actions Docs**: [Using Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsuses)

## Exercise

Try modifying the workflow to:
1. Test with multiple Node.js versions (18.x, 20.x, 21.x)
2. Add a build step after tests
3. Upload build artifacts (preview of lesson 14)

**Hint**: Use matrix strategy (covered in lesson 15)

---

**Next Lesson**: [13 - Caching](../13-caching/) →
