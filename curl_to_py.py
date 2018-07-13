class curl_to_py(object):
    p = 0
    result = {'temp': []}
    boolOptions = ['#', 'progress-bar', '-', 'next', '0', 'http1.0', 'http1.1', 'http2',
        'no-npn', 'no-alpn', '1', 'tlsv1', '2', 'sslv2', '3', 'sslv3', '4', 'ipv4', '6', 'ipv6',
        'a', 'append', 'anyauth', 'B', 'use-ascii', 'basic', 'compressed', 'create-dirs',
        'crlf', 'digest', 'disable-eprt', 'disable-epsv', 'environment', 'cert-status',
        'false-start', 'f', 'fail', 'ftp-create-dirs', 'ftp-pasv', 'ftp-skip-pasv-ip',
        'ftp-pret', 'ftp-ssl-ccc', 'ftp-ssl-control', 'g', 'globoff', 'G', 'get',
        'ignore-content-length', 'i', 'include', 'I', 'head', 'j', 'junk-session-cookies',
        'J', 'remote-header-name', 'k', 'insecure', 'l', 'list-only', 'L', 'location',
        'location-trusted', 'metalink', 'n', 'netrc', 'N', 'no-buffer', 'netrc-file',
        'netrc-optional', 'negotiate', 'no-keepalive', 'no-sessionid', 'ntlm', 'O',
        'remote-name', 'oauth2-bearer', 'p', 'proxy-tunnel', 'path-as-is', 'post301', 'post302',
        'post303', 'proxy-anyauth', 'proxy-basic', 'proxy-digest', 'proxy-negotiate',
        'proxy-ntlm', 'q', 'raw', 'remote-name-all', 's', 'silent', 'sasl-ir', 'S', 'show-error',
        'ssl', 'ssl-reqd', 'ssl-allow-beast', 'ssl-no-revoke', 'socks5-gssapi-nec', 'tcp-nodelay',
        'tlsv1.0', 'tlsv1.1', 'tlsv1.2', 'tr-encoding', 'trace-time', 'v', 'verbose', 'xattr',
        'h', 'help', 'M', 'manual', 'V', 'version'
    ]

    def parseCommand(self):
        if (len(self.curl) > 2 and (self.curl[0] == '$' or self.curl[0] == '#') and self.whitespace(self.curl[1])):
            self.curl = self.curl[1:].lstrip()
        while self.p < len(self.curl):
            self.skipWhiteSpace()
            if self.curl[self.p] == '-':
                self.flagSet()
            else:
                self.unflagged()
            self.p+= 1
        return self.result

    def unflagged(self):
        self.result['temp'].append(self.nextString())

    def skipWhiteSpace(self):
        while self.whitespace(self.curl[self.p]) and self.p < len(self.curl):
           self.p+= 1

    def flagSet(self):
        if self.isLongFlag():
            return self.longFlag()
        return self.shortFlag()

    def isLongFlag(self):
        return self.p + 1 < len(self.curl) and self.curl[self.p + 1] == '-'

    def longFlag(self):
        self.p+= 2
        flagName = self.nextString("=")
        if self.boolFlag(flagName):
            self.result[flagName] = True
        else:
            if flagName not in self.result:
                self.result[flagName] = []
            if type(self.result[flagName]) == list:
                self.p += 1
                self.result[flagName].append(self.nextString())

    def shortFlag(self):
        self.p += 1
        while self.p< len(self.curl) and not self.whitespace(self.curl[self.p]):
            flagName = self.curl[self.p]
            if flagName not in self.result:
                self.result[flagName] = []
                self.p+= 1
            if self.boolFlag(flagName):
                self.result[flagName] = True
            elif type(self.result[flagName] == list):
                self.p += 1
                self.result[flagName].append(self.nextString())

    def boolFlag(self, flag):
        return flag in self.boolOptions

    def whitespace(self, ch):
        return ch == " " or ch == "\t" or ch == "\n" or ch == "\r"

    def nextString(self, endChar=None):
        self.skipWhiteSpace()
        s = ""
        quoted = False
        quoteCh = ""
        escaped = False
        while self.p < len(self.curl):
            if quoted:
                if self.curl[self.p] == quoteCh and not escaped:
                    quoted = False
                    self.p+= 1
                    continue
            else:
                if not escaped:
                    if self.whitespace(self.curl[self.p]):
                        return s
                    if self.curl[self.p] == '"' or self.curl[self.p] == "'":
                        quoted = True
                        quoteCh = self.curl[self.p]
                        self.p+= 1
                    if endChar and self.curl[self.p] == endChar:
                        self.p+= 1
                        return s
            if not escaped and self.curl[self.p] == "\\":
                escaped = True
                if not (self.p < len(self.curl) - 1 and self.curl[self.p + 1] == '$'):
                    self.p+= 1
                    continue
            s += self.curl[self.p]
            escaped = False
            self.p += 1
        return s

    def extractRelevantPieces(self, cmd):
        relevant = {
            'url': "",
            'method': "",
            'headers': {},
            'data': {}
        }
        if 'url' in cmd and len(cmd['url']) > 0:
            relevant['url'] = cmd['url'][0]
        elif len(cmd['temp']) > 1:
            relevant['url'] = cmd['temp'][1]
        relevant['headers'] = self.getHeadersDict(cmd)
        if 'I' in cmd or 'head' in cmd:
            relevant['method'] = 'HEAD'

        if 'request' in cmd and len(cmd['request']) > 0:
            relevant['method'] = cmd['request'][len(cmd['request']) - 1].upper()
        elif 'X' in cmd and len(cmd['X']) > 0:
            relevant['method'] = cmd['X'][len(cmd['X']) - 1].upper()
        elif 'H' in cmd:
            if 'method' in cmd['H']:
                relevant['method'] = cmd['H']['method'].upper()
            elif ':method' in cmd['H']:
                relevant['method'] = cmd['H'][':method'].upper()

        relevant['data'] = self.getDataDict(cmd, relevant)
        relevant['basicAuth'] = self.getBasicAuth(cmd)
        if not relevant['method']:
            relevant['method'] = "GET"
        return relevant

    def getBasicAuth(self, cmd):
        basicAuthString = ""
        if 'user' in cmd and len(cmd['user']) > 0:
            basicAuthString = cmd['user'][len(cmd['user']) - 1]
        elif 'u' in cmd and len(cmd['u']) > 0:
            basicAuthString = cmd['u'][len(cmd['u']) - 1]
        basicAuthSplit = basicAuthString.find(':')
        if basicAuthSplit > -1:
            return {
                'user' : basicAuthString[0 : basicAuthSplit],
                'pass' : basicAuthString[basicAuthSplit + 1:]
            }
        elif not basicAuthString == "":
            return {
                'user' : basicAuthString,
                'pass' : "<PASSWORD>",
            }
        else:
            return None

    def getDataDict(self, cmd, relevant):
        data = {}
        dataAscii = []
        dataFiles = []
        data['ascii'] = ""
        data['files'] = ""
        if 'd' in cmd:
            self.loadData(relevant, cmd['d'], dataAscii, dataFiles)
        if 'data' in cmd:
            self.loadData(relevant, cmd['data'], dataAscii, dataFiles)
        if len(dataAscii) > 0:
            data['ascii'] = '&'.join(dataAscii)
        if len(dataFiles) > 0:
            data['files'] = '&'.join(dataFiles)
        return data

    def loadData(self, relevant, d, dataAscii, dataFiles):
        if not 'method' in relevant:
            relevant['method'] = "POST"
        if 'Content-Type' in relevant['headers']:
            hasContentType = True
        else:
            relevant['headers']['Content-Type'] = 'application/x-www-form-urlencoded'
        for data in d:
            if len(data) > 0 and data[0] == "@":
                dataFiles.append(data[1:])
            else:
                dataAscii.append(data)


    def getHeadersDict(self, cmd):
        result = {}
        if 'H' in cmd:
            for header in cmd['H']:
                colonIndex = header.find(':')
                if colonIndex == 0:
                    colonIndex = header[1:].find(':') + 1
                headerName = header[0: colonIndex]
                headerValue = header[colonIndex + 1:].lstrip()
                result[headerName] = headerValue

        if 'headers' in cmd:
            for key, value in cmd['headers'].items():
                # colonIndex = header.find(':')
                # if colonIndex == 0:
                #     colonIndex = header[1:].find(':')

                headerName = key
                headerValue = value
                result[headerName] = headerValue

        return result


    def renderSimple(self, method, url):
        if method == "GET":
            return "requests.get('%s')\n" % url
        elif method == "POST":
            return "requests.post('%s', data=None)\n"% url
        elif method == "HEAD":
            return "requests.head('%s')\n" % url
        else:
            return 'not support yet'
    def renderComplex(self ,req):
        py = "import requests\n"
        headers = self.getHeadersDict(req)
        data = self.getDataStr(req['data'])
        headStr = "{\n"
        for key,values in headers.items():
            headStr += "\t'%s' : '%s',\n" % (key, values)
        py += "\nheaders = " + headStr + "}\n"
        req['fullurl'] = req['url']
        py += "\nfullurl = '%s'\n"%req['fullurl']
        par = self.getParmDict(req)
        if par is not None:
            ParmStr = "{\n"
            for key, values in par.items():
                ParmStr += "\t'%s' : '%s',\n" % (key, values)
            py += "\npayload = " + ParmStr + "}\n"
        if not data ==  "data=''":
            py += data + '\n'
        py += "url = '%s'\n"%req['url']
        py += "requests." + req['method'].lower() + "(url = url"
        if headers is not "":
            py += ', headers = headers'
        if par is not None:
            py += ', params = payload'
        if not data == "data=''":
            py += ', data = data'
        if req['basicAuth'] is not None:
            py += ", auth = {'%s':'%s'}" % (req['basicAuth']['user'], req['basicAuth']['pass'])
        py += ")"
        return py

    def getParmDict(self, req):
        parms = req['url'].split('&')
        ans = {}
        if len(parms) > 1:
            for item in parms:
                key, value = item.split('=')
                ans[key] = value
            req['params'] = ans
            req['url'] = parms[0]
            return ans
        return None
    def run(self):
        self.curl = raw_input('Enter your curl:')
        # self.curl = open('curl.txt', 'r').read()
        if not self.curl.lstrip():
            print('empty input')
            return
        cmd = self.parseCommand()
        if not cmd['temp'][0] == 'curl':
            print('not a curl command')
        req = self.extractRelevantPieces(cmd)

        if len(req['headers']) == 0 and not req['data']['ascii'] and not req['data']['files'] and not 'basicauth' not in req:
            return self.renderSimple(req['method'], req['url'])
        return self.renderComplex(req)

    def getDataStr(self, data):
        dataStr = ""
        dataFiles = data['files']
        if not dataFiles == "":
            return dataStr + "data = open('%s')\n" % dataFiles
        dataStr += 'data = {\n'
        dataAsciis = data['ascii'].split("&")
        if len(dataAsciis) == 1:
            return "data='%s'" % dataAsciis[0]
        for dd in dataAsciis:
            equalSignIdx = dd.find("=")
            if equalSignIdx == -1:
                dataStr += dd
                continue
            key = dd[0: equalSignIdx]
            value = dd[equalSignIdx + 1: ].lstrip()
            dataStr += "'%s' : '%s'\n" % (key, value)
        dataStr += "}\n"
        return dataStr


if __name__ == '__main__':
    cp = curl_to_py()
    print(cp.run())
