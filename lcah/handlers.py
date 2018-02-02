from datetime import datetime
from datetime import timedelta

from flask import redirect
from flask import url_for

from lcah.models import Auction


def create_auction(request, app, db_connection):
    user = request.form["user"]
    item = request.form["item"]
    minimum_bid = int(request.form["min-bid"])
    hours = int(request.form["time"])
    end = (datetime.utcnow() + timedelta(hours=hours)).timestamp()
    auction = Auction(item=item, seller=user, current_bid=minimum_bid,
                      close_time=end)
    auction.create(db_connection)
    return redirect(url_for("auction_detail", identifier=auction.api_id))