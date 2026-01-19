from typing import Any, Optional, Tuple

from growwapi import GrowwAPI

class GrowwAdapter:
    def __init__(self, access_token: str):
        self.client = GrowwAPI(access_token)

    @staticmethod
    def get_access_token(api_key: str, totp: Optional[str] = None, secret: Optional[str] = None) -> dict:
        return GrowwAPI.get_access_token(api_key=api_key, totp=totp, secret=secret)

    def cancel_order(self, groww_order_id: str, segment: str, timeout: Optional[int] = None) -> dict:
        return self.client.cancel_order(groww_order_id=groww_order_id, segment=segment, timeout=timeout)

    def generate_socket_token(self, key_pair) -> dict:
        return self.client.generate_socket_token(key_pair=key_pair)

    def get_all_instruments(self) -> Any:
        return self.client.get_all_instruments()

    def get_available_margin_details(self, timeout: Optional[int] = None) -> dict:
        return self.client.get_available_margin_details(timeout=timeout)

    def get_contracts(self, exchange: str, underlying_symbol: str, expiry_date: str, timeout: Optional[int] = None) -> dict:
        return self.client.get_contracts(
            exchange=exchange,
            underlying_symbol=underlying_symbol,
            expiry_date=expiry_date,
            timeout=timeout,
        )

    def get_expiries(
        self,
        exchange: str,
        underlying_symbol: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> dict:
        return self.client.get_expiries(
            exchange=exchange,
            underlying_symbol=underlying_symbol,
            year=year,
            month=month,
            timeout=timeout,
        )

    def get_greeks(self, exchange: str, underlying: str, trading_symbol: str, expiry: str) -> dict:
        return self.client.get_greeks(exchange=exchange, underlying=underlying, trading_symbol=trading_symbol, expiry=expiry)

    def get_historical_candle_data(
        self,
        trading_symbol: str,
        exchange: str,
        segment: str,
        start_time: str,
        end_time: str,
        interval_in_minutes: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> dict:
        return self.client.get_historical_candle_data(
            trading_symbol=trading_symbol,
            exchange=exchange,
            segment=segment,
            start_time=start_time,
            end_time=end_time,
            interval_in_minutes=interval_in_minutes,
            timeout=timeout,
        )

    def get_historical_candles(
        self,
        exchange: str,
        segment: str,
        groww_symbol: str,
        start_time: str,
        end_time: str,
        candle_interval: str,
        timeout: Optional[int] = None,
    ) -> dict:
        return self.client.get_historical_candles(
            exchange=exchange,
            segment=segment,
            groww_symbol=groww_symbol,
            start_time=start_time,
            end_time=end_time,
            candle_interval=candle_interval,
            timeout=timeout,
        )

    def get_holdings_for_user(self, timeout: Optional[int] = None) -> dict:
        return self.client.get_holdings_for_user(timeout=timeout)

    def get_holdings(self):
        return self.get_holdings_for_user()

    def get_instrument_by_exchange_and_trading_symbol(self, exchange: str, trading_symbol: str) -> dict:
        return self.client.get_instrument_by_exchange_and_trading_symbol(exchange=exchange, trading_symbol=trading_symbol)

    def get_instrument_by_exchange_token(self, exchange_token: str) -> dict:
        return self.client.get_instrument_by_exchange_token(exchange_token=exchange_token)

    def get_instrument_by_groww_symbol(self, groww_symbol: str) -> dict:
        return self.client.get_instrument_by_groww_symbol(groww_symbol=groww_symbol)

    def get_instruments(self) -> Any:
        return self.get_all_instruments()

    def get_ltp(self, exchange_trading_symbols: Tuple[str], segment: str, timeout: Optional[int] = None) -> dict:
        return self.client.get_ltp(exchange_trading_symbols=exchange_trading_symbols, segment=segment, timeout=timeout)

    def get_ohlc(self, exchange_trading_symbols: Tuple[str], segment: str, timeout: Optional[int] = None) -> dict:
        return self.client.get_ohlc(exchange_trading_symbols=exchange_trading_symbols, segment=segment, timeout=timeout)

    def get_order_detail(self, segment: str, groww_order_id: str, timeout: Optional[int] = None) -> dict:
        return self.client.get_order_detail(segment=segment, groww_order_id=groww_order_id, timeout=timeout)

    def get_order_list(
        self,
        page: Optional[int] = 0,
        page_size: Optional[int] = 25,
        segment: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> dict:
        return self.client.get_order_list(page=page, page_size=page_size, segment=segment, timeout=timeout)

    def get_order_margin_details(self, segment: str, orders: list, timeout: Optional[int] = None) -> dict:
        return self.client.get_order_margin_details(segment=segment, orders=orders, timeout=timeout)

    def get_order_status(self, segment: str, groww_order_id: str, timeout: Optional[int] = None) -> dict:
        return self.client.get_order_status(segment=segment, groww_order_id=groww_order_id, timeout=timeout)

    def get_order_status_by_reference(self, segment: str, order_reference_id: str, timeout: Optional[int] = None) -> dict:
        return self.client.get_order_status_by_reference(segment=segment, order_reference_id=order_reference_id, timeout=timeout)

    def get_position_for_trading_symbol(self, trading_symbol: str, segment: str, timeout: Optional[int] = None) -> dict:
        return self.client.get_position_for_trading_symbol(trading_symbol=trading_symbol, segment=segment, timeout=timeout)

    def get_positions_for_user(self, segment: Optional[str] = None, timeout: Optional[int] = None) -> dict:
        return self.client.get_positions_for_user(segment=segment, timeout=timeout)

    def get_positions(self):
        return self.get_positions_for_user()

    def get_quote(self, trading_symbol: str, exchange: str, segment: str, timeout: Optional[int] = None) -> dict:
        return self.client.get_quote(trading_symbol=trading_symbol, exchange=exchange, segment=segment, timeout=timeout)

    def get_trade_list_for_order(
        self,
        groww_order_id: str,
        segment: str,
        page: Optional[int] = 0,
        page_size: Optional[int] = 25,
        timeout: Optional[int] = None,
    ) -> dict:
        return self.client.get_trade_list_for_order(
            groww_order_id=groww_order_id,
            segment=segment,
            page=page,
            page_size=page_size,
            timeout=timeout,
        )

    def modify_order(
        self,
        order_type: str,
        segment: str,
        groww_order_id: str,
        quantity: int,
        price: Optional[float] = None,
        trigger_price: Optional[float] = None,
        timeout: Optional[int] = None,
    ) -> dict:
        return self.client.modify_order(
            order_type=order_type,
            segment=segment,
            groww_order_id=groww_order_id,
            quantity=quantity,
            price=price,
            trigger_price=trigger_price,
            timeout=timeout,
        )

    def place_order(
        self,
        validity: str,
        exchange: str,
        order_type: str,
        product: str,
        quantity: int,
        segment: str,
        trading_symbol: str,
        transaction_type: str,
        order_reference_id: Optional[str] = None,
        price: Optional[float] = 0.0,
        trigger_price: Optional[float] = None,
        timeout: Optional[int] = None,
    ) -> dict:
        return self.client.place_order(
            validity=validity,
            exchange=exchange,
            order_type=order_type,
            product=product,
            quantity=quantity,
            segment=segment,
            trading_symbol=trading_symbol,
            transaction_type=transaction_type,
            order_reference_id=order_reference_id,
            price=price,
            trigger_price=trigger_price,
            timeout=timeout,
        )
