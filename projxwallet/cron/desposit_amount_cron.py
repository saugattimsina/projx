from ..models import ProjxWalletHistory

from ..services.deposit_amount import deposit_amount_address


def deposit_amount_in_address():
    projx_historys = ProjxWalletHistory.objects.filter(
        status=ProjxWalletHistory.STATUS_CHOICES.PENDING,
        transaction_type=ProjxWalletHistory.TRANSACTION_TYPE.DEPOSIT,
    )
    for projx_history in projx_historys:
        deposit_amount_address(
            address=projx_history.wallet_address, projx_wallet_history_obj=projx_history
        )
