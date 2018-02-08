from datetime import datetime
from unittest import mock

from bson.objectid import ObjectId
from pytest import fixture
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


@fixture
def mocks():
    mock_response = mock.Mock()
    mock_response.inserted_id = ObjectId(sample_id)
    mock_collection = mock.MagicMock(spec=Collection)
    mock_collection.insert_one.return_value = mock_response
    mock_database = mock.MagicMock(spec=Database)
    mock_database.__getitem__.return_value = mock_collection

    return mock_database, mock_collection, mock_response


def test_model_repr():
    assert repr(MyModel(None, False, True)) == "MyModel(_id=None, stop=False, go=True)"
    assert repr(MyModel("abc", "false", "true")) == "MyModel(_id='abc', stop='false', go='true')"


def test_auto_json():
    assert MyModel(None, False, True).to_json() == {"stop": False, "go": True}
    assert MyModel("abc", "false", "true").to_json() == {"_id": "abc", "stop": "false", "go": "true"}


def test_model_create(mocks):
    mock_database, mock_collection, mock_response = mocks

    my_model = MyModel(None, True, False)
    my_model.create(mock_database)

    mock_database.__getitem__.assert_called_with("test")
    mock_collection.insert_one.assert_called_with({"stop": True, "go": False})
    assert my_model.id == ObjectId(sample_id)

    with pytest.raises(ObjectAlreadyCreated):
        my_model.create(mock_database)


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
