# Unranked	Bronze	Silver	Gold	Platinum	Diamond
from binarytree.models import UserRank, BinaryParents
from signalbot.models import Binawallet, BinaryIncome
from datetime import date


def calculate_matrix_commission(user, amount):
    rank = UserRank.objects.get(user=user).rank.equivalent_name
    binary_parent = BinaryParents.objects.get(user=user)
    if rank == "Unranked":
        for parent in binary_parent.parents.all().order_by("-id")[:12]:
            wallet = Binawallet.objects.filter(user=parent.name).first()
            if not wallet:
                wallet = Binawallet.objects.create(user=parent.name, amount=0)
            c_amount = amount * 0.025
            wallet.amount = c_amount
            wallet.save()
            BinaryIncome.objects.create(
                paid_by=user,
                money_allocated_to=parent.name,
                amount=c_amount,
                for_month=date.today(),
            )
    elif rank == "Bronze":
        for parent in binary_parent.parents.all().order_by("-id")[:13]:
            wallet = Binawallet.objects.filter(user=parent.name).first()
            if not wallet:
                wallet = Binawallet.objects.create(user=parent.name, amount=0)

            c_amount = amount * 0.025
            wallet.amount = c_amount
            wallet.save()
            BinaryIncome.objects.create(
                paid_by=user,
                money_allocated_to=parent.name,
                amount=c_amount,
                for_month=date.today(),
            )
    elif rank == "Silver":
        for parent in binary_parent.parents.all().order_by("-id")[:13]:
            wallet = Binawallet.objects.filter(user=parent.name).first()
            if not wallet:
                wallet = Binawallet.objects.create(user=parent.name, amount=0)

            c_amount = amount * 0.025
            wallet.amount = c_amount
            wallet.save()
            BinaryIncome.objects.create(
                paid_by=user,
                money_allocated_to=parent.name,
                amount=c_amount,
                for_month=date.today(),
            )
    elif rank == "Gold":
        for parent in binary_parent.parents.all().order_by("-id")[:14]:
            wallet = Binawallet.objects.filter(user=parent.name).first()
            if not wallet:
                wallet = Binawallet.objects.create(user=parent.name, amount=0)

            c_amount = amount * 0.025
            wallet.amount = c_amount
            wallet.save()
            BinaryIncome.objects.create(
                paid_by=user,
                money_allocated_to=parent.name,
                amount=c_amount,
                for_month=date.today(),
            )
    elif rank == "Platinum":
        for parent in binary_parent.parents.all().order_by("-id")[:14]:
            wallet = Binawallet.objects.filter(user=parent.name).first()
            if not wallet:
                wallet = Binawallet.objects.create(user=parent.name, amount=0)

            c_amount = amount * 0.025
            wallet.amount = c_amount
            wallet.save()
            BinaryIncome.objects.create(
                paid_by=user,
                money_allocated_to=parent.name,
                amount=c_amount,
                for_month=date.today(),
            )
    elif rank == "Diamond":
        for parent in binary_parent.parents.all().order_by("-id")[:15]:
            wallet = Binawallet.objects.filter(user=parent.name).first()
            if not wallet:
                wallet = Binawallet.objects.create(user=parent.name, amount=0)

            c_amount = amount * 0.025
            wallet.amount = c_amount
            wallet.save()
            BinaryIncome.objects.create(
                paid_by=user,
                money_allocated_to=parent.name,
                amount=c_amount,
                for_month=date.today(),
            )
