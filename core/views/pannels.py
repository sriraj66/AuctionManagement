from django.shortcuts import render,redirect,HttpResponse
from ..models import Player,Team,Auction,Category,Bidding
from django.contrib.auth.decorators import login_required
from django.core import serializers
from ..consumer import broadcast_message_to_auction
from .serializers import AuctionSerializer,PlayerSerializer, BiddingSerializer

TEMPLATE_ROOT = "root/"
PARTIALS = TEMPLATE_ROOT+"partials/"

DATA_INFO = ["PLAYER_PROFILE","AUCTION_START","BIDDING_PLAYER","BIDDING_RESULT"]


# Splashing to Socket
def show_player_info(request,auction_id,player_id):
    
    if request.method == "POST":
        player = Player.objects.get(id=player_id)
        
        player_data = PlayerSerializer(player).data
        data = {
            "method": DATA_INFO[0],
            "message": "Showing Player Profile",
            "player": player_data
        }
        
        
        broadcast_message_to_auction(auction_id,data=data)

        return HttpResponse(f"<p class='text-success' > Showing {player.player_name} in Pannel </p>")   
    
    return HttpResponse(f"<p class='text-danger' > Invalid Request </p>")   
 
 
#  AUCTION INFO
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


# Player Bidding INfo
def show_bidding_info(request,auction_id):

    if request.method == "POST":
        
        auction = Auction.objects.get(id=auction_id)
        bid_state = auction.current_bid()
        
        if bid_state:       
            print(bid_state.player)
            try:
                data = BiddingSerializer(bid_state).data
            except Exception as e:
                data = None
                print("Error : ",e)
        else:
            data = None
            
        data = {
            "method": DATA_INFO[2],
            "message": "Showing Bidding on Screen",
            "bidding": data
        }
        
        broadcast_message_to_auction(auction_id,data=data)

        return HttpResponse(f"<p class='text-success' > Showing {auction.auction_name} in Pannel </p>")   
    
    return HttpResponse(f"<p class='text-danger' > Invalid Request </p>")   


# Bidding Result
def show_bidding_result(bid_id):
    try:
        bidding = Bidding.objects.get(id=bid_id)
        
        data = {
            "method": DATA_INFO[3],
            "message": "Showing Bidding Result on Screen",
            "bidding": BiddingSerializer(bidding).data
        }
        broadcast_message_to_auction(bidding.auction.id,data=data)
        return True    
    
    except Exception as e:
        print(f"Error While Bidding Result on Panel {e}")
        
        return False
    

# TODO
def init_bid(request,auction_id,bid_id):

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