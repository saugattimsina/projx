from ..models import UserWalletAddress
from ..services.fetch_balance import get_address_balance


def check_user_wallet_address():
    walletaddress = UserWalletAddress.objects.filter(is_completed=False)
    for address in walletaddress:
        get_address_balance(
            address=address.wallet_address,
            user=address.user,
            subcription=address.subscription,
        )
