from django.shortcuts import render

# Create your views he
import queue

from .models import TradeSignals
from .forms import TradeSignalsForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

from user.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .utils import process_telegram_message
from rest_framework import status


class TradeCreateView(CreateView):
    model = TradeSignals
    form_class = TradeSignalsForm
    # print("form is",form_class)
    template_name = 'signalbot/trade_create.html'
    success_url = '/'
    # success_url = r)
    # return render(request, 'signalbot/trade_create.html', {'form': form_class})

class TelegramWebhook(APIView):
    def post(self, request, token):
        print(token)
        if token != settings.TELEGRAM_WEBHOOK_TOKEN:
            return Response(
                {"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )

        process_telegram_message(request.data)

        return Response({"success": True})