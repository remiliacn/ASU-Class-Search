import RMPClass, requests, re
from lxml import etree


def generateResponse(instructorFullNode: list, classNumber: str, seatsOpen: str):
    response = ''
    if instructorFullNode:
        instructorFull = instructorFullNode[0]
    else:
        instructorFull = "staff"

    print(instructorFull)       # debug.

    ASU = RMPClass.RateMyProfAPI(teacher=instructorFull)
    ASU.retrieveRMPInfo()
    rating = ASU.getRMPInfo()
    firstTag = ASU.getFirstTag()

    response += "Class Code：%s\tSeats Left：%s\tInstructor：%s\tHottest Tag：%s\tRMP Rating：%s\n" % \
                (classNumber, seatsOpen, instructorFull, firstTag, rating)

    return response

class ASUClassFinder:
    def __init__(self, major, code):
        self.major = major
        self.code = code
        #updated to Fall 2020's schedule.
        self.baseUrl = f"https://webapp4.asu.edu/catalog/myclasslistresults?t=2207&s={major}&n={code}&hon=F&promod=F&e=open&page=1"
        self.Page = self._getPage()
        self.totalResult = self.getPageCount()

    def _getPage(self):
        res = requests.get(self.baseUrl, headers=RMPClass.headers)
        return res

    def getPageCount(self):
        document = etree.HTML(self.Page.text)
        fullName = document.xpath('//*[@id="classResults"]/div[3]/div/text()')
        resultNode = re.findall(r'.*?of (\d+)', fullName[0])
        if resultNode:
            totalResult = int(resultNode[0])
        else:
            totalResult = 0

        return totalResult

    def __str__(self):
        response = ""
        document = etree.HTML(self.Page.text)
        if self.totalResult > 0:
            for count in range(0, self.totalResult):
                response += self.analyzeURL(count, document)

        else:
            response = "Oops, no information document."

        return response

    def analyzeURL(self, count: int, available):
        response = ''
        if count == 0:
            classNumberString = available.xpath('//*[@id="Any_13"]/text()')
            classNumber = re.findall(r'\d+', classNumberString[0])[0]

            seatsOpenString = available.xpath('//*[@id="informal"]/td[11]/div/div[1]/text()')
            seatsOpen = re.findall(r'\d+', seatsOpenString[0])[0]

            instructorFullString = re.findall(
                r'<a id="DirectLink" title="Instructor\|(.*?)"',
                self.Page.text
            )

            response += generateResponse(instructorFullString, classNumber, seatsOpen)

        else:
            classNumberString = available.xpath(f'//*[@id="Any_13_{str(count - 1)}"]/text()')
            classNumber = re.findall(r'\d+', classNumberString[0])[0]

            seatsOpenString = available.xpath(f'//*[@id="informal_{str(count - 1)}"]/td[11]/div/div[1]/text()')
            seatsOpen = re.findall(r'\d+', seatsOpenString[0])[0]

            instructorFullString = re.findall(
                f'<a id="DirectLink_{str(count - 1)}" title="Instructor\|(.*?)"',
                self.Page.text
            )

            response += generateResponse(instructorFullString, classNumber, seatsOpen)

        return response


if __name__ == '__main__':
    classFinder = ASUClassFinder(major='CSE', code='110')
    print(classFinder.__str__())