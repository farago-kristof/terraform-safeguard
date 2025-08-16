# Terraform Safeguard

A Docker wrapper for Terraform that adds AWS account validation and safety checks.

## Features

- ✅ AWS account validation before Terraform operations
- ✅ Interactive confirmation prompts
- ✅ Multi-profile AWS support
- ✅ Automated image building for new Terraform releases

## Quick Start

```bash
# Pull and run
docker pull ghcr.io/[your-username]/terraform-safeguard:latest

# Use with your Terraform code
docker run -it --rm \
  -e AWS_PROFILE_NAME=production \
  -v ~/.aws:/root/.aws \
  -v $(pwd):/workspace \
  -w /workspace \
  ghcr.io/[your-username]/terraform-safeguard:1.5.0 \
  plan
```

## How It Works

1. Validates AWS credentials and account
2. Prompts for confirmation before operations
3. Executes Terraform with all safety checks passed

## Configuration

Set `AWS_PROFILE_NAME` environment variable and optionally create `/tmp/aws_caller_identity` with expected account ID for validation.

## Building

```bash
# Build locally
python3 scripts/build_image.py hashicorp/terraform:1.5.0 -t my-terraform:1.5.0

# Build and push
python3 scripts/build_image.py hashicorp/terraform:latest -t my-terraform:latest --push
```

## Automated Builds

GitHub Actions automatically:
- Checks for new Terraform releases every 6 hours
- Builds and pushes new images when detected
- Tags with version numbers (e.g., `terraform-safeguard:1.5.0`, `terraform-safeguard:tf-1.5.0`)

## License

MIT License
