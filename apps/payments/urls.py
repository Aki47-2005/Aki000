from django.urls import path

from . import views

urlpatterns = [
    path("submit/", views.submit_payment, name="submit_payment"),
    path("queue/", views.payment_queue, name="payment_queue"),
    path("<int:pk>/<str:decision>/", views.decide_payment, name="decide_payment"),
    path("clearance/", views.clearance_queue, name="clearance_queue"),
    path("clearance/<int:pk>/<str:decision>/", views.decide_clearance, name="decide_clearance"),
]
