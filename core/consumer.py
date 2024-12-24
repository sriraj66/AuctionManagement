from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import asyncio, json
from asgiref.sync import sync_to_async

async def async_broadcast_message_to_auction(auction_id, data, typ=1):
    """
    Asynchronous function to broadcast messages to the auction room.
    """
    try:
        TYPES = ["INIT", "MESSAGE", "BIDDING", "CLOSE"]
        
        if typ < 0 or typ >= len(TYPES):
            raise ValueError("Invalid message type")

        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            f'auction_{auction_id}',
            {
                'type': f'type_{TYPES[typ]}',
                'data': data
            }
        )
    except Exception as e:
        print("Async Error:", e)


def broadcast_message_to_auction(auction_id, data, typ=1):
    """
    Synchronous wrapper to send broadcast messages.
    Uses asyncio.run() to execute the async function in a synchronous context.
    """
    try:
        asyncio.run(async_broadcast_message_to_auction(auction_id, data, typ))
    except RuntimeError as e:
        print("Error running async function:", e)


class AuctionConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.room_group_name = f'auction_{self.auction_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        player_id = data.get('player_id')
        price = data.get('price')
        
        player = await self.get_player(player_id)
        
        print(f"Player Name: {player[0].player_name}, Price: {price}")

        await async_broadcast_message_to_auction(
            self.auction_id,
            data={
                "message": f"Price Updated {price} for {player[0].player_name}",
                "player": player[1],
                "price": price
            },
            typ=2
        )

    async def type_INIT(self, event):
        message = event['data']
        await self.send(text_data=json.dumps({'type': 'INIT', 'data': message}))

    async def type_MESSAGE(self, event):
        message = event['data']
        await self.send(text_data=json.dumps({'type': 'MESSAGE', 'data': message}))

    async def type_BIDDING(self, event):
        message = event['data']
        await self.send(text_data=json.dumps({'type': 'BIDDING', 'data': message}))

    async def type_CLOSE(self, event):
        await self.send(text_data=json.dumps({'type': 'CLOSE', 'data': "Connection Closed From Client"}))
        print("Connection Closed")
        await self.close()
        
    @sync_to_async(thread_sensitive=True)
    def get_player(self, player_id):
        from .models import Player
        from .views.serializers import PlayerSerializer
        
        try:
            player = Player.objects.get(id=int(player_id))
            player_data = PlayerSerializer(player).data
            return (player,player_data)
        except Player.DoesNotExist:
            return None