from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core.paginator import Paginator
from .models import TradeHistory
from orders.models import Order, UserActivePositions
from signalbot.models import SignalFollowedBy
from orders.serializers import UserActivePositionsSerializer


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
            await self.send(text_data=json.dumps({"type": "connected"}))

    async def send_closed_trades(self, event):
        user_followed_signals = SignalFollowedBy.objects.filter(
            user=self.user
        ).order_by("-id")
        closed_trades = []

        for signal in user_followed_signals:
            order = signal.first_order_id
            if order and order.filled:
                initial_data = {
                    "datetime": order.executed_date_time.isoformat(),
                    "pair": order.symbol.symbol,
                    "size": float(order.order_quantity),
                    "trade_direction": order.trade_direction,
                    "entry_price": {
                        "price": float(order.entry_price),
                        "avg": float(order.avg_price),
                    },
                    "filled_qty": float(order.filled_quantity),
                    "remaining_quantity": float(order.remaining_quantity),
                    "targets": [],
                    "pnl": {"pnl_amount": 0, "pnl_percent": 0},
                }

                pnl = 0
                initial_investment = float(order.entry_price) * float(
                    order.filled_quantity
                )
                related_orders = Order.objects.filter(related_order=order)

                for related_order in related_orders:
                    if related_order.filled:
                        if related_order.trade_direction == "TAKE_PROFIT":
                            target_pnl = (
                                related_order.avg_price - order.avg_price
                            ) * related_order.filled_quantity
                            pnl += target_pnl
                            initial_data["targets"].append(
                                {
                                    "datetime": related_order.executed_date_time.isoformat(),
                                    "name": "Tp1",
                                    "target_achieved": True,
                                    "target_price": float(related_order.entry_price),
                                }
                            )
                        elif related_order.trade_direction == "STOP_LOSS":
                            initial_data["hit_stop_loss"] = True
                            initial_data["stop_loss_price"] = float(
                                related_order.entry_price
                            )

                initial_data["pnl"]["pnl_amount"] = float(pnl)
                if initial_investment != 0:
                    initial_data["pnl"]["pnl_percent"] = (
                        float(float(pnl) / float(initial_investment)) * 100
                    )

                closed_trades.append(initial_data)

        await self.send(
            text_data=json.dumps(
                {
                    "type": "closed_trades",
                    "trades": closed_trades,
                }
            )
        )

    async def send_open_trades(self, event):
        user_followed_signals = SignalFollowedBy.objects.filter(
            user=self.user
        ).order_by("-id")
        open_trades = []

        for signal in user_followed_signals:
            order = signal.first_order_id
            if order:
                initial_data = {
                    "datetime": order.executed_date_time.isoformat(),
                    "pair": order.symbol.symbol,
                    "size": float(order.order_quantity),
                    "trade_direction": order.trade_direction,
                    "entry_price": {
                        "price": float(order.entry_price),
                        "avg": float(order.avg_price),
                    },
                    "filled_qty": float(order.filled_quantity),
                    "remaining_quantity": float(order.remaining_quantity),
                    "targets": [],
                    "pnl": {"pnl_amount": 0, "pnl_percent": 0},
                }

                pnl = 0
                initial_investment = float(order.entry_price) * float(
                    order.filled_quantity
                )
                related_orders = Order.objects.filter(related_order=order)

                for related_order in related_orders:

                    if related_order.trade_direction == "TAKE_PROFIT":
                        target_pnl = (
                            related_order.avg_price - order.avg_price
                        ) * related_order.filled_quantity
                        pnl += target_pnl
                        initial_data["targets"].append(
                            {
                                "datetime": related_order.executed_date_time.isoformat(),
                                "name": "Tp1",
                                "target_achieved": related_order.filled,
                                "target_price": float(related_order.entry_price),
                            }
                        )
                    elif related_order.trade_direction == "STOP_LOSS":
                        initial_data["hit_stop_loss"] = related_order.filled
                        initial_data["stop_loss_price"] = float(
                            related_order.entry_price
                        )

                initial_data["pnl"]["pnl_amount"] = float(pnl)
                if initial_investment != 0:
                    initial_data["pnl"]["pnl_percent"] = (
                        float(float(pnl) / float(initial_investment)) * 100
                    )

                open_trades.append(initial_data)

        await self.send(
            text_data=json.dumps(
                {
                    "type": "open_trades",
                    "trades": open_trades,
                }
            )
        )

    async def send_active_trades(self, event):
        user_active_positions = UserActivePositions.objects.filter(
            user=self.user
        ).order_by("-id")
        serializer = UserActivePositionsSerializer(user_active_positions, many=True)
        user_active_trades = serializer.data
        await self.send(
            text_data=json.dumps(
                {
                    "type": "active_trades",
                    "trades": user_active_trades,
                }
            )
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json["type"]

        if message_type == "open_trades_request":
            await self.send_open_trades(event=None)
        elif message_type == "closed_trades_request":
            await self.send_closed_trades(event=None)
        elif message_type == "active_trades_request":
            await self.send_active_trades(event=None)

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
