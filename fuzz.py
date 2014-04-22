import requests
import random
import string
import logHandler


class Fuzzer:
    def __init__(self, url, log_handler=None, cookies=None):
        """ Save entrypoints informations

        """

        # Clean string
        if url[-1:] != "/":
            url = url + "/"
        self.url = url

        if log_handler is not None:
            self.log_handler = logHandler.LogHandler(log_handler)
        else:
            self.log_handler = None

        if cookies is not None:
            self.cookies = {}
            for cookie in cookies.split('&'):
                param, value = cookie.split('=')
                self.cookies[param] = value
        else:
            self.cookies = {}

    def getData(self, length):
        """ Generate random printable string for given length

        """
        return ''.join(random.choice(string.printable) for _ in range(length))

    def sendData(self, url, vars):
        """ Send random string on given entrypoint

        """
        r = None
        data = {}
        results = {}
        value = self.getData(10)
        for req in vars:
            if req['method'] not in data.key:
                data[req['method'].lower()] = {}
            data[req['method'].lower()][req['var']] = value
        for method, var in data.items():
            if method == "get":
                r = requests.get(url,
                                 params=data[method],
                                 cookies=self.cookies,
                                 verify=False)
            elif method == "post":
                r = requests.post(url,
                                  data=data[method],
                                  cookies=self.cookies,
                                  verify=False)
            elif method == "cookie":
                cookies = dict(data[method].items() + self.cookies.items())
                r = requests.get(url,
                                 cookies=cookies,
                                 verify=False)
            elif method == "server":
                r = requests.get(url,
                                 headers=data[method],
                                 cookies=self.cookies,
                                 verify=False)
            else:
                pass

            if r.status_code == 404:
                return None

            # Get errors triggered by last request
            logs = []
            if self.log_handler is not None:
                logs = self.log_handler.get_lines_until_last_check()

            if url not in results.keys:
                results[url] = []

            results[url].append({'method': method,
                                 'data': var,
                                 'response': r.status_code,
                                 'informations': logs})
        return results

    def fuzz(self, base_path, entry_points, nb_tests, output):
        """Perform fuzzing using known entry_points

        """
        results = []
        current_test = 1
        for page, vars in entry_points.items():
            if output == "pretty":
                print "%d%%" % int((current_test*100) / len(entry_points))

            # Clean strings
            if page[:2] == "./":
                page = page[2:]
            if page.startswith(base_path):
                page = page[len(base_path):]

            url = "%s%s" % (self.url, page)

            # perform n tests by sending random strings
            for test in range(0, int(nb_tests)):
                result = self.sendData(url, vars)
                if result is not None:
                    results.append(result)
            current_test = current_test + 1

        return results
