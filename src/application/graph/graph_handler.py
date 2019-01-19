import os
import tempfile
from asyncio import coroutine

import tornado.web


from src.application.base_handler import BaseHandler
from src.application.graph.new import StreamingFormDataParser, StreamingFormDataParserDelegate

COMMON_URL = '/graph'


@tornado.web.stream_request_body
class GraphHandler(BaseHandler, StreamingFormDataParser):
    URL = f'{COMMON_URL}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.files_id = None
        self.parser = None
        self.file = None

    async def post(self):
        a=1
        await self.finish()
        self.request

    @coroutine
    def prepare(self):
        if self.request.method == 'POST':
            self.files_id = []
            try:
                self.parser = StreamingFormDataParser(self)
            except Exception as e:
                self.set_status(500)
                return self.finish({'error': {
                    'code': 500,
                    'message': 'Invalid multipart/form-data',
                }})

    async def data_received(self, chunk: bytes):
        if self.request.method == 'POST':
            try:
                await self.parser.data_received(chunk)
            except Exception as e:
                self.exception(e)
                self.set_status(BAD_REQUEST)
                await self.finish({'error': {
                    'code': BAD_REQUEST,
                    'message': 'Invalid multipart/form-data',
                }})

    def start_file(self, headers, disp_params):
        filename = disp_params.get('filename', None)

        if self.file and not self.file.closed:
            yield self.file.close()
            self.set_status(BAD_REQUEST)
            return self.finish({'error': {
                'code': BAD_REQUEST,
                'message': 'Invalid multipart/form-data',
            }})

        self.file = yield self.fs.new_file(filename=filename)

    def finish_file(self):
        if not self.file or self.file.closed:
            self.warning('file is not opened or is already closed. Invalid multipart/form-data')
            return
        self.files_id.append(str(self.file._id))
        yield self.file.close()

    def file_data_received(self, file_data):
        try:
            yield self.file.write(file_data)
        except Exception as e:
            self.exception(e)
            yield self.file.close()

    @classmethod
    def tornado_url(cls):
        return tornado.web.url(cls.URL, cls, name="graph")
