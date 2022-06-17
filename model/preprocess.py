import csv
import os

with open('archive/styles.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            path = "dataset/" + row[3]
            # try:
            #     os.mkdir(path)
            # except OSError:
            #     print ("Creation of the directory %s failed" % path)
            # else:
            #     print ("Successfully created the directory %s " % path)
            originalPath = "archive/images/" + row[0] + ".jpg"
            destinationPath = "dataset/" + row[3] + "/" + row[0] + ".jpg"
            print(f'{originalPath} to {destinationPath}')
            try:
                os.rename(originalPath, destinationPath)
            except OSError:
                print("error")
        line_count += 1
    print(f'Processed {line_count} lines.')