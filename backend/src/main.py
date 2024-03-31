import db_actions
import defs
from Models import Station, Path, getDriver
import db_actions
import defs
from Models import Station, Path, getDriver
from decouple import config



cookie = defs.get_cookie(config('TEST_NUMBER'), config('TEST_PIN'))

rents = defs.get_events(cookie)

frents = defs.filter_by_season(rents, 2024)



defs.total_distance(frents)

# defs.total_rides(frents)

# defs.top_frequent_rides(frents)


# # print(frents)
# # print(defs.total_time(rents['rentals']))
# print(defs.money_spent(frents))



# s1 = Station.nodes.filter(lat__startswith=52.1444, lng__startswith=21.0519)[0]
# s2 = Station.nodes.filter(lat__startswith=52.1420, lng__startswith=21.0660)[0]
# rel = s1.stations.connect(s2, {'distance':  2000, 'time': 7})

# a=db_actions.find_station_by_coordinates(getDriver(), 52.281039, 20.958925)
# # db_actions.add_distance_relation(getDriver(), 52.276877, 20.94813, 52.281039, 20.958925, 20120, 70)
# for v in a.values():
#     print(v, '\n')

# getDriver().close()

