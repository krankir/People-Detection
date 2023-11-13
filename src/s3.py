import asyncio
import os
import pathlib

from minio import Minio, S3Error
import cv2

from src.config import settings
from tempfile import TemporaryDirectory


minio_host = settings.minio_host
minio_port = settings.minio_port
minio_url = f'{minio_host}:{minio_port}'
minio_user = settings.minio_user
minio_password = settings.minio_password
bucket_name = settings.bucket_name


minioClient = Minio(
    minio_url,
    access_key=minio_user,
    secret_key=minio_password,
    secure=False
)
found = minioClient.bucket_exists(bucket_name)
if not found:
    minioClient.make_bucket(bucket_name)


async def get_cloud_file():
    """Получение названия файлов из хранилища."""
    found = minioClient.bucket_exists(bucket_name)
    if not found:
        minioClient.make_bucket(bucket_name)
    loop = asyncio.get_running_loop()
    objects = await loop.run_in_executor(None, minioClient.list_objects, bucket_name)
    return objects


async def download_file_in_minio(filename, path_file):
    """Загрузка файла в minio."""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, minioClient.fput_object, bucket_name, filename, path_file)


async def download_file_from_minio(filename: str):
    """Получение файлов из хранилища."""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, minioClient.fput_object, bucket_name, filename, filename)
