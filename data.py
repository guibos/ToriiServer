import tornado.web
from tornado import gen

import base


class DataHandler(tornado.web.StaticFileHandler, base.BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, path, include_body=True):
        # Set up our path instance variables.
        self.path = self.parse_url_path(path)
        del path  # make sure we don't refer to path instead of self.path again
        absolute_path = self.get_absolute_path(self.root, self.path)
        self.absolute_path = self.validate_absolute_path(
            self.root, absolute_path)
        if self.absolute_path is None:
            return

        self.modified = self.get_modified_time()
        self.set_headers()

        if self.should_return_304():
            self.set_status(304)
            return

        request_range = None
        range_header = self.request.headers.get("Range")
        if range_header:
            # As per RFC 2616 14.16, if an invalid Range header is specified,
            # the request will be treated as if the header didn't exist.
            request_range = httputil._parse_request_range(range_header)

        size = self.get_content_size()
        if request_range:
            start, end = request_range
            if (start is not None and start >= size) or end == 0:
                # As per RFC 2616 14.35.1, a range is not satisfiable only: if
                # the first requested byte is equal to or greater than the
                # content, or when a suffix with length 0 is specified
                self.set_status(416)  # Range Not Satisfiable
                self.set_header("Content-Type", "text/plain")
                self.set_header("Content-Range", "bytes */%s" % (size,))
                return
            if start is not None and start < 0:
                start += size
            if end is not None and end > size:
                # Clients sometimes blindly use a large range to limit their
                # download size; cap the endpoint at the actual file size.
                end = size
            # Note: only return HTTP 206 if less than the entire range has been
            # requested. Not only is this semantically correct, but Chrome
            # refuses to play audio if it gets an HTTP 206 in response to
            # ``Range: bytes=0-``.
            if size != (end or size) - (start or 0):
                self.set_status(206)  # Partial Content
                self.set_header("Content-Range",
                                httputil._get_content_range(start, end, size))
        else:
            start = end = None

        if start is not None and end is not None:
            content_length = end - start
        elif end is not None:
            content_length = end
        elif start is not None:
            content_length = size - start
        else:
            content_length = size
        self.set_header("Content-Length", content_length)

        if include_body:
            content = self.get_content(self.absolute_path, start, end)
            if isinstance(content, bytes):
                content = [content]
            for chunk in content:
                try:
                    self.write(chunk)
                    yield self.flush()
                except iostream.StreamClosedError:
                    return
        else:
            assert self.request.method == "HEAD"
