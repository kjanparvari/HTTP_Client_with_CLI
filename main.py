import argparse
import validators
import threading

parser = argparse.ArgumentParser(description="HTTP Client with CLI")
parser.add_argument("url", metavar="", type=str, help='URL')
parser.add_argument('-M', '--method', metavar="", type=str, required=False, help='HTTP Protocol Method')
parser.add_argument('-H', '--headers', action="append", metavar="", type=str, required=False,
                    help='HTTP Request Headers')
parser.add_argument('-Q', '--queries', action="append", metavar="", type=str, required=False,
                    help='HTTP Request Queries')
parser.add_argument('-D', '--data', metavar="", type=str, required=False, help='HTTP Request Body')
parser.add_argument('-J', '--json', metavar="", type=str, required=False, help='HTTP Request Body - JSON')
parser.add_argument('-F', '--file', metavar="", type=str, required=False, help='HTTP Request Body - File')
parser.add_argument('-T', '--timeout', metavar="", type=str, required=False, help='HTTP Request Wait Time [For '
                                                                                  'Response]')

args = (parser.parse_args())


class HTTPRequest:
    ALlOWED_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

    def __init__(self):
        import math
        self._url: str = ""
        self._method: str = 'GET'
        self._headers: dict = {}
        self._queries: dict = {}
        self._body: str = ""
        self._timeout = 99999.0
        self._timer_thread = threading.Thread(target=self._timer)

    def send(self):
        import requests
        try:
            response = requests.request(self.method, self.url, headers=self.headers, params=self.queries,
                                        data=self.body, timeout=self.timeout, stream=True)
            # self._timer_thread.start()

            import sys
            total_length = response.headers.get('content-length')
            final_data = bytearray()
            if total_length is None:  # no content length header
                final_data = response.content
            else:
                dl = 0
                total_length = int(total_length)
                print("Loading: ")
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    final_data.extend(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()

            print(f"\n\nStatus: {response.reason} {response.status_code}")
            for key, value in response.headers.items():
                print(f"{key}: {value}")

            import time
            if response.headers["Content-Type"] == "image/png":
                filename = "image_" + str(time.time()) + ".png"
                with open(f".\\{filename}", "wb") as f:
                    f.write(final_data)
            elif response.headers["Content-Type"] == "image/jpg" or response.headers["Content-Type"] == "image/jpeg":
                filename = "image_" + str(time.time()) + ".jpg"
                with open(f".\\{filename}", "wb") as f:
                    f.write(final_data)
            elif response.headers["Content-Type"] == "application/pdf":
                filename = "pdf_" + str(time.time()) + ".pdf"
                with open(f".\\{filename}", "wb") as f:
                    f.write(final_data)
            elif response.headers["Content-Type"] == "video/mp4":
                filename = "video_" + str(time.time()) + ".mp4"
                with open(f".\\{filename}", "wb") as f:
                    f.write(final_data)
            else:
                try:
                    print("\n\n", final_data.decode())
                except UnicodeDecodeError:
                    print("\n\n", final_data)
        except requests.exceptions.ConnectionError as e:
            self.error("connection failed")

    def _timer(self):
        print(f"timeout: {self.timeout}")
        import time
        i = 0
        while i <= self.timeout:
            print(f"timer: {i}")
            time.sleep(1)
            i += 1

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, _url: str):
        if self.is_url_valid(_url):
            self._url = str.lower(_url)
        else:
            self.error("invalid method")

    @property
    def method(self) -> str:
        return self._method

    @method.setter
    def method(self, _method: str):
        if _method is None:
            pass
        elif (_method is not None) and (_method in self.ALlOWED_METHODS):
            self._method = _method
        else:
            self.error("invalid method. allowed methods: 'GET', 'POST', 'PUT', 'DELETE', 'PATCH'.")

    @property
    def headers(self) -> dict:
        return self._headers

    @headers.setter
    def headers(self, all_headers: str):
        if all_headers is not None:
            for _headers in all_headers:
                if not self.check_format(_headers, "headers"):
                    self.error("invalid headers format")
                _headers = str.lower(_headers)
                headers_str = _headers.split(',')
                for h_str in headers_str:
                    key, value = h_str.split(':')
                    if key in self.headers.keys():
                        self.warn("repeated headers")
                    self._headers[key] = value

    @property
    def queries(self) -> dict:
        return self._queries

    @queries.setter
    def queries(self, all_queries: str):
        if all_queries is not None:
            for _queries in all_queries:
                if not self.check_format(_queries, "x-www-form-urlencoded"):
                    self.error("invalid queries format")
                _queries = str.lower(_queries)
                queries_str = _queries.split('&')
                for q_str in queries_str:
                    key, value = q_str.split('=')
                    if key in self.queries.keys():
                        self.warn("repeated headers")
                    self._queries[key] = value

    @property
    def body(self) -> str:
        return self._body

    @body.setter
    def body(self, data: str):
        _body = data[0]
        _format = data[1]
        if _body is not None:
            if not self.check_format(_body, _format):
                self.warn(f"data is not in {_format} format")

            if "content-type" not in self.headers.keys():
                self._headers["content-type"] = "application/" + _format

            if _format == 'octet-stream':
                import os.path
                if not os.path.isfile(_body):
                    self.error("invalid filename")
                with open(_body, 'rb') as file:
                    self._body = str(file.read())
            else:
                self._body = _body

    @property
    def timeout(self) -> float:
        return self._timeout

    @timeout.setter
    def timeout(self, _timeout):
        if _timeout is not None:
            self._timeout = float(_timeout)

    @staticmethod
    def is_url_valid(url: str) -> bool:
        protocols = ['http', 'https', 'ftp', 'mailto', 'file', 'data']

        try:
            url = str.lower(url)

            has_protocol = False
            for protocol in protocols:
                if protocol in url:
                    if url.index(protocol) == 0:
                        has_protocol = True

            if not has_protocol:
                url = 'http://' + url
            return validators.url(url) is True

        except Exception:
            return False

    @staticmethod
    def check_format(_data: str, _format: str) -> bool:
        if _format == "x-www-form-urlencoded":
            lst = _data.split('&')
            for w in lst:
                if len(w.strip().split("=")) != 2:
                    return False

        elif _format == "headers":
            lst = _data.split(',')
            for w in lst:
                if len(w.strip().split(":")) != 2:
                    return False

        elif _format == "json":
            import json
            try:
                a_json = json.loads(_data)
            except Exception:
                return False

        return True

    @staticmethod
    def error(msg: str) -> None:
        print(f"Error: {msg}")
        exit(-1)

    @staticmethod
    def warn(msg: str):
        print(f"Warning: {msg}")

    def __str__(self):
        return f"url: {self.url}\nmethod: {self.method}\nheaders: {self.headers}\nqueries: {self.queries}\nbody: {self.body}"


def check_body_flags(req, _data, _json, _file):
    body_flags_counter = 0
    if _data is not None:
        body_flags_counter += 1
    if _json is not None:
        body_flags_counter += 1
    if _file is not None:
        body_flags_counter += 1

    if body_flags_counter > 1:
        req.error("inserted multiple body content")


def main():
    req = HTTPRequest()
    check_body_flags(req, args.data, args.json, args.file)
    req.url = args.url
    req.method = args.method
    req.headers = args.headers
    req.queries = args.queries
    req.body = (args.data, "x-www-form-urlencoded")
    req.body = (args.json, "json")
    req.body = (args.file, "octet-stream")
    req.timeout = args.timeout
    # print(req, "\n\n\n")
    req.send()


if __name__ == '__main__':
    main()
