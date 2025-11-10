# Lesson 14: Working with Artifacts

Learn how to share data between jobs and preserve build outputs using GitHub Actions artifacts, enabling multi-job workflows and debugging capabilities.

## Overview

This lesson demonstrates:
- Uploading build artifacts with `actions/upload-artifact`
- Downloading artifacts in subsequent jobs
- Artifact naming and organization
- Job dependencies with `needs`
- Separating build and deploy stages

## Directory Structure

```
14-artifacts/
└── react-app/              # Sample React application
    ├── src/                # React source code
    ├── public/             # Static assets
    ├── build/              # Build output (created by npm run build)
    ├── coverage/           # Test coverage (created by npm test --coverage)
    ├── package.json        # Dependencies and scripts
    └── package-lock.json   # Dependency lock file
```

## Workflow

**File**: [../.github/workflows/14-artifacts.yaml](../.github/workflows/14-artifacts.yaml)

### What It Does

```yaml
env:
  build-artifact-key: app-${{ github.sha }}
  test-coverage-key: test-coverage-${{ github.sha }}

jobs:
  # Job 1: Build and test
  test-build:
    steps:
      - name: Unit tests
        run: npm run test -- --coverage

      # Upload test coverage
      - name: Upload test results
        uses: actions/upload-artifact@v4
        with:
          name: ${{ env.test-coverage-key }}
          path: 14-artifacts/react-app/coverage

      - name: Build code
        run: npm run build

      # Upload build output
      - name: Upload build files
        uses: actions/upload-artifact@v4
        with:
          name: ${{ env.build-artifact-key }}
          path: 14-artifacts/react-app/build

  # Job 2: Deploy (waits for test-build)
  deploy:
    needs: test-build
    steps:
      # Download build artifact
      - name: Download build artifact
        uses: actions/download-artifact@v4
        with:
          name: ${{ env.build-artifact-key }}
          path: build

      - name: Show build files
        run: ls -R build
```

## Key Concepts

### 1. Artifacts vs Caching

| Feature | Artifacts | Cache |
|---------|-----------|-------|
| **Purpose** | Share data between jobs | Speed up workflows |
| **Lifespan** | 90 days (default) | 7 days (unused) |
| **Size limit** | 10 GB per workflow | 10 GB per repo |
| **Use case** | Build outputs, test results | Dependencies, build tools |
| **Access** | Downloadable from UI | Internal only |

**Example**:
- ✓ Cache: `node_modules`
- ✓ Artifact: `build/`, `coverage/`, `dist/`

### 2. Upload Artifact

**Syntax**:
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: {artifact-name}
    path: {directory-or-file}
    retention-days: {optional-days}  # Default: 90
```

**Example**:
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: my-app-build
    path: build/
```

**What happens**:
1. Compresses `build/` directory
2. Uploads to GitHub
3. Artifact appears in workflow run UI
4. Available for download for 90 days

### 3. Download Artifact

**Syntax**:
```yaml
- uses: actions/download-artifact@v4
  with:
    name: {artifact-name}
    path: {destination-directory}  # Optional
```

**Example**:
```yaml
- uses: actions/download-artifact@v4
  with:
    name: my-app-build
    path: ./downloaded-build
```

**What happens**:
1. Downloads compressed artifact
2. Extracts to specified path
3. Files available in subsequent steps

### 4. Job Dependencies

```yaml
jobs:
  build:
    # ... builds the app

  deploy:
    needs: build  # Wait for 'build' to complete
    # ... deploys the app
```

**Execution flow**:
```
build job → (completes) → deploy job starts
```

