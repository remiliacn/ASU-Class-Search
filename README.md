# ASU-Class-Search
ASU class search with Rate My Professor supports

How to use this package:
* Please make sure that you have ```lxml``` package installed
* Please make sure that you have ```requests``` package installed
* Use ```api = ASUClassSearch(major, majorCode)``` to initialize it. One example will be ```api = ASUClassSearch('CSE', '120')```
* Use ```api.__str__()``` to get the result. Please note that the result will be returned as a ``str``
