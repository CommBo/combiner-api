import os
import csv

DISTRICT_FILE_PATH = os.path.join(os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir)), 'cong_district.txt')

def get_district_ids():
    district_ids = set()
    with open(DISTRICT_FILE_PATH, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            district_ids.add(row['district'])
    return sorted(list(district_ids))


def district_to_zip_codes(district_id):
    zip_codes = []
    with open(DISTRICT_FILE_PATH, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['district'] == district_id:
                zip_codes.append(row['zip'])
        return sorted(zip_codes)
