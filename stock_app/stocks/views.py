from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import config
import yfinance as yf
import datetime 
from .models import Room, Membership,Transaction, Saved_Stock 
from django.template.defaulttags import register
from decimal import Decimal

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Create your views here.
@csrf_exempt
def index(request):
    """View function for home page of site."""
    context={}
    if request.user.id:
        user = User.objects.filter(id=request.user.id)[0]
        rooms = Room.objects.filter(members=user)
        room_admins= Membership.objects.filter(room__in=rooms,creator=True)

        memberships = Membership.objects.filter(user=user)
        context = {"rooms":rooms, "memberships":memberships,"admins":room_admins}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
@login_required
def game_lobby(request,room):
    # room info - all members ranks asset value
    curr_room = Room.objects.filter(name=room)[0]
    members = Membership.objects.filter(room=curr_room).order_by('-total_asset_value','-stock_value','-cash_remaining')
    
    for member in members:
        # get all transactions per member
        member_trans = Transaction.objects.filter(member=member.id)
        
        new_stock_value = 0
        if not member_trans:
            continue 
        # update asset values
        for item in member_trans:
            ticker = item.ticker
            quote = yf.Ticker(ticker)
            data = quote.history(period="1day")
            price = data.iloc[0]['Close']
            paper_value = price * item.quantity
            new_stock_value += paper_value
        TWOPLACES = Decimal(10) ** -2     
        member.stock_value = Decimal(new_stock_value).quantize(TWOPLACES)
        member.total_asset_value = member.stock_value + member.cash_remaining
        member.save()
        # update stock value and total value 

    # update ranks
    prior_mbr = ""
    for idx,member in enumerate(members):
        if idx == 0: 
            pass
        elif prior_mbr.total_asset_value == member.total_asset_value:
            member.rank = prior_mbr.rank
            member.save()
            prior_mbr = member
            continue
        member.rank = idx + 1
        member.save()
        prior_mbr = member
    

    context = {"room":curr_room, "members":members}
    return render(request, 'game.html', context=context)

@login_required
def game_portfolio(request,room,user):
    curr_room = Room.objects.filter(name=room)[0]
    curr_user = User.objects.filter(username=user)[0]
    member = Membership.objects.filter(room=curr_room,user=curr_user)[0] 
    transactions = Transaction.objects.filter(member=member)
    price_dict = {}

    ## need to combine multiple buys from the same stock - weighted average price 
    ## and click to open each purchase record
    new_stock_value = 0
    for item in transactions:
        ticker = item.ticker
        quote = yf.Ticker(ticker)
        data = quote.history(period="1day")
        price = data.iloc[0]['Close']
        price_dict[ticker] = price
        paper_value = price * item.quantity
        new_stock_value += paper_value
    TWOPLACES = Decimal(10) ** -2     
    member.stock_value = Decimal(new_stock_value).quantize(TWOPLACES)
    member.total_asset_value = member.stock_value + member.cash_remaining
    member.save()
    print(price_dict)
    context = {"room":curr_room, "user":curr_user,"price_dict":price_dict ,"totals":member,"transactions":transactions}
    return render(request, "game-portfolio.html",context=context)


def register(request):
    if request.method == "GET":
        print("get register")
        # access register.html
        return render(request, "register.html")

    if request.method == "POST":
        # after user submits information -> save to db
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]

        # user object for django ORM

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # go back to index page
        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    # user wants to log in to make order - authenticate user credentials
    if request.method == "GET":
        # access login page
        return render(request, "login.html")

    if request.method == "POST":
        # when user provides info - check against User table with django/authenticate()
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # success --> go to index
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            # fail --> stay on login
            return HttpResponseRedirect(reverse("login"))


def logout_view(request):
    # end user session --> go back to main menu page
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
@csrf_exempt
def create_game(request):
    """View function for home page of site."""
    context = {}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'create-game.html', context=context)

@login_required(login_url='login')
def join_game(request):
    """View function for home page of site."""
    # get all rooms in db -- save to context
    rooms = Room.objects.all()
    user = User.objects.filter(id=request.user.id)[0]
    rooms = rooms.exclude(members=user)
    admin = Membership.objects.exclude(creator=False)
    context = {"rooms":rooms,"admins":admin}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'join-game.html', context=context)

