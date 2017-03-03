#  -*- coding: gbk -*-
import os
import urllib2

def downloadC() :
    for lecture in range(1,11) :
        path = "D:\\edenPPT\\C\\%d" % lecture
        os.mkdir(path)
        if lecture == 10 :
            urlLecture = "%s%d" % ("http://eden.sysu.edu.cn:8080/media/%5B2014%5D%20SE-122%20by%20Dr.%20Wang/img/Lecture%20", lecture)
        else :
            urlLecture = "%s%d" % ("http://eden.sysu.edu.cn:8080/media/%5B2014%5D%20SE-122%20by%20Dr.%20Wang/img/Lecture%200", lecture)
        page = 1
        while True :
            imgurl = urlLecture + "/page-%d.jpg" % page
            req = urllib2.Request(imgurl)
            try:
                img = urllib2.urlopen(req)
                Imgname = "%s\\%d.jpg" % (path, page)
                f = open(Imgname, "wb")
                f.write(img.read())
                f.close()
                print('C Lecture %d - %d.jpg Saved!') % (lecture, page)
                page = page + 1
            except urllib2.URLError, e:
                break

def downloadCpp() :
    Namelist = {}
    Namelist[1] = "From%20C%20to%20C++"
    Namelist[2] = "Classes%20and%20Objects"
    Namelist[3] = "Operator%20Overloading"
    Namelist[4] = "Inheritance"
    Namelist[5] = "Polymorphism"
    Namelist[6] = "Templates%20"
    Namelist[7] = "STL"
    Namelist[8] = "STL%20-%20Sources"
    Namelist[9] = "Exceptiong%20Handling%20"
    Namelist[10] = "IO%20and%20File%20"
    Namelist[11] = "Effective%20C++"
    Namelist[12] = "Windows%20and%20MFC"

    s = "http://eden.sysu.edu.cn:8080/media/%5B2014%5D%20SE-123%20by%20Dr.%20Wan/img/2014%20Lecture%20Notes%20on%20C++%20-%20"
    for lecture in range(1,13) :
        path = "D:\\edenPPT\\Cpp\\%d" % lecture
        os.mkdir(path)

        urlLecture = "%s%d%s%s" % (s, lecture, "%20-%20", Namelist[lecture])
        page = 1
        while True :
            imgurl = urlLecture + "/page-%d.jpg" % page
            req = urllib2.Request(imgurl)
            try:
                img = urllib2.urlopen(req)
                Imgname = "%s\\%d.jpg" % (path, page)
                f = open(Imgname, "wb")
                f.write(img.read())
                f.close()
                print('Cpp Lecture %d - %d.jpg Saved!') % (lecture, page)
                page = page + 1
            except urllib2.URLError, e:
                break

print "Please use SYSU network or VPN(easyconnect)"
flag = raw_input("All ppt will be in D:\\edenPPT, start download?(y or n)：")
if flag == 'y' :
    os.mkdir("D:\\edenPPT")
    os.mkdir("D:\\edenPPT\\C")
    os.mkdir("D:\\edenPPT\\Cpp")
    downloadC()
    downloadCpp()
