import re, requests
from lxml import etree
import logging

#Author Email: yiyangl6@asu.edu

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}

INFO_NOT_AVAILABLE = "Info currently not available"

teacherList = []
tagFeedBackList = []
ratingList = []
takeAgainList = []

class RateMyProfAPI:

    #school id 45 = Arizona State University, the ID is initialized to 45 if not set upon usage.
    def __init__(self, schoolId=45, teacher="staff"):
        global teacherList
        if teacher != "staff":
            teacher = str(teacher).replace(" ", "+")
        else:
            teacher = ""

        self.pageData = ""
        self.finalUrl = ""
        self.tagFeedBack = ""
        self.rating = ""
        self.takeAgain = ""
        self.teacherName = teacher
        self.index = -1

        self.schoolId = schoolId

        if self.teacherName in teacherList:
            self.index = teacherList.index(self.teacherName)
        else:
            teacherList.append(self.teacherName)

    def retrieveRMPInfo(self):
        """
        :function: initialize the RMP data
        """

        global tagFeedBackList, ratingList, takeAgainList
        #If professor showed as "staff"
        if self.teacherName == "":
            self.rating = INFO_NOT_AVAILABLE
            self.takeAgain = INFO_NOT_AVAILABLE
            self.tagFeedBack = []

            ratingList.append(INFO_NOT_AVAILABLE)
            takeAgainList.append(INFO_NOT_AVAILABLE)
            tagFeedBackList.append(INFO_NOT_AVAILABLE)

            return

        if self.index == -1:
            #making request to the RMP page
            url = "https://www.ratemyprofessors.com/search.jsp?queryoption=HEADER&" \
                  "queryBy=teacherName&schoolName=Arizona+State+University&schoolID=%s&query=" % self.schoolId + self.teacherName

            page = requests.get(url=url, headers=headers)
            self.pageData = page.text
            pageDataTemp = re.findall(r'ShowRatings\.jsp\?tid=\d+', self.pageData)
            if pageDataTemp:
                pageDataTemp = re.findall(r'ShowRatings\.jsp\?tid=\d+', self.pageData)[0]
                self.finalUrl = "https://www.ratemyprofessors.com/" + pageDataTemp
                self.tagFeedBack = []

                page = requests.get(self.finalUrl)
                t = etree.HTML(page.text)

                # Get tags
                tags = t.xpath('//*[@id="root"]/div/div/div[2]/div[1]/div[1]/div[5]/div[2]/span/text()')
                if not tags:
                    self.tagFeedBack = []
                else:
                    self.tagFeedBack = tags

                # Get rating
                self.rating = t.xpath('//*[@id="root"]/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[1]/text()')[0]
                if re.match(r'.*?N/A', self.rating):
                    self.rating = INFO_NOT_AVAILABLE
                else:
                    try:
                        self.rating = re.findall(r'\d\.\d', self.rating)[0]
                    except IndexError:
                        self.rating = INFO_NOT_AVAILABLE

                # Get "Would Take Again" Percentage
                takeAgain = t.xpath('//*[@id="root"]/div/div/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/text()')
                if not takeAgain:
                    self.takeAgain = INFO_NOT_AVAILABLE
                else:
                    takeAgain = re.findall(r'\d+%', takeAgain[0])
                    if not takeAgain:
                        self.takeAgain = INFO_NOT_AVAILABLE
                    else:
                        self.takeAgain = takeAgain[0]

            else:
                self.rating = INFO_NOT_AVAILABLE
                self.takeAgain = INFO_NOT_AVAILABLE
                self.tagFeedBack = []

            ratingList.append(self.rating)
            takeAgainList.append(self.takeAgain)
            tagFeedBackList.append(self.tagFeedBack)

        else:
            self.rating = ratingList[self.index]
            self.takeAgain = takeAgainList[self.index]
            self.tagFeedBack = tagFeedBackList[self.index]

    def getRMPInfo(self):
        """
        :return: RMP rating.
        """
        return INFO_NOT_AVAILABLE if self.rating == INFO_NOT_AVAILABLE else self.rating + "/5.0"

    def getTags(self):
        """

        :return: teacher's tag in [list]
        """
        return self.tagFeedBack

    def getFirstTag(self):
        """

        :return: teacher's most popular tag [string]
        """
        return self.tagFeedBack[0] if self.tagFeedBack else INFO_NOT_AVAILABLE

    def getWouldTakeAgain(self):
        """

        :return: teacher's percentage of would take again.
        """
        return self.takeAgain
