import RateMyProfessorAPI, requests, re

class ASUClassFinder:
    def __init__(self, major, code):
        self.major = major
        self.code = code
        self.baseUrl = "https://webapp4.asu.edu/catalog/myclasslistresults?t=2197&s=%s&n=%s&hon=F&promod=F&e=open&page=1" % (major, code)
        self.Page = self._getPage()
        self.totalResult = self.getElementsCount()

    def _getPage(self):
        res = requests.get(self.baseUrl, headers=headers)
        return res

    def getElementsCount(self):
        available = etree.HTML(self.Page.text)
        everyThing = str(available.xpath('//*[@id="classResults"]/div[3]/div/text()'))
        totalResults = re.findall(r'of \d+', everyThing)[0]
        totalResult = int(re.findall(r'\d+', totalResults)[0])
        return totalResult

    def __str__(self):
        response = ""
        available = etree.HTML(self.Page.text)
        if self.totalResult > 0:
            for count in range(0, self.totalResult):
                if count == 0:
                    classNumberString = str(available.xpath('//*[@id="Any_13"]/text()'))
                    classNumber = re.findall(r'\d+', classNumberString)[0]
                    seatsOpenString = str(available.xpath('//*[@id="informal"]/td[11]/div/div[1]/text()'))
                    seatsOpen = re.findall(r'\d+', seatsOpenString)[0]
                    instructor = str(available.xpath('//*[@id="DirectLink"]/span/text()'))
                    instructorFullString = re.findall(r'<a id="DirectLink" title="Instructor\|.*?"', self.Page.text)

                    if instructor == "[]":
                        inst = "staff"

                    else:
                        inst = re.findall(r'[^\\t]\w+', instructor)[0]

                    if len(instructorFullString) > 0:
                        instructorFullString = str(instructorFullString[0])
                    else:
                        instructorFullString = ""

                    if instructorFullString != "":
                        instructorFull = re.findall(r'\w{2,}\s\w+', instructorFullString)[0]
                    else:
                        instructorFull = "staff"

                    print(instructorFull)                   #For debugging purpose, can be ignored.

                    ASU = RateMyProfAPI(teacher=instructorFull)
                    ASU.retrieveRMPInfo()
                    rating = ASU.getRMPInfo()
                    firstTag = ASU.getFirstTag()

                    response += "Class Code：%s\tSeats Left：%s\tInstructor：%s\tHottest Tag：%s\tRMP Rating：%s\n" % \
                                (classNumber, seatsOpen, inst, firstTag, str(rating))
                else:
                    classNumberString = str(available.xpath('//*[@id="Any_13_%s"]/text()' % (str(count - 1))))
                    classNumber = re.findall(r'\d+', classNumberString)[0]
                    seatsOpenString = str(
                        available.xpath('//*[@id="informal_%s"]/td[11]/div/div[1]/text()' % (str(count - 1))))
                    seatsOpen = re.findall(r'\d+', seatsOpenString)[0]
                    instructor = str(available.xpath('//*[@id="DirectLink_%s"]/span/text()' % (str(count - 1))))
                    instructorFullString = re.findall(
                        r'<a id="DirectLink_%s" title="Instructor\|.*?"' % (str(count - 1)),
                        self.Page.text)

                    if instructor == "[]":
                        inst = "staff"

                    else:
                        inst = re.findall(r'[^\\t]\w+', instructor)[0]

                    if len(instructorFullString) > 0:
                        instructorFullString = str(instructorFullString[0])
                    else:
                        instructorFullString = ""

                    if instructorFullString != "":
                        instructorFull = re.findall(r'\w{2,}\s\w+', instructorFullString)[0]
                    else:
                        instructorFull = "staff"

                    print(instructorFull)

                    ASU = RateMyProfAPI(teacher=instructorFull)
                    ASU.retrieveRMPInfo()
                    rating = ASU.getRMPInfo()
                    firstTag = ASU.getFirstTag()

                    response += "Class Code：%s\tSeats Left：%s\tInstructor：%s\tHottest Tag：%s\tRMP Rating：%s\n" % \
                                (classNumber, seatsOpen, inst, firstTag, str(rating))

        else:
            response = "Oops, no result was found."

        return response
