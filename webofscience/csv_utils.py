import csv
from webofscience.author import Author

class CsvUtils:

    def read_csv(self, path):
        with open(path, 'r') as f:
            csv_reader = csv.reader(f)
            old_authors = []
            csv_reader.__next__()
            for line in csv_reader:
                if len(line) > 1:
                    for i in range(1, len(line)):
                        line[0] += line[i]
                splitted_line = line[0].split(";")
                old_authors.append(Author(splitted_line[0], splitted_line[1], splitted_line[2]))
        return old_authors


    def write_csv(self, list, filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for author in list:
                writer.writerow([author.email, author.article, author.date])
            f.close()
