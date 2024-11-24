from django.contrib import admin
from .models import Auction,Bidding,Team,Player,Category

admin.site.register(Auction)
admin.site.register(Bidding)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Category)