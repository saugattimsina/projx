from binarytree.models import MLMRank
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "create a MLMRank"

    def handle(self, *args, **options):
        # Pawn
        MLMRank.objects.create(
            equivalent_name="Pawn",
            rank_name="Pawn",
            direct_referrals=0,
            active_members=0,
            separate_enroller_tree_conditions={},
            rank_level=1,
        )

        # Knight
        MLMRank.objects.create(
            equivalent_name="Knight",
            rank_name="Knight",
            direct_referrals=5,
            active_members=20,
            separate_enroller_tree_conditions={},
            rank_level=2,
        )

        # Bishop
        MLMRank.objects.create(
            equivalent_name="Bishop",
            rank_name="Bishop",
            direct_referrals=10,
            active_members=100,
            separate_enroller_tree_conditions={
                "rank": {"Knight": 3},
                "member": {"total": 100, "tree": 30},
            },
            rank_level=3,
        )

        # Rook
        MLMRank.objects.create(
            equivalent_name="Rook",
            rank_name="Rook",
            direct_referrals=30,
            active_members=300,
            separate_enroller_tree_conditions={
                "rank": {"Bishop": 3},
                "member": {"total": 300, "tree": 75},
            },
            rank_level=4,
        )

        # Queen
        MLMRank.objects.create(
            equivalent_name="Queen",
            rank_name="Queen",
            direct_referrals=0,
            active_members=0,
            separate_enroller_tree_conditions={
                "rank": {"Rook": 3},
                "member": {"total": 1500, "tree": 300},
            },
            rank_level=5,
        )

        # King
        MLMRank.objects.create(
            equivalent_name="King",
            rank_name="King",
            direct_referrals=0,
            active_members=0,
            separate_enroller_tree_conditions={
                "rank": {"Queen": 3},
                "member": {"total": 33000, "tree": 6000},
            },
            rank_level=6,
        )

        # Print success message
        self.stdout.write(self.style.SUCCESS("MLMRank created successfully"))
