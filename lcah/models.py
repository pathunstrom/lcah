from datetime import datetime
from datetime import timedelta
from uuid import uuid4 as uuid

from lcah import app
from lcah.errors import ObjectNotFound


class Auction:

    def __init__(self, _id=None, item="common", seller="pathunstrom",
                 current_bid=1000, api_id=None, close_time: float=None):
        self.id = _id
        self.api_id = api_id or uuid().hex
        self.item = item  # TODO: Make Item Object
        self.seller = seller  # TODO: Make User Object
        self.current_bid = current_bid
        self.min_bid = round(current_bid / 10, -1)
        if close_time is None:
            close_time = (datetime.utcnow() + timedelta(hours=2)).timestamp()
        self.close_time = datetime.fromtimestamp(close_time)

    def __repr__(self):
        return f"Auction(_id={self.id}, item={self.item}, seller={self.seller}, \
current_bid={self.current_bid}, api_id={self.api_id}, \
close_time={self.close_time.timestamp()})"

    def to_json(self, with_id=True):
        json = {
            "api_id": self.api_id,
            "item": self.item,
            "seller": self.seller,
            "current_bid": self.current_bid,
            "close_time": self.close_time.timestamp()
        }
        if with_id:
            json["_id"] = self.id

        return json

    @staticmethod
    def get(mongo, api_key=None):
        if api_key is not None:
            document = mongo.lcah.auction.find_one({"api_id": api_key})
            if not document:
                raise ObjectNotFound
            auction = Auction(**document)
            app.logger.debug(auction)
            return auction

    def create(self, mongo):
        app.logger.debug("Create called")
        doc = self.to_json(with_id=False)
        result = mongo.lcah.auction.insert_one(doc)
        app.logger.debug(f"_id: {result.inserted_id}, api key: {self.api_id}")
        self.id = result.inserted_id
