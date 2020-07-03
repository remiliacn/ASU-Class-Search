"""
ASU class search with python3 support.
"""
import re
import requests
from lxml import etree
import rmp_class


def generate_response(instructor_full_node: list, class_number: str, seats_open: str):
    """
    Generate response string from input.
    :param instructor_full_node: list, the full node is generated from etree.HTML() function.
    :param class_number: str, user stored class number.
    :param seats_open: str, how many seats are left.

    :return str, string response of current professor name.
    """
    response = ''
    if instructor_full_node:
        instructor_full = instructor_full_node[0]
    else:
        instructor_full = "staff"

    print(instructor_full)  # debug.

    asu = rmp_class.RateMyProfAPI(teacher=instructor_full)
    asu.retrieve_rmp_info()
    rating = asu.get_rmp_info()
    first_tag = asu.get_first_tag()

    response += "Class Code：%s\tSeats Left：%s\tInstructor：%s\tHottest Tag：%s\tRMP Rating：%s\n" % \
                (class_number, seats_open, instructor_full, first_tag, rating)

    return response


class ASUClassFinder:
    """
    ASU class finder class for searching in ASU website for courses.
    """

    def __init__(self, major, code):
        """

        :param major: str, user input for major code. Such as "CSE"
        :param code: str, user input for class code. Such as "110"
        """
        self.major = major
        self.code = code
        # updated to Fall 2020's schedule.
        self.base_url = f"https://webapp4.asu.edu/catalog/myclasslistresults?t=2207" \
                        f"&s={major}&n={code}&hon=F&promod=F&e=open&page=1"

        self.page = self._get_page()
        self.total_result = self.get_page_count()

    def _get_page(self):
        """
        Helper method to get response text.
        :return: HTTPRequest.
        """
        res = requests.get(self.base_url, headers=rmp_class.headers)
        return res

    def get_page_count(self):
        """
        Get page count total
        :return: int, page count total.
        """
        document = etree.HTML(self.page.text)
        full_name = document.xpath('//*[@id="classResults"]/div[3]/div/text()')
        result_node = re.findall(r'.*?of (\d+)', full_name[0])
        if result_node:
            total_result = int(result_node[0])
        else:
            total_result = 0

        return total_result

    def __str__(self):
        """
        Generate response string by page.
        :return: str, full response of the search result.
        """
        response = ""
        document = etree.HTML(self.page.text)
        if self.total_result > 0:
            for count in range(0, self.total_result):
                response += self.analyze_url(count, document)

        else:
            response = "Oops, no information document."

        return response

    def analyze_url(self, count: int, available):
        """
        Analyze the document node.
        :param count: int, the current page count.
        :param available: documentNode, a document node to parse into etree.
        :return: str, response for one page that depends on the page number.
        """
        response = ''
        if count == 0:
            class_number_string = available.xpath('//*[@id="Any_13"]/text()')
            class_number = re.findall(r'\d+', class_number_string[0])[0]

            seats_open_string = available.xpath('//*[@id="informal"]/td[11]/div/div[1]/text()')
            seats_open = re.findall(r'\d+', seats_open_string[0])[0]

            instructor_full_string = re.findall(
                r'<a id="DirectLink" title="Instructor\|(.*?)"',
                self.page.text
            )

            response += generate_response(instructor_full_string, class_number, seats_open)

        else:
            class_number_string = available.xpath(f'//*[@id="Any_13_{str(count - 1)}"]/text()')
            class_number = re.findall(r'\d+', class_number_string[0])[0]

            seats_open_string = available.xpath(f'//*[@id="informal_{str(count - 1)}"]'
                                                f'/td[11]/div/div[1]/text()')

            seats_open = re.findall(r'\d+', seats_open_string[0])[0]

            instructor_full_string = re.findall(
                fr'<a id="DirectLink_{str(count - 1)}" title="Instructor\|(.*?)"',
                self.page.text
            )

            response += generate_response(instructor_full_string, class_number, seats_open)

        return response
