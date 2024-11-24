from django.shortcuts import render,redirect,HttpResponse
from ..models import Player,Team,Auction,Category,Bidding
from django.contrib.auth.decorators import login_required
from django.core import serializers
from ..consumer import broadcast_message_to_auction
from .serializers import AuctionSerializer,PlayerSerializer, BiddingSerializer

TEMPLATE_ROOT = "root/"
PARTIALS = TEMPLATE_ROOT+"partials/"

DATA_INFO = ["PLAYER","AUCTION","BIDDING"]


# Splashing to Socket
def show_player_info(request,auction_id,player_id):
    
    if request.method == "POST":
        player = Player.objects.get(id=player_id)
        
        player_data = PlayerSerializer(player).data
        data = {
            "method": DATA_INFO[0],
            "message": "Showing Player Info",
            "player": player_data
        }
        
        
        broadcast_message_to_auction(auction_id,data=data)

        return HttpResponse(f"<p class='text-success' > Showing {player.player_name} in Pannel </p>")   
    
    return HttpResponse(f"<p class='text-danger' > Invalid Request </p>")   
 
 
def show_auction_info(request,auction_id):

    if request.method == "POST":
        auction = Auction.objects.get(id=auction_id)
        
        auction_data = AuctionSerializer(auction).data
        
        data = {
            "method": DATA_INFO[1],
            "message": "Showing Auction Info",
            "auction": auction_data
        }
        
        
        broadcast_message_to_auction(auction_id,data=data)

        return HttpResponse(f"<p class='text-success' > Showing {auction.auction_name} in Pannel </p>")   
    
    return HttpResponse(f"<p class='text-danger' > Invalid Request </p>")   

def show_bidding_info(request,auction_id):

    if request.method == "POST":
        
        auction = Auction.objects.get(id=auction_id)
        bid_state = auction.current_bid()
        
        if bid_state:        
            bidding_data = BiddingSerializer(bid_state)
        else:
            bidding_data = "No Current Active Bid"
            
        data = {
            "method": DATA_INFO[2],
            "message": "Showing Bidding Info",
            "bidding": bidding_data
        }
        
        broadcast_message_to_auction(auction_id,data=data)

        return HttpResponse(f"<p class='text-success' > Showing {auction.auction_name} in Pannel </p>")   
    
    return HttpResponse(f"<p class='text-danger' > Invalid Request </p>")   



def pannel(request,auction_id):
    context = {
        "auction": Auction.objects.get(id=auction_id),
    }
    return render(request,TEMPLATE_ROOT+"pannel.html",context)