**Benefits**:
- Separate concerns (build vs deploy)
- Fail fast (deploy doesn't run if build fails)
- Parallel jobs where possible

### 5. Artifact Naming

```yaml
env:
  build-artifact-key: app-${{ github.sha }}
  test-coverage-key: test-coverage-${{ github.sha }}
```

**Why include `github.sha`**:
- Unique per commit
- Prevents conflicts in concurrent runs
- Easy to identify which commit produced artifact

**Example names**:
```
app-a3f9b2c1d4e5f6a7b8c9d0e1f2a3b4c5
test-coverage-a3f9b2c1d4e5f6a7b8c9d0e1f2a3b4c5
```

## Workflow Execution Flow

```
┌──────────────────────┐
│   test-build job     │
├──────────────────────┤
│ 1. Checkout          │
│ 2. Setup Node        │
│ 3. Install deps      │
│ 4. Run tests         │
│    └─> coverage/     │
│ 5. Upload coverage ✓ │  ← Artifact 1
│ 6. Build app         │
│    └─> build/        │
│ 7. Upload build ✓    │  ← Artifact 2
└──────────┬───────────┘
           │
           ▼ (needs: test-build)
┌──────────────────────┐
│     deploy job       │
├──────────────────────┤
│ 1. Download build ✓  │  ← Gets Artifact 2
│ 2. List files        │
│ 3. Deploy (simulated)│
└──────────────────────┘
```

## Running the Workflow

### Trigger the Workflow

```bash
# Via GitHub CLI
gh workflow run 14-artifacts.yaml

# Or via GitHub UI
# Actions → "14 - Working with Artifacts" → Run workflow
```

### View Artifacts

**After workflow completes**:

1. Go to the workflow run
2. Scroll to bottom → **Artifacts** section
3. See both artifacts:
   - `app-{sha}` - Build output
   - `test-coverage-{sha}` - Test coverage

4. Click to download ZIP file

### Download Artifacts Programmatically

```bash
# List artifacts for a run
gh run view <run-id> --log

# Download artifact
gh run download <run-id> -n app-{sha}
```

## Artifact Use Cases

### 1. Build Once, Deploy Many

```yaml
jobs:
  build:
    steps:
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  deploy-staging:
    needs: build
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
      - run: ./deploy-staging.sh

  deploy-production:
    needs: build
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
      - run: ./deploy-production.sh
```

### 2. Test Results and Coverage

```yaml
- name: Run tests with coverage
  run: npm test -- --coverage

- name: Upload coverage
  uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: coverage/
```

**Benefits**:
- Download coverage locally for analysis
- Compare coverage across runs
- Archive historical test results

### 3. Debug Workflows

```yaml
- name: Build fails? Upload debug info
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: debug-logs
    path: |
      logs/
      *.log
```

## Running Locally

```bash
cd 14-artifacts/react-app

# Install dependencies
npm install

# Run tests with coverage
npm test -- --coverage
# Creates: coverage/

# Build application
npm run build
# Creates: build/

# Check outputs
ls -la build/
ls -la coverage/
```

## Common Issues

### Artifact Not Found

**Problem**: "Unable to find artifact"

**Causes**:
1. **Typo in artifact name**:
   ```yaml
   # Upload
   name: my-app-build

   # Download (wrong!)
   name: my-app-built  # ✗ Typo
   ```

2. **Job failed before upload**:
   - Check if build job completed successfully
   - Upload step must have run

3. **Artifact expired** (90 days):
   - Re-run the workflow

### Path Not Found

**Problem**: "Path does not exist"

**Checks**:
```yaml
# ✓ Correct - path exists after build
path: build/

# ✗ Wrong - typo or wrong directory
path: dist/  # If build outputs to 'build/' not 'dist/'
```

**Debug**:
```yaml
- name: List directory
  run: ls -R

- name: Upload
  uses: actions/upload-artifact@v4
  with:
    path: build/  # Verify this path exists
```

### Large Artifact Size

**Problem**: "Artifact size exceeds limit"

**Limit**: 10 GB per artifact

**Solutions**:
```yaml
# ✓ Upload only necessary files
path: |
  build/**/*.js
  build/**/*.css
  build/**/*.html

# ✗ Don't upload everything
path: build/  # Includes source maps, tests, etc.
```

**Compress before upload**:
```yaml
- name: Compress build
  run: tar -czf build.tar.gz build/

- uses: actions/upload-artifact@v4
  with:
    path: build.tar.gz
```

## Best Practices

### 1. Use Descriptive Names

```yaml
# ✓ Good - includes context
name: production-build-${{ github.sha }}
name: test-coverage-${{ matrix.node-version }}

# ✗ Bad - generic
name: build
name: output
```

### 2. Set Appropriate Retention

```yaml
# Builds - shorter retention
- uses: actions/upload-artifact@v4
  with:
    name: build
    path: build/
    retention-days: 7  # 7 days instead of 90

# Important artifacts - longer retention
- uses: actions/upload-artifact@v4
  with:
    name: release-package
    path: dist/
    retention-days: 90  # Keep for 90 days
```

### 3. Upload Conditionally

```yaml
# Only upload on failure for debugging
- name: Upload logs
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: error-logs
    path: logs/

# Only upload on main branch
- name: Upload production build
  if: github.ref == 'refs/heads/main'
  uses: actions/upload-artifact@v4
  with:
    name: prod-build
    path: build/
```

### 4. Organize Multiple Artifacts

```yaml
# Pattern for multiple environments
- uses: actions/upload-artifact@v4
  with:
    name: ${{ matrix.env }}-build-${{ github.sha }}
    path: build/
```

Results in:
```
staging-build-abc123
production-build-abc123
```

## Performance Considerations

### Upload/Download Times

**Typical times**:
- Upload 100 MB: ~20-30 seconds
- Download 100 MB: ~15-25 seconds
- Compression/decompression: ~5-10 seconds

### Optimization

```yaml
# Exclude unnecessary files
path: |
  build/**/*.js
  build/**/*.css
  !build/**/*.map  # Exclude source maps
```

## Next Steps

After mastering artifacts:

1. **Lesson 15: Matrices** - Upload artifacts for multiple configurations
2. **Lesson 16: Environments** - Deploy artifacts to different environments
3. **Combine with caching** - Cache dependencies, upload build artifacts

## Related Resources

- **Workflow**: [14-artifacts.yaml](../.github/workflows/14-artifacts.yaml)
- **actions/upload-artifact**: [GitHub Marketplace](https://github.com/marketplace/actions/upload-a-build-artifact)
- **actions/download-artifact**: [GitHub Marketplace](https://github.com/marketplace/actions/download-a-build-artifact)
- **GitHub Docs**: [Storing Workflow Data](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)

## Exercise

Try these experiments:

1. **Download artifacts**: After running the workflow, download both artifacts from the UI
2. **Add a third job**: Create a `test-coverage-report` job that downloads coverage and generates a report
3. **Upload on failure**: Add a step that uploads logs only when tests fail
4. **Change retention**: Set test coverage to expire after 7 days

---

**← Previous**: [13 - Caching](../13-caching/) | **Next**: [17 - Custom Actions](../17-custom-actions/) →
