from signalbot.models import SignalFollowedBy
from user.models import User, UserKey
from orders.models import UserActivePositions
import ccxt


def updatePositions():
    user_keys = UserKey.objects.filter(is_active=True)

    for user_key in user_keys:
        try:
            exchange = ccxt.binance(
                {
                    "apiKey": user_key.api_key,
                    "secret": user_key.api_secret,
                    "enableRateLimit": True,
                    "options": {"defaultType": "future"},
                }
            )
            exchange.set_sandbox_mode(True)
        except Exception as e:
            print(e)
            continue
        positions = exchange.fetch_positions()
        active_positions = []
        for position in positions:
            if float(position["info"]["positionAmt"]) != 0:
                active_positions.append(position)
        user = user_key.user
        signal_followed_by_user = SignalFollowedBy.objects.filter(user=user)
        if signal_followed_by_user.exists():
            for signals in signal_followed_by_user:
                symbol = signals.signal.symbol.symbol
                for active_position in active_positions:
                    print("YAHA")
                    print(active_position["symbol"])
                    print(symbol)
                    if active_position["info"]["symbol"] == symbol:
                        try:
                            user_active_positions = UserActivePositions.objects.get(
                                symbol=signals.signal.symbol, user=user
                            )
                            user_active_positions.mark_price = active_position[
                                "markPrice"
                            ]
                            user_active_positions.liquidationPrice = active_position[
                                "liquidationPrice"
                            ]
                            user_active_positions.breakEvenPrice = float(
                                active_position["info"]["breakEvenPrice"]
                            )
                            user_active_positions.marginRatio = active_position[
                                "marginRatio"
                            ]
                            user_active_positions.margin = active_position[
                                "initialMargin"
                            ]
                            user_active_positions.margin_percentage = active_position[
                                "initialMarginPercentage"
                            ]
                            user_active_positions.date_time = active_position[
                                "datetime"
                            ]
                            user_active_positions.pnl = active_position["unrealizedPnl"]
                            user_active_positions.save()
                        except UserActivePositions.DoesNotExist:
                            user_active_positions = UserActivePositions.objects.create(
                                symbol=signals.signal.symbol, user=user
                            )
                            user_active_positions.entry_price = active_position[
                                "entryPrice"
                            ]
                            user_active_positions.mark_price = active_position[
                                "markPrice"
                            ]
                            user_active_positions.liquidationPrice = active_position[
                                "liquidationPrice"
                            ]
                            user_active_positions.breakEvenPrice = float(
                                active_position["info"]["breakEvenPrice"]
                            )
                            user_active_positions.marginRatio = active_position[
                                "marginRatio"
                            ]
                            user_active_positions.margin = active_position[
                                "initialMargin"
                            ]
                            user_active_positions.margin_percentage = active_position[
                                "initialMarginPercentage"
                            ]
                            user_active_positions.date_time = active_position[
                                "datetime"
                            ]
                            user_active_positions.pnl = active_position["unrealizedPnl"]
                            user_active_positions.save()


# def updatePositions():
#     user_keys = UserKey.objects.filter(is_active=True).select_related("user")
#     users = [uk.user for uk in user_keys]
#     signals = SignalFollowedBy.objects.filter(user__in=users).select_related(
#         "signal__symbol"
#     )

#     signal_map = {s.user.id: s for s in signals}

#     for user_key in user_keys:
#         try:
#             exchange = ccxt.binance(
#                 {
#                     "apiKey": "7a0c551f04850fb74e0091e60d9fa7bf67c89dff8459c500818c1823af40960c",
#                     "secret": "261e98e03d8695cd5815c75a3328aff36cac3d040bf5bb2f9cb25c8701629d50",
#                     "enableRateLimit": True,
#                     "options": {"defaultType": "future"},
#                 }
#             )
#         except Exception as e:
#             print(e)
#             continue
#         exchange.set_sandbox_mode(True)
#         positions = exchange.fetch_positions()
#         active_positions = [
#             p for p in positions if float(p["info"]["positionAmt"]) != 0
#         ]

#         for active_position in active_positions:
#             signal = signal_map.get(user_key.user.id)
#             if signal and active_position["symbol"] == signal.signal.symbol.symbol:
#                 try:
#                     user_active_positions = UserActivePositions.objects.get(
#                         symbol=signal.signal.symbol, user=signal.user
#                     )
#                     user_active_positions.mark_price = active_positions["markPrice"]
#                     user_active_positions.liquidationPrice = active_positions[
#                         "liquidationPrice"
#                     ]
#                     user_active_positions.breakEvenPrice = float(
#                         active_positions["info"]["breakEvenPrice"]
#                     )
#                     user_active_positions.marginRatio = active_positions["marginRatio"]
#                     user_active_positions.margin = active_positions["margin"]
#                     user_active_positions.margin_percentage = active_positions[
#                         "initialMarginPercentage"
#                     ]
#                     user_active_positions.pnl = active_positions["unrealizedPnl"]
#                     user_active_positions.save()
#                 except UserActivePositions.DoesNotExist:
#                     user_active_positions = UserActivePositions.objects.get(
#                         symbol=signal.signal.symbol, user=signal.user
#                     )
#                     user_active_positions.entry_price = active_positions["entryPrice"]
#                     user_active_positions.mark_price = active_positions["markPrice"]
#                     user_active_positions.liquidationPrice = active_positions[
#                         "liquidationPrice"
#                     ]
#                     user_active_positions.breakEvenPrice = float(
#                         active_positions["info"]["breakEvenPrice"]
#                     )
#                     user_active_positions.marginRatio = active_positions["marginRatio"]
#                     user_active_positions.margin = active_positions["margin"]
#                     user_active_positions.margin_percentage = active_positions[
#                         "initialMarginPercentage"
#                     ]
#                     user_active_positions.pnl = active_positions["unrealizedPnl"]
#                     user_active_positions.save()

#                 except Exception as e:
#                     print(e)
