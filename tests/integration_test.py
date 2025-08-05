#
# Copyright (C) 2025 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
Integration tests. They need a valid .env at the root of the
project with credentials to access the DCI CS.
"""

import datetime
import json

import pytest
from fastmcp import Client

from mcp_server.main import create_server


@pytest.fixture
def mcp_server():
    server = create_server()
    return server


def parse_response(result):
    """Helper function to parse MCP tool response."""
    if result.content and len(result.content) > 0:
        content_text = result.content[0].text
        return json.loads(content_text)
    else:
        pytest.fail("No content returned from tool")


async def test_date(mcp_server):
    """Test date-related tools."""
    async with Client(mcp_server) as client:
        # Test today tool
        result = await client.call_tool("today", {})
        assert not result.is_error

        data = parse_response(result)
        assert "today" in data and data["today"] == datetime.date.today().strftime(
            "%Y-%m-%d"
        )


@pytest.mark.integration
async def test_team(mcp_server):
    """Test team-related tools."""
    async with Client(mcp_server) as client:
        # Test query_dci_teams
        result = await client.call_tool("query_dci_teams", {"query": "like(name,DCI)"})
        assert not result.is_error

        data = parse_response(result)
        assert "teams" in data or "error" in data


@pytest.mark.integration
async def test_job_tools(mcp_server):
    """Test job-related tools."""
    async with Client(mcp_server) as client:
        # Test list_dci_jobs with a simple filter (no limit parameter)
        result = await client.call_tool(
            "query_dci_jobs",
            {"query": "contains(tags,daily)", "only_fields": ["team_id"]},
        )
        assert not result.is_error

        data = parse_response(result)
        assert "jobs" in data and len(data["jobs"]) > 0


@pytest.mark.integration
async def test_component_tools(mcp_server):
    """Test component-related tools."""
    async with Client(mcp_server) as client:
        # Test query_dci_components
        result = await client.call_tool(
            "query_dci_components", {"query": "like(name,%)"}
        )
        assert not result.is_error

        data = parse_response(result)
        assert "components" in data or "error" in data

        # Test query_dci_components with a specific component query
        result = await client.call_tool(
            "query_dci_components", {"query": "eq(id,dummy-id)"}
        )
        assert not result.is_error

        data = parse_response(result)
        # Should return empty results or error/message, both are valid
        assert "components" in data or "error" in data or "message" in data


@pytest.mark.integration
async def test_file_tools(mcp_server):
    """Test file-related tools."""
    async with Client(mcp_server) as client:
        # Test query_dci_files
        result = await client.call_tool("query_dci_files", {"query": "like(name,%)"})
        assert not result.is_error

        data = parse_response(result)
        assert "files" in data or "error" in data


@pytest.mark.integration
async def test_pipeline_tools(mcp_server):
    """Test pipeline-related tools."""
    async with Client(mcp_server) as client:
        # Test query_dci_pipelines
        result = await client.call_tool(
            "query_dci_pipelines", {"query": "like(name,%)"}
        )
        assert not result.is_error

        data = parse_response(result)
        assert "pipelines" in data or "error" in data


@pytest.mark.integration
async def test_product_tools(mcp_server):
    """Test product-related tools."""
    async with Client(mcp_server) as client:
        # Test query_dci_products
        result = await client.call_tool("query_dci_products", {"query": "like(name,%)"})
        assert not result.is_error

        data = parse_response(result)
        assert "products" in data or "error" in data


@pytest.mark.integration
async def test_topic_tools(mcp_server):
    """Test topic-related tools."""
    async with Client(mcp_server) as client:
        # Test query_dci_topics
        result = await client.call_tool(
            "query_dci_topics", {"query": "like(name,OCP-%)"}
        )
        assert not result.is_error

        data = parse_response(result)
        assert "topics" in data and len(data["topics"]) > 0


@pytest.mark.integration
async def test_pr_tools(mcp_server):
    """Test PR-related tools."""
    async with Client(mcp_server) as client:
        # Test get_latest_dci_job_for_pr with dummy data
        result = await client.call_tool(
            "get_latest_dci_job_for_pr",
            {
                "pr_url": "https://github.com/my-org/my-repo/pull/42",
                "job_name": "test-job",
            },
        )
        assert not result.is_error

        data = parse_response(result)
        # This might return empty results or error, both are valid
        assert isinstance(data, dict) and "jobs" in data and len(data["jobs"]) == 0


@pytest.mark.integration
async def test_job_file_tools(mcp_server):
    """Test job file and result tools."""
    async with Client(mcp_server) as client:
        # Test list_job_files with a dummy job ID (returns empty list, not error)
        result = await client.call_tool("list_job_files", {"job_id": "dummy-job-id"})
        assert not result.is_error

        data = parse_response(result)
        assert "job_id" in data and "files" in data

        # Test list_job_results with a dummy job ID (returns empty list, not error)
        result = await client.call_tool("list_job_results", {"job_id": "dummy-job-id"})
        assert not result.is_error

        data = parse_response(result)
        assert "job_id" in data and "results" in data


@pytest.mark.integration
async def test_file_download_tools(mcp_server):
    """Test file download and content tools."""
    async with Client(mcp_server) as client:
        # Test download_dci_file with a dummy file ID (returns error structure)
        result = await client.call_tool(
            "download_dci_file",
            {
                "job_id": "dummy-job-id",
                "file_id": "dummy-file-id",
                "output_path": "/tmp/test",
            },
        )
        assert not result.is_error

        data = parse_response(result)
        assert "file_id" in data and ("content" in data or "error" in data)

        # Test get_file_content with a dummy file ID (returns error structure)
        result = await client.call_tool(
            "get_file_content", {"file_id": "dummy-file-id"}
        )
        assert not result.is_error

        data = parse_response(result)
        assert "file_id" in data and ("content" in data or "error" in data)


@pytest.mark.integration
async def test_pipeline_job_tools(mcp_server):
    """Test pipeline job tools."""
    async with Client(mcp_server) as client:
        # Test get_pipeline_jobs with a dummy pipeline ID (returns empty list, not
        # error)
        result = await client.call_tool(
            "get_pipeline_jobs", {"pipeline_id": "dummy-pipeline-id"}
        )
        assert not result.is_error

        data = parse_response(result)
        assert "pipeline_id" in data and "jobs" in data


@pytest.mark.integration
async def test_remoteci_tools(mcp_server):
    """Test remoteci-related tools."""
    async with Client(mcp_server) as client:
        # Test query_dci_remotecis
        result = await client.call_tool(
            "query_dci_remotecis", {"query": "like(name,%)"}
        )
        assert not result.is_error

        data = parse_response(result)
        assert "remotecis" in data or "error" in data


@pytest.mark.integration
async def test_product_team_tools(mcp_server):
    """Test product team tools."""
    async with Client(mcp_server) as client:
        # Test get_product_teams with a dummy product ID (returns empty list, not error)
        result = await client.call_tool(
            "get_product_teams", {"product_id": "dummy-product-id"}
        )
        assert not result.is_error

        data = parse_response(result)
        assert "product_id" in data and "teams" in data


@pytest.mark.integration
async def test_error_handling(mcp_server):
    """Test error handling for invalid tool calls."""
    async with Client(mcp_server) as client:
        # Test calling a tool with valid parameters but expecting graceful handling
        result = await client.call_tool("query_dci_teams", {"query": "like(name,%)"})
        assert not result.is_error  # Should handle gracefully

        data = parse_response(result)
        assert "teams" in data or "error" in data
