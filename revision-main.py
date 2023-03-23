from sortedcontainers import SortedList
from datetime import date, timedelta
# from logging import basicConfig, DEBUG, debug, disable
import shelve
# basicConfig(level=DEBUG, format='%(message)s')

data = shelve.open('data')
# 1st review: 1 day after learning the new information
# 2nd review: 3 days after the 1st review
# 3rd review: 7 days after the 2nd review
# 4th review: 21 days after the 3rd review
# 5th review: 30 days after the 4th review
# 6th review: 45 days after the 5th review
# 7th review: 60 days after the 6th review
review_gaps = [1,3,7,21,30,45,60]
for i in range(1, len(review_gaps)):
    review_gaps[i] += review_gaps[i-1]

# format: revision date, iteration, subject, topic, link, key (for unique identification)
sorted_list_of_items = data['sorted_list_of_items']
unique_key = data['unique_key']

def clear_items_before_today():
    temp = []
    for e in sorted_list_of_items:
        if e[0] < date.today():
            temp.append(e)
        else:
            break
    for e in temp: sorted_list_of_items.discard(e)


def clear_items_key(key):
    temp = []
    for e in sorted_list_of_items:
        if e[-1] == key:
            temp.append(e)
    for e in temp: sorted_list_of_items.discard(e)


def add_revision_item(d):
    global unique_key
    subject = input('Subject: ')
    topic = input('Topic: ')
    link = input('Link/Note: ')

    for i in range(len(review_gaps)):
        sorted_list_of_items.add([
            d + timedelta(days=review_gaps[i]),
            i+1,
            subject,
            topic,
            link,
            unique_key
        ])
    unique_key = unique_key + 1
# a = SortedList()

def fetch_revisions():
    for e in sorted_list_of_items:
        if e[0] == date.today():
            print_rev(e)
        elif e[0] > date.today():
            break


def fetch_all_revisions():
    for e in sorted_list_of_items:
        print_rev(e)

# format: revision date, iteration, subject, topic, link, key (for unique indentification)
def print_rev(e):
    x = e[0].strftime('%d %b, %Y')
    print(f'Date:\t\t{x}')
    print(f'Iteration:\t{e[1]}')
    print(f'Subject:\t{e[2]}')
    print(f'Topic:\t\t{e[3]}')
    print(f'Link/Note:\t{e[4]}')
    print(f'Key:\t\t{e[5]}\n')

if __name__ == '__main__':
    print('1: Add entry')
    print('2: Fetch today\'s revision')
    print('3: Fetch all revision')
    print('4: Clear all items before today')
    print('5: Clear all occurences of a given unique key')
    print('6: Add entry with offset')
    
    choice = int(input('Enter your choice: '))

    if choice == 1:
        add_revision_item(date.today())
    elif choice == 2:
        fetch_revisions()
    elif choice == 3:
        fetch_all_revisions()
    elif choice == 4:
        clear_items_before_today()
    elif choice == 5:
        key = int(input('Key: '))
        clear_items_key(key)
    elif choice == 6:
        offset = int(input('Offset: '))
        add_revision_item(date.today() + timedelta(days=offset))
    else:
        print('Invalid')

    data['sorted_list_of_items'] = sorted_list_of_items
    data['unique_key'] = unique_key
    data.close()
    x = input('Press any key (and enter) to exit...')

