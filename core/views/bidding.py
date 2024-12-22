from django.shortcuts import render,redirect,HttpResponse
from ..models import Auction,Team, Category, Player,Bidding
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success,error,warning


TEMPLATE_ROOT = "root/"
PARTIALS = TEMPLATE_ROOT+"partials/"


@login_required
def start_bid(request,auction_id):
    try:
        if request.method == "POST":
            auction = Auction.objects.get(id=auction_id,user=request.user)
            player_id = request.POST.get("player_id")
            player = Player.objects.get(id=player_id)
            
            if player.bidding():
                print(player.bidding())
                if player.bidding().is_sold == True:
                    return HttpResponse("Player Already Sold")
                
            obj = Bidding(
                user = request.user,
                auction = auction,
                player = player,
                curent_price = player.player_category.base_price
            )
            obj.save()
            print("Bidding Started")
            
            auction.current_bid_id = obj.id
            auction.save()
            return render(request,PARTIALS+"bidding_control.html",{
                "current_bid" : obj,
                "auction": auction,
                "player": player,
                "teams" : Team.objects.filter(auction=auction)
            })
        else:
            return HttpResponse("<p>Invalid Request</p>")

    except Exception as e:
        print(e)
    
    return HttpResponse("<p>No Player Exist</p>")

@login_required
def sell_player(request,bidding_id):
    bidding = Bidding.objects.get(id=bidding_id,user=request.user)
    bidding.auction.current_bid_id = 0
    
    try:
        if request.method == 'POST':
            current_price = request.POST.get("current_price")
            sold_to = request.POST.get("sold_to")
            bidding.curent_price = current_price
            print(current_price)
            
            # Sold
            if int(sold_to) != -1:
                team = Team.objects.get(id=sold_to)
                bidding.team = team
                if bidding.team.balance() < int(current_price):
                    error(request,f"Team {team.team_short_name} not enough team balance")
                    bidding.auction.save()
                    return redirect("dashboard",bidding.auction.id)
                
                bidding.is_sold = True
                bidding.player.is_sold = True
                success(request,f"Player Sold to {bidding.team}")
                
                bidding.team.used_amount += int(current_price)
                bidding.team.max_bid = max(bidding.team.max_bid,int(current_price))
                bidding.team.save()
                
            # Unsold
            else:
                bidding.is_sold = False
                bidding.player.is_sold = False
                warning(request,f"Player Unsold")
                
            bidding.auction.save()
            bidding.player.save()
            bidding.save()            
            
            
            return redirect("dashboard",bidding.auction.id)
        
    except Exception as e:
        print(e)
    error("Somthing went Wrong")
    bidding.auction.save()
    return redirect("dashboard",bidding.auction.id)
  
        
@login_required
def update_current_bit(request,auction_id):
    context = {
        "current_bid": Auction.objects.get(id=auction_id).current_bid()
    }
    return render(request,PARTIALS+"start_bid_form.html",context)
