# This is for accepting input from command line
import argparse

parser = argparse.ArgumentParser(description='Check kubernetes cluster status.')
parser.add_argument('--insecure', help='Ignore SSL Certificate Errors', action="store_const", const=True, default=False) 
args = parser.parse_args()
insecure=args.insecure

# Supress unverified HTTPS request messages...
# Need to remove this for production
import urllib3
if insecure:
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# This is for making CURL requests to HTTP
import pycurl
import certifi
from StringIO import StringIO


from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from kubernetes import client, config
# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()

from openshift.dynamic import DynamicClient
k8s_client = config.new_client_from_config()
dyn_client = DynamicClient(k8s_client)


class MetricCollector:
  _insecure=False
  output=""

  def __init__(self, inscure):
    self._insecure = insecure
    output=""

    # not working yet
    # if self.insecure == True:
    #   urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  
  def text2yaml(self, text):
    return load(text)
  
  def yaml2text(self, yaml):
    return dump(yaml)
  
  # the CRD for hubs in python has not been implemented yet
  # so we will determine what is a "hub" by looking at what
  # pods are running in each namespace.
  def get_hubs(self):
    hubs = []
    namespaces = v1.list_namespace()
    for i in namespaces.items:
      namespace = i.metadata.name
      pods = v1.list_namespaced_pod(namespace)
      v1.list_namespaced_pod
      for j in pods.items:
        pod_name = j.metadata.name
        if "jobrunner" in pod_name:
          hubs.append(i)
    return hubs
  
  def get_pods(self, hub):
    return v1.list_namespaced_pod(hub).items
  
  def get_routes(self, hub):
      v1_routes = dyn_client.resources.get(api_version='route.openshift.io/v1', kind='Route')
      return v1_routes.get(namespace=hub).items
  
  def get_metrics_for_hub_url(self, url):
    #FNULL = open(os.devnull, 'w')
    #expected_status_code = "200"
    #return subprocess.call("curl 'https://" + url + "' -H 'Connection: keep-alive'
    #  -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1'
    #  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36' 
    # -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' 
    # -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9' 
    # --compressed --insecure -I -s | grep 'HTTP/1.1[ ]" + 
    # expected_status_code + "'", shell=True, stdout=FNULL, stderr=subprocess.STDOUT) == 0;

    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://' + url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())

    if self._insecure:
      c.setopt(pycurl.SSL_VERIFYPEER, 0)   
      c.setopt(pycurl.SSL_VERIFYHOST, 0)

    #if self.verbose:
    #  c.setopt(c.VERBOSE, True)
    
    c.setopt(pycurl.USERAGENT,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')
    c.setopt(pycurl.ENCODING, 'gzip, deflate, br')

    c.setopt(pycurl.HTTPHEADER, 
      ['Connection: keep-alive',
       'Pragma: no-cache',
       'Cache-Control: no-cache',
       'Upgrade-Insecure-Requests: 1',
       'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
       'Accept-Language: en-US,en;q=0.9' 
      ])
    
    c.perform()

    record = {}
    #record['ACTIVESOCKET'] = c.getinfo(pycurl.ACTIVESOCKET)
    #record['APPCONNECT_TIME_T'] = c.getinfo(pycurl.APPCONNECT_TIME_T)
    #record['CERTINFO'] = c.getinfo(pycurl.CERTINFO)
    #record['CONDITION_UNMET'] = c.getinfo(pycurl.CONDITION_UNMET)
    #record['CONNECT_TIME_T'] = c.getinfo(pycurl.CONNECT_TIME_T)
    #record['CONTENT_LENGTH_DOWNLOAD_T'] = c.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD_T)
    #record['CONTENT_LENGTH_UPLOAD_T'] = c.getinfo(pycurl.CONTENT_LENGTH_UPLOAD_T)
    #record['COOKIELIST'] = c.getinfo(pycurl.COOKIELIST)
    #record['FILETIME'] = c.getinfo(pycurl.FILETIME)
    #record['FILETIME_T'] = c.getinfo(pycurl.FILETIME_T)
    #record['HTTP_VERSION'] = c.getinfo(pycurl.HTTP_VERSION)
    #record['NAMELOOKUP_TIME_T'] = c.getinfo(pycurl.NAMELOOKUP_TIME_T)
    #record['PRETRANSFER_TIME_T'] = c.getinfo(pycurl.PRETRANSFER_TIME_T)
    #record['PRIVATE'] = c.getinfo(pycurl.PRIVATE)
    #record['PROTOCOL'] = c.getinfo(pycurl.PROTOCOL)
    #record['PROXY_SSL_VERIFYRESULT'] = c.getinfo(pycurl.PROXY_SSL_VERIFYRESULT)
    #record['REDIRECT_TIME_T'] = c.getinfo(pycurl.REDIRECT_TIME_T)
    #record['RTSP_CLIENT_CSEQ'] = c.getinfo(pycurl.RTSP_CLIENT_CSEQ)
    #record['RTSP_CSEQ_RECV'] = c.getinfo(pycurl.RTSP_CSEQ_RECV)
    #record['RTSP_SERVER_CSEQ'] = c.getinfo(pycurl.RTSP_SERVER_CSEQ)
    #record['RTSP_SESSION_ID'] = c.getinfo(pycurl.RTSP_SESSION_ID)
    #record['SCHEME'] = c.getinfo(pycurl.SCHEME)
    #record['SIZE_DOWNLOAD_T'] = c.getinfo(pycurl.SIZE_DOWNLOAD_T)
    #record['SIZE_UPLOAD_T'] = c.getinfo(pycurl.SIZE_UPLOAD_T)
    #record['SPEED_DOWNLOAD_T'] = c.getinfo(pycurl.SPEED_DOWNLOAD_T)
    #record['SPEED_UPLOAD_T'] = c.getinfo(pycurl.SPEED_UPLOAD_T)
    #record['STARTTRANSFER_TIME_T'] = c.getinfo(pycurl.STARTTRANSFER_TIME_T)
    #record['TLS_SESSION'] = c.getinfo(pycurl.TLS_SESSION)
    #record['TLS_SSL_PTR'] = c.getinfo(pycurl.TLS_SSL_PTR)
    #record['TOTAL_TIME_T'] = c.getinfo(pycurl.TOTAL_TIME_T)
    record['APPCONNECT_TIME'] = c.getinfo(pycurl.APPCONNECT_TIME)
    record['CONNECT_TIME'] = c.getinfo(pycurl.CONNECT_TIME)
    record['CONTENT_LENGTH_DOWNLOAD'] = c.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD)
    record['CONTENT_LENGTH_UPLOAD'] = c.getinfo(pycurl.CONTENT_LENGTH_UPLOAD)
    record['CONTENT_TYPE'] = c.getinfo(pycurl.CONTENT_TYPE)
    record['EFFECTIVE_URL'] = c.getinfo(pycurl.EFFECTIVE_URL)
    record['FTP_ENTRY_PATH'] = c.getinfo(pycurl.FTP_ENTRY_PATH)
    record['HEADER_SIZE'] = c.getinfo(pycurl.HEADER_SIZE)
    record['HTTPAUTH_AVAIL'] = c.getinfo(pycurl.HTTPAUTH_AVAIL)
    record['HTTP_CONNECTCODE'] = c.getinfo(pycurl.HTTP_CONNECTCODE)
    record['LASTSOCKET'] = c.getinfo(pycurl.LASTSOCKET)
    record['LOCAL_IP'] = c.getinfo(pycurl.LOCAL_IP)
    record['LOCAL_PORT'] = c.getinfo(pycurl.LOCAL_PORT)
    record['NAMELOOKUP_TIME'] = c.getinfo(pycurl.NAMELOOKUP_TIME)
    record['NUM_CONNECTS'] = c.getinfo(pycurl.NUM_CONNECTS)
    record['OS_ERRNO'] = c.getinfo(pycurl.OS_ERRNO)
    record['PRETRANSFER_TIME'] = c.getinfo(pycurl.PRETRANSFER_TIME)
    record['PRIMARY_IP'] = c.getinfo(pycurl.PRIMARY_IP)
    record['PRIMARY_PORT'] = c.getinfo(pycurl.PRIMARY_PORT)
    record['PROXYAUTH_AVAIL'] = c.getinfo(pycurl.PROXYAUTH_AVAIL)
    record['REDIRECT_COUNT'] = c.getinfo(pycurl.REDIRECT_COUNT)
    record['REDIRECT_TIME'] = c.getinfo(pycurl.REDIRECT_TIME)
    record['REDIRECT_URL'] = c.getinfo(pycurl.REDIRECT_URL)
    record['REQUEST_SIZE'] = c.getinfo(pycurl.REQUEST_SIZE)
    record['RESPONSE_CODE'] = c.getinfo(pycurl.RESPONSE_CODE)
    record['SIZE_DOWNLOAD'] = c.getinfo(pycurl.SIZE_DOWNLOAD)
    record['SIZE_UPLOAD'] = c.getinfo(pycurl.SIZE_UPLOAD)
    record['SPEED_DOWNLOAD'] = c.getinfo(pycurl.SPEED_DOWNLOAD)
    record['SPEED_UPLOAD'] = c.getinfo(pycurl.SPEED_UPLOAD)
    record['SSL_ENGINES'] = c.getinfo(pycurl.SSL_ENGINES)
    record['SSL_VERIFYRESULT'] = c.getinfo(pycurl.SSL_VERIFYRESULT)
    record['STARTTRANSFER_TIME'] = c.getinfo(pycurl.STARTTRANSFER_TIME)
    record['TOTAL_TIME'] = c.getinfo(pycurl.TOTAL_TIME)
    c.close()

    return record
    #body = buffer.getvalue()
    #print(body)

  def record_append(self, key, value):
      return key + " " + str(value) + "\n"
  
  def execute(self):

    hubs = self.get_hubs()
    hubs_count = len(hubs)
    hubs_online = 0
    for hub in hubs:
      hub_name = hub.metadata.name
    
      pods = self.get_pods(hub_name)
      for pod in pods:
        pod_name = pod.metadata.name
      
      routes = self.get_routes(hub_name)
      for route in routes:
        route_host = route.spec.host
        metrics = self.get_metrics_for_hub_url(route_host)
        is_online = metrics['RESPONSE_CODE'] == 200
        if is_online == False:
          self.output += self.record_append(hub_name + "_" + route_host + "_online", 0)
        else:
          self.output += self.record_append(hub_name + "_" + route_host + "_online", 1)
          hubs_online += 1
        for key in metrics:
          if metrics[key]:
            try:
              self.output += self.record_append(hub_name + "_" + route_host + "_" + key +"", metrics[key])
            except ValueError:
              self.output += self.record_append("#" + hub_name + "_" + route_host + "_" + key +"", metrics[key])
  
    # nodes = self.get_nodes()
    # print self.yaml2text(nodes)
    
    if hubs_count != 0:
      hubs_online_percentage = float(hubs_online) / float(hubs_count) * 100.0
    else:
      hubs_online_percentage = "NaN"

    self.output = self.record_append("hubs_online", hubs_online) + self.output
    self.output = self.record_append("hubs_total", hubs_count) + self.output
    self.output = self.record_append("hubs_online_percentage", hubs_online_percentage) + self.output

    if hubs_online == hubs_count:
      exitcode = 0
    else:
      exitcode = 1
    
    self.output = self.record_append("exit_code", exitcode) + self.output

    return exitcode
  
