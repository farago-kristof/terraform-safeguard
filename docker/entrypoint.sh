#!/bin/bash
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== AWS Account Configuration ===${NC}"
echo "AWS Profile: ${AWS_PROFILE_NAME}"
echo "Environment File: .env.${AWS_PROFILE_NAME}"
echo "Caller Identity File: /tmp/aws_caller_identity.${AWS_PROFILE_NAME}"

# Check if caller identity file exists
if [ -f "/tmp/aws_caller_identity" ]; then
    echo -e "${GREEN}✓${NC} Caller identity file found"
    echo "Expected caller identity:"
    cat /tmp/aws_caller_identity
    echo ""  # Add newline after displaying file content
else
    echo -e "${RED}✗${NC} Caller identity file not found"
fi

# Test AWS credentials by getting caller identity
echo "Checking AWS identity..."
if CURRENT_ACCOUNT=$(aws sts get-caller-identity --output text --query 'Account' 2>/dev/null); then
    echo -e "${GREEN}✓${NC} AWS credentials are valid"
    echo "Current AWS Account: ${CURRENT_ACCOUNT}"

    # Compare with expected if file exists
    if [ -f "/tmp/aws_caller_identity" ]; then
        EXPECTED_ACCOUNT=$(cat /tmp/aws_caller_identity)
        if [ "${CURRENT_ACCOUNT}" = "${EXPECTED_ACCOUNT}" ]; then
            echo -e "${GREEN}✓${NC} Account matches expected: ${EXPECTED_ACCOUNT}"
        else
            echo -e "${RED}✗${NC} Account mismatch! Expected: ${EXPECTED_ACCOUNT}, Got: ${CURRENT_ACCOUNT}"
            exit 1
        fi
    fi
else
    echo -e "${RED}✗${NC} AWS credentials are invalid or insufficient"
    exit 1
fi

echo -e "${GREEN}=== Ready for Terraform operations ===${NC}"
echo ""

# Ask for confirmation before proceeding
echo -e "${YELLOW}Proceed with Terraform operations on account ${CURRENT_ACCOUNT} (profile: ${AWS_PROFILE_NAME})? (yes/no):${NC}"
read -r CONFIRMATION

if [ "$CONFIRMATION" = "yes" ] || [ "$CONFIRMATION" = "y" ]; then
    echo -e "${GREEN}✓${NC} Proceeding with Terraform operations"
    echo ""
elif [ "$CONFIRMATION" = "no" ] || [ "$CONFIRMATION" = "n" ]; then
    echo -e "${YELLOW}Operation cancelled by user${NC}"
    exit 0
else
    echo -e "${RED}✗${NC} Invalid response. Please answer 'yes' or 'no'"
    exit 1
fi

echo -e "${GREEN}Profile: ${AWS_PROFILE_NAME}${NC}"
# Execute terraform with all passed arguments, or start an interactive shell
if [ $# -eq 0 ]; then
    exec /bin/bash
else
    exec terraform "$@"
fi