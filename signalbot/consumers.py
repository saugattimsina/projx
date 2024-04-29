from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core.paginator import Paginator
from .models import TradeHistory


class TradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.room_group_name = f"user_{self.user.username}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )
            await self.accept()
            await self.send_initial_trade_history(
                event=None
            )  # Modify this call to include an event parameter

    async def send_initial_trade_history(self, event):  # Add 'event' parameter here
        trades = TradeHistory.objects.filter(user=self.user).order_by("-id")
        paginator = Paginator(trades, 10)
        page1 = paginator.page(1)
        trades_data = [
            {
                "trade_id": trade.trade_id,
                "symbol": trade.symbol,
                "amount": trade.amount,
                "price": trade.price,
                "trade_side": trade.trade_side,
                "profit_loss": trade.profit_loss,
                "trade_fee": trade.trade_fee,
                "fee_currency": trade.fee_currency,
                "timestamp": trade.timestamp,
            }
            for trade in page1.object_list
        ]
        await self.send(
            text_data=json.dumps({"type": "initial_trades", "trades": trades_data})
        )

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
