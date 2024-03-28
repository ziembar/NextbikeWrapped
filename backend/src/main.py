import defs

cookie = defs.get_cookie("48123123123", "123123")

rents = defs.get_events(cookie)

frents = defs.filter_by_season(rents, 2024)


defs.total_rides(frents)

defs.top_frequent_rides(frents)


# print(frents)
# print(defs.total_time(rents['rentals']))
print(defs.money_spent(frents))