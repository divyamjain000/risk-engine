from growwapi import GrowwAPI

class GrowwAdapter:
    def __init__(self, access_token: str):
        self.client = GrowwAPI(access_token)

    def fetch_holdings(self):
        return self.client.get_holdings()

    def fetch_positions(self):
        return self.client.get_positions()

    def fetch_orders(self):
        return self.client.get_orders()
