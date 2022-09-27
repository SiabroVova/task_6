from datetime import datetime
from peewee import *

# Creates dict of abb, names, cars, time result and then general dict and sort it
abb_list, gen_list_dict, gen_dict_time, start_list, end_list = [], [], [], [], []

with open('docs/abbreviations.txt', 'r', encoding="utf-8") as f_abb:
    [abb_list.append(line.rstrip()) for line in f_abb]
    abb_list.sort()
with open('docs/start.log', 'r') as f_start:
    [start_list.append(line.rstrip()) for line in f_start]
    start_list.sort()
with open('docs/end.log', 'r') as f_end:
    [end_list.append(line.rstrip()) for line in f_end]
    end_list.sort()

for string in abb_list:
    temp_dict = {}
    index_for_cut = string.find('_', 4)
    temp_dict['abb'] = string[:3]
    temp_dict['name'] = string[4:index_for_cut]
    temp_dict['car'] = string[index_for_cut + 1:]
    gen_list_dict.append(temp_dict)

for time_num in range(len(start_list)):
    temp_dict = {}
    temp_for_dict_index = 0
    temp_dict['time_result'] = str(
        datetime.strptime(
            end_list[time_num][14:], '%H:%M:%S.%f') - datetime.strptime(start_list[time_num][14:], '%H:%M:%S.%f')
    )[:-3]
    gen_dict_time.append(temp_dict)

[gen_list_dict[x].update(gen_dict_time[x]) for x in range(19)]

gen_list_dict_sorted = sorted(gen_list_dict, key=lambda d: d['time_result'])


# Create Database and fill it by data from sorted general dict
db = SqliteDatabase('database.db')


class Drivers(Model):
    id = PrimaryKeyField(unique=True)
    abb = CharField()
    name = CharField()
    car = CharField()
    time_result = CharField()

    class Meta:
        database = db
        db_table = 'drivers'


Drivers.create_table()
with db.atomic():
    Drivers.insert_many(gen_list_dict_sorted).execute()
