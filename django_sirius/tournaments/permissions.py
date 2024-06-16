"""Custom permissions for the tournaments app."""
from typing import Any

from django.http import HttpRequest
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView


class UserAdminPermission(BasePermission):
    """Permission for user admin."""

    _safe_methods = ['GET', 'HEAD', 'OPTIONS']

    def has_permission(self, request: HttpRequest, view: APIView) -> bool:
        """Check if the user has permission.

        Args:
            request (HttpRequest): The incoming HTTP request.
            view (APIView): The view which is being accessed.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        # Allow all requests from authenticated users
        return request.user.is_authenticated

    def has_object_permission(
        self,
        request: HttpRequest,
        view: APIView,
        just_obj: Any,
    ) -> bool:
        """Check if the user has permission to access or manipulate the object.

        Args:
            request (HttpRequest): The incoming HTTP request.
            view (APIView): The view which is being accessed.
            just_obj (Any): The object that the user wants to \
                access or manipulate.

        Returns:
            bool: True if the request method is safe \
                or the user is the owner of the object or an admin,\
                    False otherwise.
        """
        # Allow safe methods to all
        if request.method in self._safe_methods:
            return True
        # Allow requests from the object's owner or an admin
        return just_obj.owner == request.user or request.user.is_staff
