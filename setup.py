from sortedcontainers import SortedList
import shelve

data = shelve.open('data')

sorted_list_of_items = SortedList()
data['sorted_list_of_items'] = sorted_list_of_items
data['unique_key'] = 0

data.close()
