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



# filename = 'Галь Гадот О Своей Груди, Юридической Школе И Конкурсах Красоты.mp4'
# object_key = minioClient.fget_object(bucket_name, filename, '1.mp4')

# input_video = '1.mp4'
#
# # Откройте видеофайл с использованием OpenCV
# cap = cv2.VideoCapture(input_video)

# # Получите общую длительность видео
# total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
# total_duration = total_frames / frame_rate
#
# # Закройте видеофайл
# cap.release()
#
# print(total_frames)
# print(frame_rate)
# print(f'Общая длительность видео: {total_duration} секунд')


# with tempfile.TemporaryDirectory() as tmp:
#     # имя временного каталога
#     print('Имя временного каталога:', tmp)
#     path_dir = pathlib.Path(tmp)
#     a_file = path_dir / 'a_file.txt'
#     print(path_dir)