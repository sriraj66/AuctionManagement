from django.shortcuts import render,redirect,HttpResponse
from ..models import Auction,Team, Category, Player
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success,error,warning
import pandas as pd

TEMPLATE_ROOT = "root/"
PARTIALS = TEMPLATE_ROOT+"partials/"

@login_required
def auction(request):
    context = {
        "auctions" : Auction.objects.filter(user=request.user),
        "sports_type" : Auction.SPORTS_TYPE,
        "auction_type": Auction.AUCTION_TYPE
    }
    return render(request,TEMPLATE_ROOT+"create_auction.html",context)

@login_required
def create_auction(request):
    
    try:
        if request.method=='POST':
            auction_name = request.POST.get("auction_name")
            sports_type = request.POST.get("sport_type")
            auction_type = request.POST.get("auction_type")
            s_date = request.POST.get("start_date")
            e_date = request.POST.get("end_date")
            place = request.POST.get("auction_place")
            squad_limit = request.POST.get("squad_limit")
            team_purse = request.POST.get("team_purse")
            
    
            obj = Auction(user=request.user,auction_name=auction_name,sports_type=sports_type,auction_type=auction_type,starting_date=s_date,ending_date=e_date,auction_place=place,squad_limit=squad_limit,team_purse=team_purse)
                        
            obj.save()
            success(request,"Auction Created")
            return redirect("auction")
    except Exception as e:
        print(e)
        error(request,"Somthing went wrong")
        return redirect("auction")
    
    return redirect("auction")




@login_required
def manage_teams(request,auction_id):
    auction = Auction.objects.get(id=auction_id)

    context = {
        "auction" : auction,
        "teams" : Team.objects.filter(auction=auction),
        "categories": Category.objects.filter(auction=auction),
        "players" : Player.objects.filter(auction=auction)
    }
    
    return render(request,TEMPLATE_ROOT+"manage_team.html",context)

def create_team(request,auction_id):
    auction = Auction.objects.get(id=auction_id)
    
    if request.method=='POST':
        t_name = request.POST.get("team_name")
        s_name = request.POST.get("short_name")
        o_name = request.POST.get("owner_name")
        logo = request.FILES.get("logo")
        
        obj = Team(user = request.user,team_name=t_name,team_short_name=s_name,owner_name=o_name,team_logo=logo,auction=auction)
        
        obj.purse = auction.team_purse
        obj.save()
    
    context = { 
        "auction" : auction,
        "teams" : Team.objects.filter(auction=auction)
    }
    return render(request,PARTIALS+"team_table.html",context)


@login_required
def delete_team(request,auction_id,team_id):
    auction = Auction.objects.get(id=auction_id)
    
    try:
        if request.method=='POST':
            obj = Team.objects.get(id=team_id)            
            obj.delete()
            print(obj)
            
    except Exception as e:
        print(e)
    
    context = { 
        "auction" : auction,
        "teams" : Team.objects.filter(auction=auction)
    }
    return render(request,PARTIALS+"team_table.html",context)
    

@login_required
def add_categories(request,auction_id):
    try:
        
        auction = Auction.objects.get(id=auction_id)
        
        if request.method == 'POST':
            name = request.POST.get("name")
            short_name = request.POST.get("short_name")
            base_price = request.POST.get("base_price",0)
            limit_count = request.POST.get("limit_count",0)
            obj = Category(
                auction = auction,
                name = name,
                short_name = short_name,
                base_price = base_price,
                limit_count = limit_count
            )
            obj.save()
            print("Object Saved")
            
            return HttpResponse("<p class='text-success' >Done!!</p>")
    except Exception as e:
        print(e)
    return HttpResponse("<p class='text-danger' >Invalid Request</p>")

@login_required
def create_player(request,auction_id):
    try:
        auction = Auction.objects.get(id=auction_id)
        if request.method == 'POST':
            player_name = request.POST.get("player_name")
            player_category = request.POST.get("player_category")
            player_image = request.POST.get("player_image")
            mpl_id = request.POST.get("mpl_id")
            player_age = request.POST.get("player_age",0)
            player_village = request.POST.get("player_village")
            player_role = request.POST.get("player_role")
            player_matches = request.POST.get("player_matches",0)
            player_bat_matches = request.POST.get("player_bat_matches",0)
            player_bowl_matches = request.POST.get("player_bowl_matches",0)
            player_bat_runs = request.POST.get("player_bat_runs",0)
            player_bowl_runs = request.POST.get("player_bowl_runs",0)
            player_30s = request.POST.get("player_30s",0)
            player_50s = request.POST.get("player_50s",0)
            player_100s = request.POST.get("player_100s",0)
            player_max = request.POST.get("player_max",0)
            player_wickets = request.POST.get("player_wickets",0)
            player_economy = request.POST.get("player_economy",0)
            player_miden = request.POST.get("player_miden",0)
            player_hattrick = request.POST.get("player_hattrick",0)
            
            obj = Player(
                user = request.user,
                player_name = player_name,
                player_category = Category.objects.get(id=player_category),
                player_image = player_image,
                mpl_id = mpl_id,
                player_age = player_age,
                player_village = player_village,
                player_role = player_role,
                player_matches = player_matches,
                auction = auction,
                player_bat_matches = player_bat_matches,
                player_bat_runs = player_bat_runs,
                player_30s = player_30s,
                player_50s = player_50s,
                player_100s = player_100s,
                player_max = player_max,
                player_wickets = player_wickets,
                player_bowl_runs = player_bowl_runs,
                player_economy = player_economy,
                player_bowl_matches = player_bowl_matches,
                player_miden = player_miden,
                player_hattrick = player_hattrick
            )
            obj.save()
            print("Player Added")
    except Exception as e:
        print(e)
    context = {
        "players": Player.objects.filter(auction=auction)
    }
    return render(request,PARTIALS+"player_table.html",context)

