import os
from multiprocessing import Pool, Lock, Manager
from minio import Minio
import cv2 as cv
import tempfile
import face_recognition

from app.logger import logger
from worker.app.config import app_config
import concurrent.futures


minio_host = app_config.minio_host
minio_port = app_config.minio_port
minio_url = f'{minio_host}:{minio_port}'
minio_user = app_config.minio_user
minio_password = app_config.minio_password
bucket_name = app_config.bucket_name


minioClient = Minio(
    minio_url,
    access_key=minio_user,
    secret_key=minio_password,
    secure=False
)

video_urls = [
    "Галь Гадот О Своей Груди, Юридической Школе И Конкурсах Красоты.mp4",
    "Жена только уложила детей спать и я который подавился.mp4",
    "Занятия фитнесом на удаленке.mp4",
    "Воздушный шар и бенгальский огонь гремучая смесь.mp4",
    "Как я вижу мужчин 2003 года рождения и как есть на самом деле.mp4"]


def process_video(filename):
    logger.info("Starting detected_face!!!!!!")
    # Читаем файл с видео
    global video_urls
    fp_ = tempfile.NamedTemporaryFile(
        mode='w+b',
        suffix='.mp4',
        dir='/tmp',
        delete=True,
    )
    fp_name = ((fp_.name).split('/'))[-1]
    minioClient.fget_object(bucket_name, filename, fp_name)
    video_urls.remove(filename)
    cap = cv.VideoCapture(f'{fp_name}')
    count = 0
    count_percent = 0
    fps = int(cap.get(cv.CAP_PROP_FPS))
    # Получение общего количества кадров
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    logger.info(f"total frame = {total_frames}")
    one_percent_frame = round((total_frames / 100))
    count_frame = one_percent_frame
    print(one_percent_frame)
    try:
            while cap.isOpened():
                multiplier = fps * 40 # промежуток между которыми мы будем делать скриншот
                ret, frame = cap.read()
                if not ret:
                    break
                frame_id = int(round(cap.get(1)))
                if frame_id >= one_percent_frame:
                    print(f'если{frame_id} больше или ровно {one_percent_frame} и это {count_percent}%')
                    one_percent_frame += count_frame
                    count_percent += 1
                elif frame_id == total_frames:
                    print(f'если{frame_id} больше или ровно {one_percent_frame} и это 100%')

                if frame_id % multiplier == 0:
                    fp = tempfile.NamedTemporaryFile(
                        mode='w+b',
                        suffix='.jpg',
                        dir='/tmp',
                        delete=True,
                    )
                    cv.imwrite(fp.name, frame)
                    face_img = face_recognition.load_image_file(fp)
                    im_face_locations = face_recognition.face_locations(face_img)
                    print(f'Обнаружено лиц на фрейме --> {len(im_face_locations)}')
                    count += 1
                    fp.close()
                    # os.remove(fp.name)  # Удаление временного файла
            print(f'Найдено лиц в видео {count}')
            return count
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        # Высвобождаем ресурсы
    finally:
        os.remove(fp_name)
        fp_.close()# Удаление временного файла

        cap.release()
        cv.destroyAllWindows()


# if __name__ == '__main__':
#     filename = 'Галь Гадот О Своей Груди, Юридической Школе И Конкурсах Красоты.mp4'
#     process_video(filename)
# if __name__ == "__main__":
#     video_urls = ["Галь Гадот О Своей Груди, Юридической Школе И Конкурсах Красоты.mp4", "Жена только уложила детей спать и я который подавился.mp4", "Занятия фитнесом на удаленке.mp4", "Воздушный шар и бенгальский огонь гремучая смесь.mp4",
#                   "Как я вижу мужчин 2003 года рождения и как есть на самом деле.mp4"]
#
#     workers = 2
#
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         for i in range(workers):
#             for j in video_urls:
#                 executor.submit(process_video, j)
