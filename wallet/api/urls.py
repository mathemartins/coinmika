from django.urls import path

from wallet.api.views import (
    WalletCreate
)

urlpatterns = [
    path('create/', WalletCreate.as_view(), name="create-wallet")
]