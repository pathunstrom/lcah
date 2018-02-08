from datetime import datetime
from datetime import timedelta
from inspect import signature
from uuid import uuid4 as uuid

from bson.objectid import ObjectId

from lcah import app
from lcah.errors import ObjectNotFound


class Model:

    _id = None
    collection = "test"
    database = "lcah"  # TODO: Use Environment Variable.

    def __repr__(self):
        parameters = ", ".join(f"{k}={v!r}" for k, v in self.items())
        return f"{type(self).__name__}({parameters})"

    def items(self):
        for param in signature(type(self)).parameters:
            yield param, getattr(self, param)

    def to_json(self):
        value = dict(self.items())
        if "_id" in value and self._id is None:
            del value["_id"]
        return value

    @property
    def id(self):
        return self._id


class Auction(Model):
    collection = "auctions"

    def __init__(self, _id: ObjectId=None, item="common", seller="pathunstrom",
                 current_bid: int=1000, api_id: str=None,
                 close_time: datetime=None):
        self._id = _id
        self.api_id = api_id or uuid().hex
        self.item = item  # TODO: Make Item Object
        self.seller = seller  # TODO: Make User Object
        self.current_bid = current_bid
        self.min_bid = round(current_bid / 10, -1)
        if close_time is None:
            close_time = datetime.utcnow() + timedelta(hours=2)
        self.close_time = close_time

    @staticmethod
    def get(mongo, *, api_key=None):
        if api_key is not None:
            document = mongo.lcah.auction.find_one({"api_id": api_key})
            if not document:
                raise ObjectNotFound
            auction = Auction(**document)
            app.logger.debug(auction)
            return auction

    @staticmethod
    def get_all(mongo):
        for doc in mongo.lcah.auction.find():
            try:
                yield Auction(**doc)
            except:
                app.logger.error(f"Auction document failed: {doc['_id']}")
                continue

    def create(self, mongo):
        app.logger.debug("Create called")
        doc = self.to_json()
        result = mongo.lcah.auction.insert_one(doc)
        app.logger.debug(f"_id: {result.inserted_id}, api key: {self.api_id}")
        self._id = result.inserted_id


class Bid:

    def __init__(self, _id: ObjectId=None, auction_id=None, user="red",
                 amount=7000, time=None):
        self.id = _id
        self._auction = auction_id
        self.user = user
        self.amount = amount
        self.time = time or datetime.utcnow()

    def create(self, mongo):
        doc = self.to_json(with_id=False)
        result = mongo.lcah.bid.insert_one(doc)
        self.id = result.inserted_id
        return self
