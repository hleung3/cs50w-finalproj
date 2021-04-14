import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_app.settings')
import django
django.setup()

from stocks.models import Room, Membership, Saved_Stock, Transaction
from django.contrib.auth.models import User

from decimal import Decimal
import datetime 
import random
import yfinance as yf

# populate db with users, rooms, link with memberships, and create transactions


new_username = ["bob","ryu","andy","leo","nick","jake","gandalf","stan","kyle","cartman","kenny",
                "bart","homer","lisa","maggie","marge","winnie","karen","shirley","sabrina","ann"]

new_rooms = ["my_game","newgame","winners_only","wallstreetbets"]

stock_list = ["MAXR","TSLA","GOOG","MSFT","NFLX","AAPL","BNO","SAN","WFC","CM",
              "AMZN","SNAP","FB","TWTR","WMT","CVX","CME","JNJ","WM","MA","ECL","AMT",
              "NEE","MMM","AXP","BA","CAT","CSCO","KO","DIS","DOW","XOM","CS","HD","IBM",
              "INTC","JPM","MCD","MRK","NKE","PFE","PG","TRV","UNH","VZ","V","WBA","COST"] 


# create new users
try:
    for username in new_username:
        new_user = User.objects.create_user(username=username,
                                            password=username+"123",
                                            email=username+"@email.com",
                                            first_name=username)
        new_user.is_superuser = False
        new_user.is_staff = False
        print(new_user.email)
        new_user.save()
except django.db.utils.IntegrityError:
    print("error: users already exist")
    pass


# create new rooms
try:
    for name in new_rooms:
        date = datetime.datetime.now()
        room = Room(name=name,create_date=date,max_users=25)
        room.save()
        print(room.create_date)
except django.db.utils.IntegrityError:
    print("error: room already exist")
    pass
# name,create_date,max_users, starting_value



# link user with rooms
# for each user - random generate n room names and link them
# user, room, creator?, date_join, total_asset_value, rank
try:
    for room in new_rooms:
        curr_room = Room.objects.filter(name=room)[0]
        # select random number of users from new_users list
        room_users = random.sample(new_username,random.randint(1,len(new_username)))
        # select a random user from selected as admin
        admin = random.choice(room_users)
        for user in room_users:
            date = datetime.datetime.now()
            # create membership instance
            curr_user = User.objects.filter(username=user)[0]
            # add new member - since user & room are FK, 
            # cannot be added if the combination alrady exists
            new_member = Membership(user=curr_user,room=curr_room,date_join=date)
            new_member.save()
            if user == admin:
                # set this user as admin
                new_member.creator = True
                new_member.save(update_fields=['creator'])
    print("added memberships")
except django.db.utils.IntegrityError:
    print("error: membership already exist")
    pass




# create transactions
for room in Room.objects.all():
    break
    # get members of each room:
    room_users = room.members.all()
    for user in room_users:
        print(user)
        member_data = Membership.objects.filter(user=user,room=room)[0]
        stocks = random.sample(stock_list,5)

        # user can only buy a number less than his remaining cash value
        for stock in stocks:
            cash = member_data.cash_remaining
            print(cash)
            date = datetime.datetime.now()
            
            # get stock price and make transaction 
            quote = yf.Ticker(stock)
            data = quote.history(period="1day")
            current_price = Decimal(data.iloc[0]['Close'])
            # quantity is based on how much cash on hand, min buy 1 stock
            quantity = int((Decimal(cash)/current_price) * Decimal("0.1"))
            if quantity == 0:
                print("qty is 0") 
                continue
            print(date,stock,current_price,quantity)
            user_trnsactn = Transaction(member=member_data,quantity=quantity,
                                        price=current_price,date=date,ticker=stock) 
            user_trnsactn.save()

            # update user's remaining cash value and stock value
            member_data.cash_remaining -= current_price * quantity
            member_data.stock_value += current_price * quantity
            member_data.save()            
            print("cash remaining", member_data.cash_remaining,member_data.stock_value)


