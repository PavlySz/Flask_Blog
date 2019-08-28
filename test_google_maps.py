import googlemaps 
import os

# Requires API key 
gmaps = googlemaps.Client(key='AIzaSyA0UxBztBE0FGFdVDn-14uU5mcJUKUoRvg') 
  
# Requires cities name 
my_dist = gmaps.distance_matrix('Cairo Governerate, Egypt','Alexandria Governerate, Egypt')['rows'][0]['elements'][0] 
  
# Printing the result 
print(my_dist)