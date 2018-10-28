import csv

def get_data():
    FILE_NAME = "data/bookmark_list.csv"
    with open(FILE_NAME,'r') as csvfile:
        data_list = csv.reader(csvfile,delimiter=',',quotechar='"')
        result = list(data_list)

    return result

if __name__ == "__main__":
    print(get_data())