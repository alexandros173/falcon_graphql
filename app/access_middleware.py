import math
import time
import logging
from falcon import Response, Request


class AccessMiddleware:

    async def process_request(self, req: Request, resp: Response) -> None:
        resp.set_header('timer', str(time.time()))

    async def process_response(self, req: Request, resp: Response, resource: object, params: dict) -> None:
        logging.info(
            req,
            req.get_header('x-request-id'), req.access_route[0],
            req.method, req.relative_uri, req.get_header('User-Agent'),
            int(resp.status[:3]), len(str(resp.media)),
            math.ceil((time.time() - float(resp.get_header('timer'))) * 1000),
            'HTTP/1.1')
