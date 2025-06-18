# CodeCommit MCP

Model Context Protocol (MCP) server for AWS CodeCommit operations.

## Requirements

- Python 3.13 or higher
- AWS credentials (IAM user access key and secret key, or IAM role)
- Access permissions to AWS CodeCommit

## Installation

After cloning the project, you can install it in development mode with the following command:

```bash
uv sync -e .
```

If you don't have the uv (Ultrafast Virtualenv) package manager installed, you can get it from the [uv official site](https://github.com/astral-sh/uv).

## How to Run

### Standard Input/Output Mode (stdio)

Using uv:

```bash
uv run server.py
```
s
This server runs in standard input/output (stdio) mode by default. MCP requests and responses are exchanged through standard input/output. This is convenient for integration with IDEs like VS Code or CLI tools.

### Environment Configuration

#### Using IAM User Credentials

AWS credentials can be specified using environment variables or configuration files:

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=your_region
```

#### Using AWS IAM Identity Center (SSO)

This tool also supports authentication using AWS IAM Identity Center (formerly AWS SSO). You can set it up with the following steps:

1. Make sure your AWS CLI configuration is complete:

```bash
aws configure sso
```

2. To run using a profile (e.g., the `default` profile):

```bash
export AWS_PROFILE=default
```

3. Or you can obtain SSO credentials before running with:

```bash
aws sso login --profile your-sso-profile
```

SSO credentials are automatically used based on the profile configured in ~/.aws/config. The boto3 library handles this authentication flow automatically.

## Available Tools

- **codecommitListRepositories**: Retrieve a list of CodeCommit repositories
  - Parameters:
    - `filterString`: Filter string for repository names (optional)
  - Return value: Array of repository names

- **codecommitCreatePullRequest**: Create a pull request in a CodeCommit repository
  - Parameters:
    - `repository_name`: Name of the repository to create the pull request in
    - `source_branch`: Name of the source branch
    - `destination_branch`: Name of the destination branch
    - `title`: Title of the pull request
    - `description`: Description of the pull request
  - Return value: Information about the created pull request

- **codecommitGetPullRequest**: Get details of a pull request in a CodeCommit repository
  - Parameters:
    - `pull_request_id`: ID of the pull request
  - Return value: Detailed information about the specified pull request

## Integration with VS Code

You can easily integrate this MCP server with IDEs and AI assistants that support the Model Context Protocol.

### VS Code Configuration

To configure this MCP server in VS Code, you can add the following to your `.vscode/settings.json` file:

```json
{
  "mcp": {
    "servers": {
      "codecommit": {
        "cwd": "${workspaceFolder}",
        "command": "uv",
        "args": ["run", "server.py"],
        "env": {
          "AWS_PROFILE": "your-profile",
          "AWS_REGION": "us-west-2"
        }
      }
    }
  }
}
```

Make sure to adjust the configuration based on your specific environment and requirements.
