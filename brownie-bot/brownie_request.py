from dataclasses import dataclass


@dataclass
class brownie_request:
    store_number: str
    date: str
    time: str
    order_id: str
    receipt_location: str
    code: str
