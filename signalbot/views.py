from django.shortcuts import render

# Create your views he
import queue

from .models import TradeSignals,SignalFollowedBy
from .forms import TradeSignalsForm
from django.views.generic import CreateView,ListView
from django.urls import reverse_lazy

from user.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .utils import process_telegram_message
from rest_framework import status
from django.db.models import Count

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
    
class TradeSignalHistory(ListView):
    model = TradeSignals
    template_name = 'signalbot/trade_history.html'
    context_object_name = 'trades'
    paginate_by = 10
    def get_queryset(self):
        queryset = super().get_queryset()
        # Annotate each TradeSignals object with the follow count
        queryset = queryset.annotate(follow_count=Count('signalfollowedby'))
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class DisplaySignalFollowers(ListView):
    model = SignalFollowedBy
    template_name = 'signalbot/signal_followers.html'
    context_object_name = 'followers'
    paginate_by = 10

    def get_queryset(self):
        signal_id = self.kwargs['signal_id']  # Get the signal_id from URL parameter
        queryset = SignalFollowedBy.objects.filter(signal_id=signal_id)
        return queryset