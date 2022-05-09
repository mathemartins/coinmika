from django.urls import path

from wallet.api.views import (
    WalletCreate, WalletRestore, ListWallets
)

urlpatterns = [
    path('create/', WalletCreate.as_view(), name="create-wallet"),
    path('restore/', WalletRestore.as_view(), name="restore-wallet"),
    path('list/', ListWallets.as_view(), name="list-wallet"),
]