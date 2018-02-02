from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from lcah import app
from lcah import mongo
import lcah.handlers as handlers
from lcah.models import Auction
from lcah.utils import catch_object_not_found


@app.route("/")
def home():
    return render_template("layout.html")


@app.route("/auction", methods=["GET", "POST"])
def auction_home():
    if request.method == "POST":
        return handlers.create_auction(request, app, mongo)
    else:
        return render_template("auctions.html")


@app.route("/auction/<identifier>")
@catch_object_not_found(app)
def auction_detail(identifier):
    app.logger.debug(f"Identifier: {identifier}")
    auction = Auction.get(mongo, identifier)
    return render_template("auction.html", auction=auction)


@app.route("/bid/<_id>")
def bid(_id):
    return redirect(url_for("auction_detail", identifier=_id))


@app.route("/create/auction")
def create_auction():
    return render_template("create-auction.html")
