from binarytree.models import UserRank
from signalbot.models import ReferalWallet, ReferalIncome, ReferalWithdrawlHistory
from user.models import User


def all_in_one(user, reffered_by, refered_user, m_amount):
    print("hello")
    print(m_amount)
    try:
        wallet = ReferalWallet.objects.get(user=user)
    except:
        wallet = ReferalWallet.objects.create(user=user, amount=0)

    wallet.amount = wallet.amount + m_amount
    wallet.save()
    ReferalIncome.objects.create(
        refered_by=reffered_by,
        refered_user=refered_user,
        money_allocated_to=user,
        amount=m_amount,
    )


def calculate_commission(ancestors, amount, reffered_by, refered_user):
    membership_amount = amount
    level = len(ancestors)
    for ancestor in ancestors:
        user = User.objects.get(id=ancestor.user.id)
        rank = UserRank.objects.get(user=user).rank.name
        print("user :", user)
        print("rank :", rank)
        print("level :", level)

        if level == 1:
            print(f"commision {membership_amount*0.5}")
            m_amount = membership_amount * 0.5
            print(m_amount)
            all_in_one(
                user=user,
                reffered_by=reffered_by,
                refered_user=refered_user,
                m_amount=m_amount,
            )
        elif (
            level == 2
            and rank == "Bronze"
            or rank == "Silver"
            or rank == "Gold"
            or rank == "Platinum"
            or rank == "Diamond"
        ):
            print(f"commision {membership_amount*0.1}")
            m_amount = membership_amount * 0.1
            all_in_one(
                user=user,
                reffered_by=reffered_by,
                refered_user=refered_user,
                m_amount=m_amount,
            )
        elif (
            level == 3
            or level == 4
            and rank == "Silver"
            or rank == "Gold"
            or rank == "Platinum"
            or rank == "Diamond"
        ):
            print(f"commision {membership_amount*0.05}")
            m_amount = membership_amount * 0.05
            all_in_one(
                user=user,
                reffered_by=reffered_by,
                refered_user=refered_user,
                m_amount=m_amount,
            )
        elif level == 5 and rank == "Platinum" or rank == "Diamond" or rank == "Gold":
            print(f"commision {membership_amount*0.03}")
            m_amount = membership_amount * 0.3
            all_in_one(
                user=user,
                reffered_by=reffered_by,
                refered_user=refered_user,
                m_amount=m_amount,
            )
        elif level == 6 and rank == "Platinum" or rank == "Diamond" or rank == "Gold":
            print(f"commision {membership_amount*0.02}")
            m_amount = membership_amount * 0.2
            all_in_one(
                user=user,
                reffered_by=reffered_by,
                refered_user=refered_user,
                m_amount=m_amount,
            )
        elif level == 7 and rank == "Platinum" or rank == "Diamond":
            print(f"commision {membership_amount*0.02}")
            m_amount = membership_amount * 0.02
            all_in_one(
                user=user,
                reffered_by=reffered_by,
                refered_user=refered_user,
                amom_amountunt=m_amount,
            )
        elif level == 8 and rank == "Platinum" or rank == "Diamond":
            print(f"commision {membership_amount*0.01}")
            m_amount = membership_amount * 0.01
            all_in_one(
                user=user,
                reffered_by=reffered_by,
                refered_user=refered_user,
                m_amount=m_amount,
            )
        elif level == 9 or level == 10 and rank == "Diamond":
            print(f"commision {membership_amount*0.01}")
            m_amount = membership_amount * 0.01
            all_in_one(
                user=user,
                reffered_by=reffered_by,
                refered_user=refered_user,
                m_amount=m_amount,
            )
        else:
            print("no commisions")
        level = level - 1
