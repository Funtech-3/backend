"""Ticket application of Events backend URL Configuration."""

from django.urls import include, path

from rest_framework import routers

from tickets.views import UserTicketViewSet


# ticket_router = routers.DefaultRouter()


# urlpatterns = [
#     path('', include(ticket_router.urls)),
# ]
