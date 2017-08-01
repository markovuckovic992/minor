#!/usr/bin/env python

import sys
import json
import optparse
import os
import Queue
import random
import re
import string
import subprocess
import threading
import time
import urllib2

VERSION = "2.64"
BANNER = """
+-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-+
|f||e||t||c||h||-||s||o||m||e||-||p||r||o||x||i||e||s| <- v%s
+-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-++-+""".strip("\r\n") % VERSION

ANONIMITY_LEVELS = {"elite": "high", "anonymous": "medium", "transparent": "low"}
FALLBACK_METHOD = False
IFCONFIG_CANDIDATES = ("https://ifconfig.co/ip", "https://api.ipify.org/?format=text", "https://ifconfig.io/ip", "https://ifconfig.minidump.info/ip", "https://myexternalip.com/raw", "https://wtfismyip.com/text")
IFCONFIG_URL = None
MAX_HELP_OPTION_LENGTH = 18
PROXY_LIST_URL = "https://hidester.com/proxydata/php/data.php?mykey=csv&gproxy=2"
ROTATION_CHARS = ('/', '-', '\\', '|')
TIMEOUT = 10
THREADS = 10
USER_AGENT = "curl/7.{curl_minor}.{curl_revision} (x86_64-pc-linux-gnu) libcurl/7.{curl_minor}.{curl_revision} OpenSSL/0.9.8{openssl_revision} zlib/1.2.{zlib_revision}".format(curl_minor=random.randint(8, 22), curl_revision=random.randint(1, 9), openssl_revision=random.choice(string.lowercase), zlib_revision=random.randint(2, 6))

if not subprocess.mswindows:
    BANNER = re.sub(r"\|(\w)\|", lambda _: "|\033[01;41m%s\033[00;49m|" % _.group(1), BANNER)

options = None
counter = [0]
threads = []

def retrieve(url, data=None, headers={"User-agent": USER_AGENT}, timeout=TIMEOUT, opener=None):
    try:
        req = urllib2.Request("".join(url[i].replace(' ', "%20") if i > url.find('?') else url[i] for i in xrange(len(url))), data, headers)
        retval = (urllib2.urlopen if not opener else opener.open)(req, timeout=timeout).read()
    except Exception as ex:
        try:
            retval = ex.read() if hasattr(ex, "read") else getattr(ex, "msg", str())
        except:
            retval = None

    return retval or ""

def worker(queue, handle=None):
    try:
        while True:
            proxy = queue.get_nowait()
            result = ""
            counter[0] += 1
            sys.stdout.write("\r%s\r" % ROTATION_CHARS[counter[0] % len(ROTATION_CHARS)])
            sys.stdout.flush()
            start = time.time()
            candidate = "%s://%s:%s" % (proxy["type"], proxy["IP"], proxy["PORT"])
            if not all((proxy["IP"], proxy["PORT"])) or re.search(r"[^:/\w.]", candidate):
                continue
            if not FALLBACK_METHOD:
                process = subprocess.Popen("curl -m %d -A \"%s\" --proxy %s %s" % (TIMEOUT, USER_AGENT, candidate, IFCONFIG_URL), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result, _ = process.communicate()
            elif proxy["type"] in ("http", "https"):
                opener = urllib2.build_opener(urllib2.ProxyHandler({"http": candidate, "https": candidate}))
                result = retrieve(IFCONFIG_URL, timeout=options.maxLatency or TIMEOUT, opener=opener)
            if (result or "").strip() == proxy["IP"].encode("utf8"):
                latency = time.time() - start
                if latency < (options.maxLatency or TIMEOUT):
                    sys.stdout.write("\r%s%s # latency: %.2f sec; country: %s; anonymity: %s (%s)\n" % (candidate, " " * (32 - len(candidate)), latency, ' '.join(_.capitalize() for _ in (proxy["country"].lower() or '-').split(' ')), proxy["anonymity"].lower() or '-', ANONIMITY_LEVELS.get(proxy["anonymity"].lower(), '-')))
                    sys.stdout.flush()
                    if handle:
                        os.write(handle, "%s%s" % (candidate, os.linesep))
    except Queue.Empty:
        pass

def run():
    global FALLBACK_METHOD
    global IFCONFIG_URL


    for candidate in IFCONFIG_CANDIDATES:
        result = retrieve(candidate)
        if re.search(r"\A\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\Z", (result or "").strip()):
            IFCONFIG_URL = candidate
            break

    process = subprocess.Popen("curl -m %d -A \"%s\" %s" % (TIMEOUT, USER_AGENT, IFCONFIG_URL), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()
    FALLBACK_METHOD = re.search(r"\d+\.\d+\.\d+\.\d+", stdout or "") is None

    try:
        proxies = json.loads(retrieve(PROXY_LIST_URL, headers={"User-agent": USER_AGENT, "Referer": "https://hidester.com/proxylist/"}))
    except:
        pass

    response_data = []
    for proxy in proxies:
        if 'socks5' == proxy['type']:
            response_data.append(proxy['type'] + '://' + proxy['IP'] + ':' + unicode(proxy['PORT']))
    
    # rnd = random.randint(0, len(response_data))

    return response_data
    # queue = Queue.Queue()
    # for proxy in proxies:
    #     queue.put(proxy)

    # sys.stdout.write("[i] testing %d proxies (%d threads)...\n\n" % (len(proxies), options.threads or THREADS))
    # for _ in xrange(options.threads or THREADS):
    #     thread = threading.Thread(target=worker, args=[queue, handle])
    #     thread.daemon = True

    #     try:
    #         thread.start()
    #     except ThreadError as ex:
    #         sys.stderr.write("[x] error occurred while starting new thread ('%s')" % ex.message)
    #         break

    #     threads.append(thread)

    # try:
    #     alive = True
    #     while alive:
    #         alive = False
    #         for thread in threads:
    #             if thread.isAlive():
    #                 alive = True
    #                 time.sleep(0.1)
    # except KeyboardInterrupt:
    #     sys.stderr.write("\r   \n[!] Ctrl-C pressed\n")
    # else:
    #     sys.stdout.write("\n[i] done\n")
    # finally:
    #     sys.stdout.flush()
    #     sys.stderr.flush()
    #     if handle:
    #         os.close(handle)
    #     os._exit(0)

def main():
    IP = run()
    return IP
