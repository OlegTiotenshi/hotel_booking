import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks
from src.tasks.tasks import resize_image_celery, resize_image_background_tasks

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("/celery")
def upload_image_celery(file: UploadFile):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_image_celery.delay(image_path)


@router.post("/background-tasks")
def upload_image_background_tasks(file: UploadFile, background_tasks: BackgroundTasks):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    background_tasks.add_task(resize_image_background_tasks, image_path)
