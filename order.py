# paper trading simulator code

amount = 400
portfolio = 0
money_end = amount
investment = []
transaction_cost = 0.001
portfolio_value = amount


def buy(quantity, price):

    price = round(price, 2)

    global portfolio, money_end, portfolio_value

    allocated_money = quantity * price
    money_end = round(
        money_end - allocated_money - (transaction_cost * allocated_money), 2
    )
    portfolio += quantity

    if investment == []:
        investment.append(allocated_money)
    else:
        investment.append(allocated_money)
        investment[-1] += investment[-2]

    portfolio_value = round(money_end + price, 2)

    # print(f"Bought {quantity} script at {price}")
    # print(f"Portfolio: {portfolio}")
    # print(f"Investment: {investment}")
    print(f"Funds: {money_end}")
    print(f"Portfolio Value: {portfolio_value}")


def sell(quantity, price):

    price = round(price, 2)

    global portfolio, money_end, portfolio_value

    allocated_money = quantity * price
    money_end = round(
        money_end + allocated_money - (transaction_cost * allocated_money), 2
    )
    portfolio -= quantity
    investment.append(-allocated_money)
    investment[-1] += investment[-2]

    portfolio_value = round(money_end, 2)

    # print(f"Sold {quantity} script at {price}")
    # print(f"Portfolio: {portfolio}")
    # print(f"Investment: {investment}")
    # print(f"Funds: {money_end}")
    print(f"Portfolio Value: {portfolio_value}")


price = 90
quantity = 3

# buy(quantity, price)
# buy(2, 100)
# sell(1, 110)
# buy(2, 105)
# sell(3, 110)
# sell(1, 110)


# print(portfolio)
# print(investment)
# print(money_end)
