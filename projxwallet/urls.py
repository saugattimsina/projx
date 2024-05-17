from django.urls import path

from .apiview import (
    WithdrawProjxWallet,
    DepositProjxWallet,
    FetchProjxWalletBalanceView,
)

urlpatterns = [
    path(
        "fetch/balance/",
        FetchProjxWalletBalanceView.as_view(),
        name="fetch_wallet_balance",
    ),
    path(
        "deposit/",
        DepositProjxWallet.as_view(),
        name="deposit_wallet",
    ),
    path(
        "withdraw/",
        WithdrawProjxWallet.as_view(),
        name="withdraw_wallet",
    ),
]
