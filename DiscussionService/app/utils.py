import logging
from typing import Optional

import requests
from fastapi import HTTPException, UploadFile, status

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

USER_SERVICE_URL = "http://user_service:7000"
API_TOKEN = "6d207e02198a847aa98d0a2a901485a5"


def get_current_user_from_user_service(token: str) -> Optional[dict]:
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{USER_SERVICE_URL}/user/get_current_user", headers=headers)

        response.raise_for_status()
        current_user = response.json()

        return current_user

    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to user_service: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error connecting to user_service: {str(e)}")

    except ValueError as ve:
        logger.error(f"Error converting user_id to integer: {str(ve)}")
        raise HTTPException(status_code=500, detail="Error converting user_id to integer")

    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException as e:
        raise e


# 62859be54313b73a7ba8c95e09d561f6

def upload_to_imgbb(file: UploadFile):
    url = "https://api.imgbb.com/1/upload"
    params = {
        "key": "62859be54313b73a7ba8c95e09d561f6",
        "name": file.filename
    }

    try:
        files = {"image": (file.filename, file.file, file.content_type)}
        response = requests.post(url, params=params, files=files)

        response.raise_for_status()

        data = response.json()

        if data.get("data", {}).get("url"):
            return data["data"]["url"]
        else:
            error_message = data.get("error", {}).get("message", "Unknown error")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Upload failed: {error_message}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error uploading file: {str(e)}")


def get_user_by_id(user_id: int, token: str) -> Optional[dict]:
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}", headers=headers)

        response.raise_for_status()
        user_data = response.json()

        return user_data

    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to user_service: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error connecting to user_service: {str(e)}")

    except ValueError as ve:
        logger.error(f"Error converting user_id to integer: {str(ve)}")
        raise HTTPException(status_code=500, detail="Error converting user_id to integer")

    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))