from csv import reader

# wrapper for input to fix python 2/3 compatibility issues
from six.moves import input
from six import next
from json import dumps
from numpy import arange
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


class Student(object):
    def __init__(self, firstName, lastName, email):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.preCampData = defaultdict(dict)
        self.postCampData = defaultdict(dict)
        self.appData = defaultdict(dict)
        self.survey2Dict = {"precamp": self.preCampData,
                            "postcamp": self.postCampData,
                            "application": self.appData}

    def addData(self, year, survey, row, header):

        for idx, el in enumerate(row):
            self.survey2Dict[survey][year][header[idx]] = el.strip()


# A surprisingly ugly way to pretty print a dictionary
# Stolen from Q0
def printOptions(options: dict):
    print(("\n" + dumps(options, indent=4) + "\n")
          .replace('"', '').replace(',', ''))


def parseFile(filename: str, year, survey):
    csvReader = reader(open(filename))
    header = next(csvReader)

    emailCol = header.index("Email Address")
    firstNameCol = header.index("First Name")
    lastNameCol = header.index("Last Name")

    data = {}
    rows = []

    for col in header:
        data[col] = []

    for row in csvReader:
        key = row[firstNameCol].strip() + row[lastNameCol].strip()
        if key in students:
            students[key].addData(year, survey, row, header)
        else:
            student = Student(firstName=row[firstNameCol],
                              lastName=row[lastNameCol], email=row[emailCol])
            student.addData(year, survey, row, header)
            students[key] = student

        for idx, datum in enumerate(row):
            data[header[idx]].append(datum)
        rows.append(row)

    return data, rows

def parseSingleYear():
    print("-------- Which year? --------")
    options = {"a": 2018, "b": 2019, "c": 2020, "d": 2021, "e": 2022}

    printOptions(options)

    year = options[input("Please select option above: ")]

    basePath = "/Users/nayaye/PycharmProjects/sage2021analysis/{YEAR}/{{FORM}}.csv".format(YEAR=year)

    # appFile = basePath.format(FORM="application")
    # appData, appRows = parseFile(appFile, year, "application")
    # print(appData.keys())

    precampFile = basePath.format(FORM="precamp")
    precampData, precampRows = parseFile(precampFile, year, "precamp")

    postcampFile = basePath.format(FORM="postcamp")
    postcampData, postcampRows = parseFile(postcampFile, year, "postcamp")

     # plt.scatter(appData["Zip Code"], appData["Check the highest year of schooling completed by your parent or guardian:"])
     # plt.xticks(rotation=90)
     # plt.show()

    commonHeaders = set(postcampData.keys()).intersection(set(precampData.keys()))

    # commonHeaders.remove("Timestamp")
    commonHeaders.remove("First Name")
    commonHeaders.remove("Last Name")
    commonHeaders.remove("Email Address")
    commonHeaders.remove("High School")


    for commonHeader in commonHeaders:
        x = []
        y1 = []
        y2 = []
        change = []
        changeCount = defaultdict(int)
        for _, student in students.items():
            if not student.preCampData or not student.postCampData:
                    continue
            if (not student.preCampData[year][commonHeader]
                   or not student.postCampData[year][commonHeader]):
                   continue
            if (not student.preCampData[year]
                    or not student.postCampData[year]):
                    continue
            # x.append("{LASTNAME}, {FIRSTNAME}".format(LASTNAME=student.lastName, FIRSTNAME=student.firstName))

            y1.append(student.preCampData[year][commonHeader])
            y2.append(student.postCampData[year][commonHeader])
            try:
                changeCount[polarity[student.postCampData[year][commonHeader].lower()]
                           - polarity[student.preCampData[year][commonHeader].lower()]] +=1
                #change.append(polarity[student.postCampData[year][commonHeader].lower()]
                #             - polarity[student.preCampData[year][commonHeader].lower()])
                #x.append(student.firstName[0] + student.lastName[0])
            except KeyError:
                pass
        x = np.arange(len(changeCount.keys()))  # the label locations
        # width = 0.35  # the width of the bars
        fig, ax = plt.subplots()
        plt.yticks(arange(0, 100, 5.0), rotation=0)
        plt.xlim(-4.5, 4.5)
        plt.ylim(0, 100)
        # ax.bar(x, y1, alpha=0.5, color="c", width=0.1)
        # ax.scatter(x, y1, s=125, label="Pre Camp", alpha=0.5)
        # ax.scatter(x, y2, alpha=0.5, s=250, label="Post Camp")
        # ax.scatter(x, change, s=500)
        # ax.bar(changeCount.keys(), changeCount.values(), zorder=0, ec="black")
        # ax.legend()
        ax.set_ylabel("Count")
        ax.set_xlabel("Change in Positivity")
        plt.suptitle(year)
        plt.title(commonHeader)
        plt.plot()
        # pps = ax.bar(x - width / 2, changeCount.values(), width, label='Total of Students')
        pps = ax.bar(changeCount.keys(), changeCount.values(), color = 'purple', zorder = 0, ec="black")
        for p in pps:
            height = p.get_height()
            ax.annotate('{}'.format(height),
                        xy=(p.get_x() + p.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

        plt.savefig("{YEAR}{NAME}.png".format(NAME=commonHeader, YEAR=year), bbox_inches="tight", dpi=400)
        plt.show()

    # Post camp files either seem preprocessed or don't exist
    # postcampFile = basePath.format(FORM="postcamp")

    print(0)


def parseYOY():
    print(1)


if __name__ == "__main__":

    singleYearKey = "a"
    multiYearKey = "b"

    options = {singleYearKey: "Parse Single Year",
               multiYearKey: "Parse YOY"}
    actions = {singleYearKey: parseSingleYear, multiYearKey: parseYOY}

    print("-------- Parsing Options --------")

    printOptions(options)

    userInput = input("Please select option above: ")

    while userInput not in actions.keys():
        userInput = input("Please select option above: ")

    students = {}
    polarity = {"strongly agree": 2, "somewhat agree": 1, "i do not know": 0,
                "somewhat disagree": -1, "strongly disagree": -2}

    actions[userInput]()
