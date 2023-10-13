from django.shortcuts import render,redirect

# Create your views he
import queue

from .models import TradeSignals,SignalFollowedBy,TradeSymbol
from .forms import TradeSignalsForm,TakeProfitForm,TakeProfits
from django.views.generic import CreateView,ListView
from django.urls import reverse_lazy

from user.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .utils import process_telegram_message
from rest_framework import status
from django.db.models import Count
import ccxt
from jsonview.decorators import json_view
# from django.forms import formset_factory 
from django.forms import modelformset_factory


from django.http import HttpResponse
class TradeCreateView(CreateView):
    model = TradeSignals
    form_class = TradeSignalsForm
    
    # take_profit = TakeProfitForm
    # print("form is",form_class)
    template_name = 'signalbot/trade_create.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['take_profit'] = TakeProfitForm()
        TakeProfitFormSet = modelformset_factory(TakeProfits, form=TakeProfitForm, extra=4)
        context['form2'] = TakeProfitFormSet
        return context
    def post(self,request):
        TakeProfitFormSet = modelformset_factory(TakeProfits, form=TakeProfitForm)
        formset = TakeProfitFormSet(request.POST, queryset=TakeProfits.objects.none())
        formset.empty_permitted = True
        form = TradeSignalsForm(request.POST)
        x = form.save(commit=False)
        print("the id is ",x.id)
        # print(formset)
        if formset.is_valid() and form.is_valid():
            # print(form)
            print("hello")
            # for take_profit in formset:
            #     y = take_profit.save()
            #     form.instance.take_profit_amount.add(y)
            # form.save()    
        else:
            print("invalid")
        return HttpResponse("success")

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
    

def all_symbols():
    exchange = ccxt.binance({
        'rateLimit': 2000,  # Adjust this rate limit as needed
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
        }
    })

    # Fetch all available markets (symbols) for Binance Futures
    markets = exchange.fetch_markets()

    # Print the list of trading symbols
    # carry = []
    for market in markets:
        info = market["info"]
        # print(info)
        pair = info.get("pair",info.get("symbol"))
        base_asset = info.get("baseAsset")
        quote_asset = info.get("quoteAsset")
        if quote_asset == "USDT":
            TradeSymbol.objects.get_or_create(symbol=pair,base_asset=base_asset,quote_asset=quote_asset)

    return "true"
class ShowPairs(ListView):
    model = TradeSymbol
    template_name = 'binance/show_pairs.html'
    context_object_name = 'pairs'



def ADDPairs(request):
    if request.method == 'POST':
        print("recive request to get pairs")
        all_symbols()
        return redirect(reverse_lazy("signalbot:show-pairs"))
    if request.method == 'GET':
       return redirect(reverse_lazy("signalbot:show-pairs"))


@json_view
def pair_info(request):
    print("got request")
    exchange = ccxt.binance({
        'rateLimit': 2000,  # Adjust this rate limit as needed
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',
        }
    })

    # Fetch all available markets (symbols) for Binance Futures
    markets = exchange.fetch_markets()
    # print(request.GET['symbol'])
    required_symbol = request.GET['symbol']
    data = ""
    for symbol in markets:
        if symbol['info'].get("pair",symbol['info'].get("symbol")) == required_symbol:
            # print(symbol)
            data =  symbol["info"]
            # break
            return {"success":True,"symbol":data}

            # return {"symbol":
    return {"success":False}

