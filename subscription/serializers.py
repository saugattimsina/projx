from rest_framework import serializers
from .models import Subscription, UserSubPaymentHistory, SubscriptionDetail


from .payment_generate import get_payment_qr


import qrcode
import base64
from io import BytesIO


def qr_generator(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    # Convert the image to a BytesIO object
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")

    # Encode the image as base64
    base64_image = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    return base64_image


class SubscriptionSerializer(serializers.Serializer):
    payment_id = serializers.CharField(max_length=100)

    def create_payment_custom(self, validated_data):
        payment_id = validated_data.get("payment_id")
        user = self.context["user"]
        payments = Subscription.objects.filter(id=payment_id).first()
        # print(payment)
        if payments.package_type == "free":
            return {"message": "package is already free", "image": ""}
        else:
            payment = get_payment_qr(payments.price, user.username)
            print(payment)
            payment_qr = payment["pay_address"]
            UserSubPaymentHistory.objects.create(
                user=user,
                subscription=payments,
                date_transaction=payment["created_at"],
                amount=payments.price,
                payment_id=payment["payment_id"],
                payment_status=payment["payment_status"],
                remaining_amount=payments.price,
                has_partial_payment=True,
            )

            img = qr_generator(payment_qr)

            return {"mesage": "please pay to this qr code", "image": img}


class SubscriptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionDetail
        # fields = '__all__'
        exclude = ("related_to", "id")


class SubscriptionDataSerializer(serializers.ModelSerializer):
    subscription_details = SubscriptionDetailSerializer(
        source="subscriptiondetail_set", many=True
    )

    class Meta:
        model = Subscription
        fields = (
            "package_name",
            "price",
            "time_in_days",
            "time_in_months",
            "description",
            "package_type",
            "subscription_details",
        )
        # feilds = ('subscription_details',)
