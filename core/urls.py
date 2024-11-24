from django.urls import path
from .controller import *

urlpatterns = [
    
    
    # create_auction.py
    path("",auction,name="auction"),
    
    path("create/create",create_auction,name="create_auction"),
    
    # Teams
    path("manageTeam/create/<int:auction_id>",create_team,name="create_team"),
    path("manageTeam/<int:auction_id>",manage_teams,name="manage_team"),
    path("manageTeam/d/<int:auction_id>/<int:team_id>",delete_team,name="delete_team"),

    # Categories
    path("categories/<int:auction_id>",add_categories,name="add_categories"),
    
    # Players
    path("player/<int:auction_id>",create_player,name="create_player"),
    path("player/u/<int:auction_id>",upload_from_exel,name="upload_from_exel"),
    path("player/d/<int:player_id>",delete_player,name="delete_player"),
    path("player/e<int:auction_id>/",edit_player,name="edit_player"),
    
    # Dashboard
    path("dash/<int:auction_id>",dashboard,name="dashboard"),
    path("dash/UPlayers/<int:auction_id>",update_dash_players,name="update_dash_players"),


    # Bidding
    path("bid/<int:auction_id>",start_bid,name="start_bid"),
    path("bid/sell/<int:bidding_id>",sell_player,name="sell_player"),
    path("current/bid/<int:auction_id>",update_current_bit,name="update_current_bit"),
    
    # Channels / Pannels
    path("pannel/<int:auction_id>",pannel,name="pannel")
]



# Animation Endpoints
ANIMATION_ENDPOINTS = [
    path("pannel/p/<int:auction_id>/<int:player_id>",show_player_info,name="show_player_info"),
    path("pannel/a/<int:auction_id>",show_auction_info,name="show_auction_info")
]
urlpatterns+=ANIMATION_ENDPOINTS