@login_required
def delete_player(request,player_id):
    context = {
        "players": []
    }
    try:
        if request.method=='POST':
            if Player.objects.exists(player_id=player_id):
                player = Player.objects.get(id=player_id)
                if player.user == request.user:
                    context['players'] = Player.objects.filter(auction=player.auction)
                    player.delete()
                    print("Player Deleted")
        else:
            print("Invalid Request Method for deleation")            
    except Exception as e:
        print(e)
        
    return render(request,PARTIALS+"player_table.html",context)


@login_required
def edit_player(request,auction_id):
    try:
        playerid = request.POST.get("player_id")
        
        obj = Player.objects.get(id=int(playerid))
        
        if request.method == 'POST' and request.user == obj.user:
            player_name = request.POST.get("player_name")
            player_category = request.POST.get("player_category")
            player_image = request.POST.get("player_image")
            mpl_id = request.POST.get("mpl_id")
            player_age = request.POST.get("player_age", 0)
            player_village = request.POST.get("player_village")
            player_role = request.POST.get("player_role")
            player_matches = request.POST.get("player_matches", 0)
            player_bat_matches = request.POST.get("player_bat_matches", 0)
            player_bowl_matches = request.POST.get("player_bowl_matches", 0)
            player_bat_runs = request.POST.get("player_bat_runs", 0)
            player_bowl_runs = request.POST.get("player_bowl_runs", 0)
            player_30s = request.POST.get("player_30s", 0)
            player_50s = request.POST.get("player_50s", 0)
            player_100s = request.POST.get("player_100s", 0)
            player_max = request.POST.get("player_max", 0)
            player_wickets = request.POST.get("player_wickets", 0)
            player_economy = request.POST.get("player_economy", 0)
            player_miden = request.POST.get("player_miden", 0)
            player_hattrick = request.POST.get("player_hattrick", 0)
            
            
            # Update player details
            obj.player_name = player_name
            obj.player_category = Category.objects.get(id=player_category)
            obj.player_image = player_image
            obj.mpl_id = mpl_id
            obj.player_age = player_age
            obj.player_village = player_village
            obj.player_role = player_role
            obj.player_matches = player_matches
            obj.player_bat_matches = player_bat_matches
            obj.player_bowl_matches = player_bowl_matches
            obj.player_bat_runs = player_bat_runs
            obj.player_bowl_runs = player_bowl_runs
            obj.player_30s = player_30s
            obj.player_50s = player_50s
            obj.player_100s = player_100s
            obj.player_max = player_max
            obj.player_wickets = player_wickets
            obj.player_economy = player_economy
            obj.player_miden = player_miden
            obj.player_hattrick = player_hattrick
            
            # Save the updated player
            obj.save()
            success(request,f"Player : {player_name} Updated")
        else:
            error(request,"Invalid Request")
    except Exception as e:
        print(f"Error: {e}")
     
    return redirect("dashboard",auction_id)

@login_required
def upload_from_exel(request, auction_id):
    try:
        auction = Auction.objects.get(id=auction_id)
        if request.method == 'POST':
            excel_file = request.FILES.get("player_excel")
            
            if excel_file:
                df = pd.read_excel(excel_file)

                # Iterate through each row in the DataFrame
                for _, row in df.iterrows():
                    try:
                        obj = Player(
                            user=request.user,
                            player_name=row.get("player_name"),
                            player_category=Category.objects.get(id=row.get("player_category")),
                            player_image=row.get("player_image"),  # Handle image upload separately if needed
                            mpl_id=row.get("mpl_id"),
                            player_age=row.get("player_age", 0),
                            player_village=row.get("player_village"),
                            player_role=row.get("player_role"),
                            player_matches=row.get("player_matches", 0),
                            auction=auction,
                            player_bat_matches=row.get("player_bat_matches", 0),
                            player_bat_runs=row.get("player_bat_runs", 0),
                            player_30s=row.get("player_30s", 0),
                            player_50s=row.get("player_50s", 0),
                            player_100s=row.get("player_100s", 0),
                            player_max=row.get("player_max", 0),
                            player_wickets=row.get("player_wickets", 0),
                            player_bowl_runs=row.get("player_bowl_runs", 0),
                            player_economy=row.get("player_economy", 0),
                            player_bowl_matches=row.get("player_bowl_matches", 0),
                            player_miden=row.get("player_miden", 0),
                            player_hattrick=row.get("player_hattrick", 0)
                        )
                        obj.save()
                        print(f"Player {row.get('player_name')} added")
                    except Exception as row_error:
                        print(f"Error adding player {row.get('player_name')}: {row_error}")
            else:
                print("No Excel file uploaded")

    except Exception as e:
        print(f"Error: {e}")
    
    context = {
        "players": Player.objects.filter(auction=auction)
    }
    return render(request, PARTIALS + "player_table.html", context)
