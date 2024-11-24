# Addmin Views
from .views.dashboard import dashboard,update_dash_players
from .views.create_auction import create_auction,auction,delete_team,manage_teams,create_team,add_categories,delete_player,create_player,edit_player,upload_from_exel

# Bidding

from .views.bidding import start_bid,sell_player,update_current_bit

# Channels
from .views.pannels import pannel,show_player_info,show_auction_info