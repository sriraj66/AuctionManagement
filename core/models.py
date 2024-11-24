from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    auction = models.ForeignKey('Auction',verbose_name="Auction",on_delete=models.CASCADE,blank=True)
    name = models.CharField(max_length=255,verbose_name="Category Name")
    short_name = models.CharField(max_length=255,verbose_name="Category Name")
    base_price = models.PositiveIntegerField(verbose_name="Base Price")
    limit_count = models.PositiveIntegerField(verbose_name="Limit Count")
    
    def __str__(self) -> str:
        return self.name
    
class Auction(models.Model):
    
    AUCTION_TYPE = (("OPEN","OPEN"),("PENDING","PENDING"),("CLOSED","CLOSED"))
    
    SPORTS_TYPE = (
        ("CRICKET","CRICKET"),
        ("FOOTBALL","FOOTBALL"),
        ("KABADI","KABADI"),
        ("HOCKEY","HOCKEY"),
        ("VOLLYBALL","VOLLYBALL"),
        ("SHUTTLECOCK","SHUTTLECOCK"),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Admin User")
    
    auction_name = models.CharField(max_length=255,verbose_name="Auction Name")
    sports_type = models.CharField(max_length=255,choices=SPORTS_TYPE,default=0,verbose_name="Sports Type")
    auction_type = models.CharField(max_length=100,choices=AUCTION_TYPE,default=0,verbose_name="Auction Type")
    
    starting_date = models.DateTimeField(verbose_name="Starting Date")
    ending_date = models.DateTimeField(verbose_name="Ending Date")
    
    auction_place = models.CharField(max_length=200,verbose_name="Auction Place")
    
    # Teams
    squad_limit = models.PositiveIntegerField(verbose_name="Squad Limit")
    team_purse = models.PositiveIntegerField(verbose_name="Team Purse")

    # Bidding
    current_bid_id = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.auction_name + " "+ self.auction_place

    class Meta:
        ordering = '-id',

    def current_bid(self):
        if self.current_bid_id == 0:
            return False
        else:
            return Bidding.objects.get(id=self.current_bid_id)
    
    def player_count(self):
        return Player.objects.filter(auction = self.auction)
    

class Team(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Admin User")
    
    team_name = models.CharField(max_length=255,verbose_name="Team Name")
    team_short_name = models.CharField(max_length=50,verbose_name="Short Name")
    owner_name = models.CharField(max_length=255,verbose_name="Owner Name")
    team_logo = models.ImageField(upload_to="TeamLogos/")

    auction = models.ForeignKey('Auction',on_delete=models.CASCADE,blank=True)
    
    purse = models.PositiveIntegerField(default=0,verbose_name="Team Purse")
    
    used_amount = models.PositiveIntegerField(default=0,verbose_name="Used Amount")
    
    max_bid = models.PositiveIntegerField(default=0,verbose_name="Max Bid")
    
    
    def player_count(self):
        return Player.objects.filter(auction = self.auction,player_team=self.id).count()
    
    def balance(self):
        return self.purse - self.used_amount
    
    def __str__(self) -> str:
        return self.team_name

class Player(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Admin User")
    player_name = models.CharField(max_length=255,verbose_name="Player Name")
    player_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    player_image = models.URLField(verbose_name="Profile Image",default="https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png")
    mpl_id = models.CharField(unique=True,verbose_name="MPL ID",max_length=255,blank=True,null=True)
    player_age = models.PositiveIntegerField(verbose_name="Age")
    player_village = models.CharField(max_length=255,verbose_name="Village Name",blank=True)
    
    player_role = models.CharField(max_length=255,verbose_name="Player Role")
    
    player_matches = models.PositiveIntegerField(verbose_name="Player Total Matches")
    
    auction = models.ForeignKey('Auction',verbose_name="Auction",on_delete=models.CASCADE,blank=True)
    player_team = models.ForeignKey(Team,on_delete=models.CASCADE,blank=True,null=True,verbose_name="Player Team")
    # Batting
    player_bat_matches = models.PositiveIntegerField(verbose_name="Player Matches on Bat")
    player_bat_runs = models.PositiveIntegerField(verbose_name="Player Runs on Bat")
    player_30s = models.PositiveIntegerField(verbose_name="Player 30s")
    player_50s = models.PositiveIntegerField(verbose_name="Player 50s")
    player_100s = models.PositiveIntegerField(verbose_name="Player 100s")
    player_max = models.PositiveIntegerField(verbose_name="Player High Score")
    # Bowling
    player_wickets = models.PositiveIntegerField(verbose_name="Player wickets")
    player_bowl_runs = models.PositiveIntegerField(verbose_name="Player Bowling Runs")

    player_economy = models.PositiveIntegerField(verbose_name="Player Economy")
    player_bowl_matches = models.PositiveIntegerField(verbose_name="Player Matches on Bowl")
    player_miden = models.PositiveIntegerField(verbose_name="Player Miden overs")
    player_hattrick = models.PositiveIntegerField(verbose_name="Total Hattrick",default=0)
    
    is_sold = models.BooleanField(default=False, verbose_name="Is Solded")
    is_bidded = models.BooleanField(default=False,verbose_name="Is Bidded")
    
    def __str__(self) -> str:
        return self.player_name + " " + self.player_role
    def bat_avg(self):
        try:
            return round(self.player_bat_runs/self.player_bat_matches,2)
        except Exception as e:
            print(e)
            return 0
        
    def bidding(self):
        
        bidds = Bidding.objects.filter(auction=self.auction,player=self.id)
        if(len(bidds)!=0):
            return bidds[0]
        else:
            return False
        
    def bid_status(self):
        biddings = Bidding.objects.filter(auction=self.auction,player=self.id).order_by("-id")
        
        if len(biddings)!=0:
            if biddings[0].is_sold == True:
                return "Sold"
            else:
                return "Un Sold"
        else:
            return "No Bid"
        
        
                
    def bowl_avg(self):
        try:
            return round(self.player_bowl_runs/self.player_bowl_matches,2)
        except Exception as e:
            print(e)
            return 0
    



class Bidding(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Admin User")
    auction = models.ForeignKey(Auction,on_delete=models.CASCADE,verbose_name="Auction")
    team = models.ForeignKey(Team,on_delete=models.CASCADE,verbose_name="Team",blank=True,null=True)
    player = models.ForeignKey(Player,on_delete=models.CASCADE,verbose_name="Player ")
    price_track = models.TextField(default="")
    curent_price = models.PositiveIntegerField(verbose_name="Current Price")
    is_sold = models.BooleanField(default=False)
    
    def getPriceTrack(self):
        return self.price_track.split(":")
    
    def setPrice(self,price):
        self.curent_price = price
        track = self.getPriceTrack().append(str(price))
        self.price_track = ":".join(track)
        self.save()
        
    def undoPrice(self):
        try:
            price_track = self.getPriceTrack()
            price_track.pop()
            self.curent_price = int(price_track[-1])
            self.price_track = ":".join(price_track)
        except Exception as e:
            print(e)
            self.curent_price = self.player.player_category.base_price
        finally:
            self.save()
    
    def reset(self):
        self.curent_price = self.player.player_category.base_price
        self.save()
    
