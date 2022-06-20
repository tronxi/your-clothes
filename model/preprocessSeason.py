import csv
import os
import shutil

with open('archive/styles.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    errors = 0
    labels = set()
    for row in csv_reader:
        if line_count != 0:
            # path = "season/" + row[6]
            # try:
            #     os.makedirs(path)
            # except OSError:
            #     print ("Creation of the directory %s failed" % path)
            # else:
            #     print ("Successfully created the directory %s " % path)

            # originalPath = "archive/images/" + row[0] + ".jpg"
            # destinationPath = "season/" + row[6] + "/" + row[0] + ".jpg"
            # print(f'{originalPath} to {destinationPath}')
            # try:
            #     shutil.copy(originalPath, destinationPath)
            # except Exception:
            #     print("error")
            #     errors += 1
            labels.add(row[6])
        line_count += 1
    for label in labels:
        list = os.listdir("season/" + label)
        number_files = len(list)
        print(label, number_files)
    print(f'Processed {line_count} lines.')
    print("errores", errors)