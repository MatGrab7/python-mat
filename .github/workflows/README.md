# CI Pipeline Configuration

This directory contains GitHub Actions workflows for automated code quality and security scanning.

## Workflow: Code Quality and Secrets Scan

The workflow runs on every push to `main` and `develop` branches and includes three jobs:

### 1. **Code Quality Checks**
- **Pylint**: Python linting for common errors and code issues
- **Flake8**: Style guide enforcement and error detection
- **Black**: Code formatting verification
- **SonarQube**: Advanced code quality analysis (optional - requires setup)

### 2. **Secrets Detection**
- **TruffleHog**: Scans for secrets, API keys, tokens in your repository
- **detect-secrets**: Additional secrets detection using pattern matching

### 3. **GitHub Native Scanning**
- **CodeQL**: GitHub's native security analysis tool for Python code

## Setup Instructions

### Basic Setup (No Additional Configuration)
The workflow works out-of-the-box for code quality and secrets scanning using TruffleHog and GitHub's native tools.

### Optional: SonarQube Setup
If you want to enable SonarQube analysis:

1. Sign up at [SonarCloud](https://sonarcloud.io) (free for public repositories)
2. Create a new organization and project
3. Add these secrets to your GitHub repository:
   - `SONAR_HOST_URL`: Your SonarQube server URL (or `https://sonarcloud.io` for SonarCloud)
   - `SONAR_TOKEN`: Your authentication token

**To add secrets:**
1. Go to Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add the above values

### Optional: .sonarcloud.properties
Create a `.sonarcloud.properties` file in your repo root for SonarQube configuration:
```properties
sonar.projectKey=your-project-key
sonar.organization=your-org-name
```

## How to Use

1. **Push code to your repository**: The workflow automatically triggers on every commit to `main` or `develop`
2. **View results**: 
   - Go to the "Actions" tab in your GitHub repository
   - Click on the workflow run to see detailed logs
   - Security and Code Scanning alerts appear in the "Security" tab

## Customization

### Disable Specific Checks
Edit `.github/workflows/code-quality-and-secrets-scan.yml` and remove or modify jobs as needed.

### Add More Tools
You can extend the workflow to include:
- Bandit (Python security scanner)
- Safety (Python dependency vulnerability scanner)
- OWASP Dependency-Check
- Custom linting rules

### Change Trigger Events
Modify the `on:` section to trigger on different events:
```yaml
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly scan
```

## Workflow Status Indicators

All checks are set to `continue-on-error: true` to prevent pipeline failure while still reporting issues. This allows PRs to be merged even if warnings are found, but you'll see the results in GitHub's interface.

To make checks fail the workflow, remove `continue-on-error: true` from specific steps.

## Troubleshooting

- **TruffleHog errors**: Update the branch references if your default branch isn't `main`
- **Python path issues**: Ensure all Python files are in the repo root or adjust the `pylint` and `flake8` paths
- **CodeQL timeout**: Large repositories may need increased timeout or can exclude specific paths

## References

- [TruffleHog Documentation](https://github.com/trufflesecurity/trufflehog)
- [CodeQL Documentation](https://codeql.github.com/)
- [SonarQube Documentation](https://docs.sonarqube.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
