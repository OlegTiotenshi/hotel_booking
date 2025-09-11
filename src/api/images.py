from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImagesService

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("/celery")
def upload_image_celery(file: UploadFile):
    ImagesService().upload_image_celery(file)


@router.post("/background-tasks")
def upload_image_background_tasks(file: UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_image_background_tasks(file, background_tasks)
