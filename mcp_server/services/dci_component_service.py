"""DCI component service for managing components."""

import sys
from typing import Any

from dciclient.v1.api import component

from .dci_base_service import DCIBaseService


class DCIComponentService(DCIBaseService):
    """Service class for DCI component operations."""

    def get_component(self, component_id: str) -> Any:
        """
        Get a specific component by ID.

        Args:
            component_id: The ID of the component to retrieve

        Returns:
            Component data as dictionary, or None if not found
        """
        try:
            context = self._get_dci_context()
            result = component.get(context, component_id)
            if hasattr(result, "json"):
                return result.json()
            return result
        except Exception as e:
            print(f"Error getting component {component_id}: {e}")
            return None

    def query_components(
        self,
        query: str,
        limit: int = 50,
        offset: int = 0,
        sort: str | None = None,
    ) -> list:
        """
        List components using the advanced query syntax.

        Args:
            query: query criteria (e.g., "and(ilike(name,ocp),contains(tags,ga))")
            limit: Maximum number of components to return (default: 50)
            offset: Number of components to skip (default: 0)
            sort: Sort criteria (e.g., "-created_at")

        Returns:
            A dictionary with components data or an empty dictionary on error
        """
        try:
            context = self._get_dci_context()
            # Use the base.list method which is available
            result = component.base.list(
                context,
                component.RESOURCE,
                limit=limit,
                offset=offset,
                query=query,
                sort=sort,
            )
            if hasattr(result, "json"):
                return result.json()
            return result
        except Exception as e:
            print(f"Error listing components: {e}", file=sys.stderr)
            import traceback

            traceback.print_exc()
            return {"error": str(e), "message": "Failed to list components."}

    def list_components(
        self,
        limit: int | None = None,
        offset: int | None = None,
        where: str | None = None,
        sort: str | None = None,
    ) -> list:
        """
        List components with optional filtering and pagination.

        Args:
            limit: Maximum number of components to return
            offset: Number of components to skip
            where: Filter criteria (e.g., "name:like:test")
            sort: Sort criteria (e.g., "name:asc")

        Returns:
            List of component dictionaries
        """
        try:
            context = self._get_dci_context()
            # Provide default values for required parameters
            if limit is None:
                limit = 50
            if offset is None:
                offset = 0

            result = component.base.list(
                context,
                component.RESOURCE,
                limit=limit,
                offset=offset,
                where=where,
                sort=sort,
            )
            if hasattr(result, "json"):
                data = result.json()
                return data.get("components", []) if isinstance(data, dict) else []
            return result if isinstance(result, list) else []
        except Exception as e:
            print(f"Error listing components: {e}")
            return []
