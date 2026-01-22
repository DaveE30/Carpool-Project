# use highway_miles, city_miles, midway_miles and combined mpg, highway mpg, city mpg to calculate trip cost in cost_calculations.py and divide it by the number of passengers
def calculate_trip_cost(highway_miles, city_miles, midway_miles, highway_mpg, city_mpg,combined_mpg, passenger):
   
   cost_of_gas = 2.83
   highway_gas = (  float(highway_miles) / highway_mpg) * cost_of_gas
   city_gas    = (     float(city_miles) /    city_mpg) * cost_of_gas
   midway_gas  = (   float(midway_miles) / combined_mpg) * cost_of_gas
   total_fuel_cost = highway_gas + city_gas + midway_gas
   passenger_cost = total_fuel_cost/passenger  # Assuming 1 passenger for now
   return cost_of_gas, highway_gas, city_gas, midway_gas, total_fuel_cost, passenger_cost


