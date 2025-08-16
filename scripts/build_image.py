#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

def push_to_github_registry(image_tag: str) -> bool:
    """Push the built image to GitHub Container Registry.

    Args:
        image_tag: The image tag to push

    Returns:
        bool: True if push successful, False otherwise
    """
    try:
        # Tag for GitHub Container Registry
        gh_tag = f"ghcr.io/{image_tag}"

        print(f"Tagging image for GitHub Container Registry: {gh_tag}")
        tag_cmd = ["docker", "tag", image_tag, gh_tag]
        subprocess.run(tag_cmd, check=True, capture_output=True, text=True)

        print(f"Pushing to GitHub Container Registry: {gh_tag}")
        push_cmd = ["docker", "push", gh_tag]
        subprocess.run(push_cmd, check=True, capture_output=True, text=True)

        print(f"Successfully pushed: {gh_tag}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Push failed with exit code {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def build_docker_image(base_tag: str, output_tags: list[str], push: bool = False) -> bool:
    """Build a Docker image with custom entrypoint using the specified Terraform base image.

    Args:
        base_tag: The base Terraform image tag (e.g., 'hashicorp/terraform:1.5.0')
        output_tags: List of output image tags
        push: Whether to push the image to GitHub Container Registry

    Returns:
        bool: True if build successful, False otherwise
    """
    if not output_tags:
        print("Error: No output tags specified")
        return False

    # Get the directory containing this script
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docker_dir = project_root / "docker"
    dockerfile_path = docker_dir / "Dockerfile"

    if not dockerfile_path.exists():
        print(f"Error: Dockerfile not found at {dockerfile_path}")
        return False

    print(f"Building Docker image with base: {base_tag}")
    print(f"Output tags: {', '.join(output_tags)}")
    print(f"Docker context: {docker_dir}")

    try:
        # Build the Docker image with first tag
        cmd = [
            "docker", "build",
            "--build-arg", f"BASE_IMAGE={base_tag}",
            "-t", output_tags[0],
            "-f", str(dockerfile_path),
            str(docker_dir)
        ]

        # Add additional tags
        for tag in output_tags[1:]:
            cmd.extend(["-t", tag])

        print(f"Executing: {' '.join(cmd)}")
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        print("Build successful!")
        print(f"Image tagged as: {', '.join(output_tags)}")

        # Push to GitHub Container Registry if requested
        if push:
            success = True
            for tag in output_tags:
                if not push_to_github_registry(tag):
                    success = False
            return success

        return True

    except subprocess.CalledProcessError as e:
        print(f"Docker build failed with exit code {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: Docker command not found. Please ensure Docker is installed and in PATH.")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Build a custom Terraform Docker image with safeguard entrypoint"
    )
    parser.add_argument(
        "base_tag",
        help="Base Terraform image tag (e.g., 'hashicorp/terraform:1.5.0')"
    )
    parser.add_argument(
        "-t", "--tag",
        dest="output_tags",
        action="append",
        required=True,
        help="Output image tag (can be specified multiple times or as comma-separated list)"
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push the built image to GitHub Container Registry"
    )

    args = parser.parse_args()

    # Handle comma-separated tags within each -t argument
    all_tags = []
    for tag_arg in args.output_tags:
        # Split by comma and strip whitespace
        tags = [tag.strip() for tag in tag_arg.split(',')]
        all_tags.extend(tags)

    success = build_docker_image(args.base_tag, all_tags, args.push)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
