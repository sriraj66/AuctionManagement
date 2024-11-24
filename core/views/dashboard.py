from django.shortcuts import render,redirect
from ..models import Player,Team,Auction,Category,Bidding
from django.contrib.auth.decorators import login_required
from ..consumer import broadcast_message_to_auction


TEMPLATE_ROOT = "root/"
PARTIALS = TEMPLATE_ROOT+"partials/"

@login_required
def dashboard(request,auction_id):
    auction = Auction.objects.get(id=auction_id)
    bid_state = auction.current_bid()
    
    broadcast_message_to_auction(auction_id,typ=0,data={
        "message" : "Backend Connected"
    })
        
    context = {
        "auction": auction,
        "players" : Player.objects.filter(auction=auction),
        "bidding" : Bidding.objects.filter(auction=auction),
        "teams" : Team.objects.filter(auction=auction),
        "current_bid": bid_state,
        "categories": Category.objects.filter(auction=auction)
    }
    if bid_state:
        context['player'] = bid_state.player
    
    
    return render(request,TEMPLATE_ROOT+"dashboard.html",context)

@login_required
def update_dash_players(request,auction_id):
    context = {
        "players" : Player.objects.filter(auction = Auction.objects.get(auction_id))
    }
    return render(request,PARTIALS+"dash_players.html",context)