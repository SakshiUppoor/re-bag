from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Auction, Item
from datetime import timedelta

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        auction = Auction.objects.get(id=int(data['auction_id']))
        messages = Message.objects.filter(auction=auction)
        content = {
            'messages': self.messages_to_json(messages),
            'command': 'messages'
        }
        self.send_message(content)

    def new_message(self, data):
        sender = data['from']
        sender_user = User.objects.get(email=sender)
        auction_id = int(data['auction_id'])
        auction = Auction.objects.get(id=auction_id)
        current_price = auction.item.current_price
        message = Message.objects.create(
            sender=sender_user,
            price=data['price'],
            auction=auction
        )
        message.save()
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def fetch_items(self, data):
        print(data)
        sender = data['from']
        sender_user = User.objects.get(email=sender)
        auction = Auction.objects.get(id=int(data['auction_id']))
        items = Item.objects.filter(buyer=sender_user)
        content = {
            'items': self.items_to_json(items),
            'command': 'items'
        }
        self.send_message(content)

    def new_item(self, data):
        sender = data['from']
        sender_user = User.objects.get(email=sender)
        auction_id = int(data['auction_id'])
        auction = Auction.objects.get(id=auction_id)
        item = auction.item
        item.buyer = sender_user
        item.save()
        content = {
            'command': 'new_item',
            'item': self.item_to_json(item)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.sender.id,
            'sender': message.sender.first_name + " " + message.sender.last_name,
            'profile_image': message.sender.image.url,
            'price': message.price,
            'timestamp': str((message.time_stamp +
                              timedelta(hours=5.5)).strftime("%H:%M")),
        }

    def items_to_json(self, items):
        result = []
        for item in items:
            result.append(self.item_to_json(item))
        return result

    def item_to_json(self, item):
        return {
            'name': item.item_name,
            'item_image': item.item_images.first().image.url,
            'price': item.current_price,
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'fetch_items': fetch_items,
        'new_item': new_item,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        if data['command'] in self.commands:
            self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
