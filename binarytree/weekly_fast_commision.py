from binarytree.models import UserRank


def calculate_commission(ancestors):
    membership_amount = 40
    level = len(ancestors)
    for ancestor in ancestors:
        user = ancestor.user
        rank = UserRank.objects.get(user=user).rank.name
        print("user :", user)
        print("rank :", rank)
        print("level :", level)
        level = level - 1
        if level == 1:
            print(f"commision {membership_amount*0.5}")
        elif (
            level == 2
            and rank == "Bronze"
            or rank == "Silver"
            or rank == "Gold"
            or rank == "Platinum"
            or rank == "Diamond"
        ):
            print(f"commision {membership_amount*0.1}")
        elif (
            level == 3
            or level == 4
            and rank == "Silver"
            or rank == "Gold"
            or rank == "Platinum"
            or rank == "Diamond"
        ):
            print(f"commision {membership_amount*0.05}")
        elif level == 5 and rank == "Platinum" or rank == "Diamond" or rank == "Gold":
            print(f"commision {membership_amount*0.03}")
        elif level == 6 and rank == "Platinum" or rank == "Diamond" or rank == "Gold":
            print(f"commision {membership_amount*0.02}")
        elif level == 7 and rank == "Platinum" or rank == "Diamond":
            print(f"commision {membership_amount*0.02}")
        elif level == 8 and rank == "Platinum" or rank == "Diamond":
            print(f"commision {membership_amount*0.01}")
        elif level == 9 or level == 10 and rank == "Diamond":
            print(f"commision {membership_amount*0.01}")
        else:
            print("no commisions")
