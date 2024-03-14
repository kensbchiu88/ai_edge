import os
import cv2
import uuid

from app.core.error import AppError
class VideoService:

    """
    Save the first frame of a video as an image file.
    
    Parameters:
        uri (str): The URI of the video file.
    
    Returns:
        str: The file path of the saved image.
    """
    def save_frame_as_image(self, uri):
        cap = cv2.VideoCapture(uri)
        success, frame = cap.read()
        cap.release()

        if not success:
            raise AppError("Unable to read video file")
        
        temp_img_path = os.path.join("temp/", str(uuid.uuid4()) + ".jpg")
        cv2.imwrite(temp_img_path, frame)

        return temp_img_path