@login_required(login_url='login')
def portfolio(request):
    """View function for users saved stocks portfolio ."""

    # provide information as JSON for html file to use
        # need saved stocks that current user has saved
    user = User.objects.filter(id=request.user.id)[0]
    saved_stocks = Saved_Stock.objects.filter(user=user)
    tickers = saved_stocks.values_list('ticker', flat=True).distinct()
    # print(tickers)
    context = {"stocks_exist": False,
               "stocks": saved_stocks,
               "prices": {},
               "percent": {}}
    for ticker in tickers:
        old_price = saved_stocks.filter(ticker=ticker).values_list('initial_price',flat=True)[0]   
        # get new data
        quote = yf.Ticker(ticker)
        data = quote.history(period="1day")
        new_price = data.iloc[0]['Close']
        # calculate percent change
        float_percent = (new_price - float(old_price))/float(old_price) * 100
        percent = float("{:.2f}".format(float_percent))
        #  save to JSON context
        context['prices'][ticker] = new_price
        context['percent'][ticker] = percent
    print(context)
    # Render the HTML template portfolio.html with the data in the context variable
    return render(request, 'portfolio.html', context=context)

@login_required(login_url='login')
def buy_sell(request,room,user,bs):
    context = {"transaction":bs}
    context['room'] = room

    # if user specified a stock to trade
    if request.META['QUERY_STRING']:
        # add users total value, cash and stock values to context
        curr_room = Room.objects.filter(name=room)[0]
        curr_user = User.objects.filter(username=user)[0]
        member = Membership.objects.filter(room=curr_room,user=curr_user)[0] 
        context['member'] = member
        if bs == "sell":
            # split ticker and max quantity
            query_list = request.META['QUERY_STRING'].split("&")
        else:
            # get stock ticker
            query_list = []
            query_list.append(request.META['QUERY_STRING'])
        ticker =  query_list[0].split("=")[1]
        stock = yf.Ticker(ticker)
        data = stock.history(period="1day")
        
        # check if market is actually open
        current_datetime = datetime.datetime.now()
        market_open = datetime.time(9,30,00)
        market_closed = datetime.time(16,30,00)
        
        if (current_datetime.time() <= market_open or current_datetime.time() > market_closed) or int(data.iloc[0]['Volume']) == 0 or data.index[0].date() != current_datetime.date():
            context['error'] = "Markets are currently closed. Transactions cannot be processed today: Please go back to your portfolio. :C"
            return render(request,'buy-sell.html',context=context)
        
        # if stock exists
        elif not data.empty:
            context['stock'] = ticker 
            current_price = data.iloc[0]['Close']
            context['price'] = current_price

            if bs == "buy":
                max_buy = member.cash_remaining // Decimal(current_price)
                context['max'] = max_buy
        else:
            context['error'] = "Error in stock ticker: Please go back to your portfolio."
            return render(request,'buy-sell.html',context=context)

    return render(request, 'buy-sell.html',context=context)


@csrf_exempt
def get_quote(request):
    # delete order made by users
    if request.method == "GET":
        return HttpResponseNotAllowed()
    print(request.POST)
    ticker = request.POST['ticker']
    current_time = datetime.datetime.now()
    quote = yf.Ticker(ticker)
    data = quote.history(period="1day")
    # print(data)

    if data.empty:
        print("empty data frame")
        # error in ticker query
        response = {"quote":False,"message":"Stock not found."}
        return JsonResponse(response, safe=False)
    response = {"quote":True,
			   "ticker":ticker,
			   "price":data.iloc[0]['Close'],
			   "date":current_time.strftime("%x"),
			   "time":current_time.strftime("%X"),
			   "quantity":data.iloc[0]['Volume']}
    return JsonResponse(response, safe=False)

