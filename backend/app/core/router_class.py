import json
import time

from fastapi import Request, Response
from fastapi.routing import APIRoute

from app.api.v1.module_system.log.model import OperationLogModel
from app.config.setting import settings
from app.core.database import async_db_session


class OperationLogRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            start = time.time()
            response: Response = await original_route_handler(request)
            if (
                settings.OPERATION_LOG_RECORD
                and request.method in settings.OPERATION_RECORD_METHOD
                and self.name not in settings.IGNORE_OPERATION_FUNCTION
            ):
                payload = ""
                try:
                    body = await request.body()
                    payload = body.decode("utf-8", errors="ignore")[:2000]
                except Exception:
                    payload = ""
                async with async_db_session() as session:
                    async with session.begin():
                        log = OperationLogModel(
                            type=2 if request.scope.get("user_id") else 1,
                            request_path=request.url.path,
                            request_method=request.method,
                            request_payload=payload,
                            request_ip=request.client.host if request.client else None,
                            response_code=response.status_code,
                            response_json=json.dumps({"status_code": response.status_code}),
                            process_time=f"{time.time() - start:.2f}s",
                            description=self.summary,
                            created_id=request.scope.get("user_id"),
                            updated_id=request.scope.get("user_id"),
                        )
                        session.add(log)
            return response

        return custom_route_handler
