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

"""DCI file service for managing files."""

import os
import sys
from typing import Any

from dciclient.v1.api import file as dci_file

from .dci_base_service import DCIBaseService


class DCIFileService(DCIBaseService):
    """Service class for DCI file operations."""

    def get_file(self, file_id: str) -> Any:
        """
        Get a specific file by ID.

        Args:
            file_id: The ID of the file to retrieve

        Returns:
            File data as dictionary, or None if not found
        """
        try:
            context = self._get_dci_context()
            result = dci_file.get(context, file_id)
            if hasattr(result, "json"):
                return result.json()
            return result
        except Exception as e:
            print(f"Error getting file {file_id}: {e}")
            return None

    def query_files(
        self,
        query: str,
        limit: int = 50,
        offset: int = 0,
        sort: str | None = None,
    ) -> list:
        """
        List files using the advanced query syntax.

        Args:
            query: query criteria (e.g., "and(ilike(name,ansible),contains(tags,ga))")
            limit: Maximum number of files to return (default: 50)
            offset: Number of files to skip (default: 0)
            sort: Sort criteria (e.g., "-created_at")

        Returns:
            A dictionary with files data or an empty dictionary on error
        """
        try:
            context = self._get_dci_context()
            return dci_file.list(
                context, query=query, limit=limit, offset=offset, sort=sort
            ).json()
        except Exception as e:
            print(f"Error listing files: {e}", file=sys.stderr)
            import traceback

            traceback.print_exc()
            return {"error": str(e), "message": "Failed to list files."}

    def list_files(
        self,
        limit: int | None = None,
        offset: int | None = None,
        where: str | None = None,
        sort: str | None = None,
    ) -> list:
        """
        List files with optional filtering and pagination.

        Args:
            limit: Maximum number of files to return
            offset: Number of files to skip
            where: Filter criteria (e.g., "name:ansible.log")
            sort: Sort criteria (e.g., "-created_at")

        Returns:
            List of file dictionaries
        """
        try:
            context = self._get_dci_context()
            # Provide default values for required parameters
            if limit is None:
                limit = 50
            if offset is None:
                offset = 0

            result = dci_file.list(
                context, limit=limit, offset=offset, where=where, sort=sort
            )
            if hasattr(result, "json"):
                data = result.json()
                return data.get("files", []) if isinstance(data, dict) else []
            return result if isinstance(result, list) else []
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    def download_file(self, job_id: str, file_id: str, output_path: str) -> bool:
        """
        Download a file to a local path.

        Args:
            job_id: The ID of the job associated with the file
            file_id: The ID of the file to download
            output_path: Local path where to save the file

        Returns:
            True if download successful, False otherwise
        """
        try:
            context = self._get_dci_context()

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Download the file
            res = dci_file.download(context, job_id, file_id, output_path)
            print(f"{res=}")
            return True
        except Exception as e:
            print(f"Error downloading file {file_id} to {output_path}: {e}")
            return False

    def get_file_content(self, file_id: str) -> Any:
        """
        Get the content of a file as a string.

        Args:
            file_id: The ID of the file

        Returns:
            File content as string, or None if error
        """
        try:
            context = self._get_dci_context()
            result = dci_file.content(context, file_id)
            if hasattr(result, "text"):
                return result.text
            return str(result) if result is not None else None
        except Exception as e:
            print(f"Error getting content for file {file_id}: {e}")
            return None