@csrf_exempt
def add_portfolio(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()
    # check if data is valid stock info
    data_check = request.POST['quote']
    if not data_check:
        response = {"quote":False,"message":"Error with data"}
        return JsonResponse(response, safe=False)

    # get data from request
    user = User.objects.filter(id=request.user.id)[0]
    date = str(datetime.datetime.now())
    ticker = request.POST['ticker']
    price = request.POST['price']

    # save data to db
    new_stock = Saved_Stock(user=user,date_added=date,ticker=ticker,initial_price=price)
    new_stock.save()
    response = {"quote":True, "message":"Data Saved"}
    return JsonResponse(response, safe=False)

@csrf_exempt
def remove_saved(request):
    # if request.method == "GET":
    #     return HttpResponseNotAllowed()
    # get request info
    user_id = request.POST['userid']
    ticker = request.POST['ticker']
    print(request.POST['userid'],request.POST['ticker'])
    # get table objects
    user = User.objects.filter(id=user_id)[0]
    stock = Saved_Stock.objects.filter(user=user,ticker=ticker)[0]
    print(stock.user,stock.ticker,stock.initial_price,stock.date_added)
    # remove stock from db
    stock.delete()

    # return JSON Reponse
    response = {"deleted":True,"remove":ticker,"user":user_id}
    return JsonResponse(response,safe=False)

@csrf_exempt
def create_newgame(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()
    else:
        # get data
        name = request.POST['room-name']
        players = request.POST['room-players']
        start_value =  float(request.POST['room-value'])
        # check if room name exists
        check_rooms = Room.objects.filter(name=name)
        # if check_rooms is empty:
        response = {}
        if check_rooms.exists():
            response = {"quote":False,"message":"creategame room already exists {0},{1}".format(name,players)}

            # return false
        else:
        # create new room
            date = datetime.datetime.now()
            new_room = Room(name=name,create_date=date,max_users=int(players),starting_value=start_value)
            new_room.save()
            response = {"quote":True,"name":name,"message":"room created. you are now the admin"}
            # add current user as admin in membership
            user = User.objects.filter(id=request.user.id)[0]
            room = Room.objects.filter(name=name)[0]
            make_admin = Membership(user=user,room=room,creator=True,
                                    date_join=date,total_asset_value=start_value,rank=1)
            make_admin.save()

        # return json response
        return JsonResponse(response, safe=False)


@csrf_exempt
def user_join(request):
    if request.method == "GET":
        return HttpResponseNotAllowed()
    room = Room.objects.filter(name=request.POST['room'])
    user = User.objects.filter(id=request.user.id)
    date =datetime.datetime.now()
    check_room = Membership.objects.filter(user=user[0],room=room[0])
    if check_room.exists():
        # check if user already in room --> return error response
        print(check_room)
        response = {"quote":False,"msg":"User Already in Room, Please go to Homepage.","room":room[0].name}
    else:
        # add to room with default starting value
        start_val = room[0].starting_value
        print(start_val)
        new_member = Membership(user=user[0],room=room[0],creator=False,date_join=date,total_asset_value=start_val)
        new_member.save() 
        response = {"quote":True,"msg":"User added to {}".format(room[0].name),"room":room[0].name}
    # return response
    return JsonResponse(response, safe=False)

@login_required
@csrf_exempt
def new_transaction(request):
    print(request.POST)
    context = {}

    tickername = context['ticker'] = request.POST['ticker']
    roomname = context['room'] = request.POST['room']
    username = context['user'] = request.POST['user']
    tr_type = context['tranaction'] = request.POST['transaction']
    quantity = int(request.POST['quantity'])
    price = Decimal(request.POST['price'])

    # call ORM models and update the transaction
    room = Room.objects.filter(name=roomname)
    user = User.objects.filter(username=username)
    member = Membership.objects.filter(user=user[0],room=room[0])[0]
    date = datetime.datetime.now()
    # stop transaction if market is closed
    try:
        if tr_type == "buy":
            # separate buy new stock and buy more stock
            check_tr = Transaction.objects.filter(member=member,ticker=tickername)
            if not check_tr:
                # update member cash remaining
                buy_transaction = Transaction(member=member,quantity=quantity,price=price,
                                              ticker=tickername,date=date)
                buy_transaction.save()
            else:
                buy_transaction = check_tr[0]
                buy_transaction.price = ((buy_transaction.quantity * buy_transaction.price)+(quantity * price))/(buy_transaction.quantity + quantity)     
                buy_transaction.quantity += quantity
                buy_transaction.save()
            member.cash_remaining -= quantity * price
            member.save()
            context['tr_success'] = True
        elif tr_type == "sell":
            # get_tranaction
            sell_transaction = Transaction.objects.filter(member=member,ticker=tickername)[0]
            sell_transaction.quantity -= quantity
            sell_transaction.save()
            # update membership cash remaining
            member.cash_remaining += quantity * price
            member.save() 
            if sell_transaction.quantity == 0:
                # delete record
                sell_transaction.delete()
            context['tr_success'] = True
    except:
        context['tr_success'] = False 

    # tell user if success or error in transaction html page and to go back to portfolio to start over
    # success --> you have bought/sold {quantity} {stock} at {price} == {total} --> show new {user} {totals} in {room} 
    # error  --> some error --> button to go back to portfolio


    return render(request, 'transaction.html',context=context)
