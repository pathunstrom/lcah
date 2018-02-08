from datetime import datetime

from bson.objectid import ObjectId
from lcah.models import Auction
from lcah.models import Model

sample_id = '5a7cc692b26565317881e8e1'


class MyModel(Model):
    """
    A test model to test functionality of Model base class.
    """
    def __init__(self, _id, stop, go):
        self._id = _id
        self.stop = stop
        self.go = go


def test_auto_repr():
    assert repr(MyModel(None, False, True)) == "MyModel(_id=None, stop=False, go=True)"
    assert repr(MyModel("abc", "false", "true")) == "MyModel(_id='abc', stop='false', go='true')"


def test_auto_json():
    assert MyModel(None, False, True).to_json() == {"stop": False, "go": True}
    assert MyModel("abc", "false", "true").to_json() == {"_id": "abc", "stop": "false", "go": "true"}


def test_auction_repr():
    dt = datetime.fromtimestamp(0)
    auction = Auction(_id=None, item="common", seller="pathunstrom",
                      current_bid=1000, api_id="5", close_time=dt)
    assert repr(auction) == "Auction(_id=None, item='common', seller='pathunstrom', current_bid=1000, api_id='5', close_time=datetime.datetime(1969, 12, 31, 19, 0))"


def test_auction_to_json():
    dt = datetime.fromtimestamp(0)
    auction = Auction(_id=None, item="common", seller="pathunstrom",
                      current_bid=1000, api_id="5", close_time=dt)
    assert auction.to_json() == {"item": "common",
                                 "seller": "pathunstrom",
                                 "current_bid": 1000,
                                 "api_id": '5',
                                 "close_time": datetime.fromtimestamp(0)}

    auction = Auction(_id=ObjectId(sample_id), item="uncommon",
                      seller="pathunstrom", current_bid=500, api_id="40",
                      close_time=dt)
    assert auction.to_json() == {"_id": ObjectId(sample_id),
                                 "item": "uncommon",
                                 "seller": "pathunstrom",
                                 "current_bid": 500,
                                 "api_id": "40",
                                 "close_time": datetime.fromtimestamp(0)}


def test_auction_create():
    pass
