from rest_framework import serializers
from ..models import Player, Team, Auction, Category, Bidding
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    auction = serializers.StringRelatedField()

    class Meta:
        model = Category
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    auction = serializers.StringRelatedField()

    class Meta:
        model = Team
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    player_category = CategorySerializer()
    player_team = TeamSerializer()
    auction = serializers.StringRelatedField()

    class Meta:
        model = Player
        fields = '__all__'

class AuctionSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    # category_set = CategorySerializer(many=True, read_only=True)
    # player_set = PlayerSerializer(many=True, read_only=True)
    team_set = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

class BiddingSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)
    team_set = TeamSerializer(read_only=True)
    
    class Meta:
        model = Bidding
        fields = '__all__'
