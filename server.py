from typing import Annotated

import boto3
from fastmcp import FastMCP
from pydantic import Field

mcp: FastMCP = FastMCP(
    name="CodeCommit Tools",
    instructions="""
    Tools for managing AWS CodeCommit repositories and pull requests.
    you can use these tools to:
    - List repositories with `codecommitListRepositories(filterString: str)`.
    - Create a pull request with `codecommitCreatePullRequest(repository_name: str, source_branch: str, destination_branch: str, title: str, description: str)`.
    """,
)
client = boto3.client("codecommit")


@mcp.tool(name="codecommitListRepositories", description="List CodeCommit repositories", tags={"codecommit"})
def list_repositories(
    filterString: Annotated[
        str,
        Field(description="Filter string for repository names"),
    ],
) -> list[str]:
    response = client.list_repositories()
    if "repositories" not in response:
        return []
    if not filterString:
        return [repo["repositoryName"] for repo in response["repositories"]]
    # Filter repositories by the provided filterString
    return [
        repo["repositoryName"]
        for repo in response["repositories"]
        if filterString.lower() in repo["repositoryName"].lower()
    ]


@mcp.tool(
    name="codecommitCreatePullRequest",
    description="Create a pull request in a CodeCommit repository",
    tags={"codecommit"},
)
def create_pull_request(
    repository_name: Annotated[
        str,
        Field(description="Name of the repository to create the pull request in"),
    ],
    source_branch: Annotated[str, Field(description="Name of the source branch")],
    destination_branch: Annotated[
        str,
        Field(description="Name of the destination branch"),
    ],
    title: Annotated[str, Field(description="Title of the pull request")],
    description: Annotated[str, Field(description="Description of the pull request")],
) -> str:
    response = client.create_pull_request(
        title=title,
        description=description,
        targets=[
            {
                "repositoryName": repository_name,
                "sourceReference": source_branch,
                "destinationReference": destination_branch,
            },
        ],
    )
    return response["pullRequest"]


@mcp.tool(
    name="codecommitGetPullRequest",
    description="Get details of a pull request in a CodeCommit repository",
    tags={"codecommit"},
)
def get_pull_request(
    pull_request_id: Annotated[str, Field(description="ID of the pull request")],
) -> dict:
    response = client.get_pull_request(pullRequestId=pull_request_id)
    return response["pullRequest"]


if __name__ == "__main__":
    mcp.run(transport="stdio")
