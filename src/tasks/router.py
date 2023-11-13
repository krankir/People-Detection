from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse

from src.amqp.service_request import ServiceHandler
from src.logger import logger
from src.s3 import get_cloud_file, download_file_in_minio

templates = Jinja2Templates(directory='src/templates')
router = APIRouter(prefix='/minio', tags=['tasks'])


@router.get("/")
async def process_request(request: Request):
    logger.info("Request started")
    return await ServiceHandler.call_service()


@router.get('/list')
async def get_minio_files_list(request: Request):
    return templates.TemplateResponse(
        'list.html',
        {
            'request': request,
            'elements': await get_cloud_file()
        }
    )


@router.post(
    '/upload',
    response_class=RedirectResponse,
    status_code=302,
)
async def upload_file_in_minio(path=Form()):
    name_file = path.split('/')[-1]
    await download_file_in_minio(name_file, path)
    return '/minio/list'

