from typing import List
from pydantic import BaseModel
import requests
import urllib.parse

from app.core.config import settings
from app.core.error import AppError

class LabelService:
    def __init__(self):
        pass

    def get_labels_by_uri(self, uri: str) -> List['LabelService.GetLabelOutputDto']:
        result = []
        # 抓取stream_data_id
        params = { 'uri' : uri}
        param_encoded = urllib.parse.urlencode(params)
        get_streaming_url = f"{settings.LABELING_SYSTEM_URI}{settings.GET_STREAMING_API}?{param_encoded}"

        response = requests.get(get_streaming_url)
        if response.status_code == 200:
            data = response.json()
            if data:
                first_data = data[0]
                streaming_id = first_data.get("id")
        else:
            print('Error:', response.status_code)
            raise AppError(message="Failed to get labeled data(streaming_data_id).")
        
        # 抓取labeled data
        get_label_url = f"{settings.LABELING_SYSTEM_URI}{settings.GET_LABEL_API}".replace("{id}", str(streaming_id))
        response = requests.get(get_label_url)
        if response.status_code == 200:
            for label in response.json():
                if label.get("type") == settings.LABEL_TYPE:
                    dto = LabelService.GetLabelOutputDto(**label)
                    result.append(dto)
        else:
            print('Error:', response.status_code)
            raise AppError(message="Failed to get labeled data.")
        
        return result
    
    class GetLabelOutputDto(BaseModel):
        streaming_data_id: int
        equipment_no: str
        x1: int
        y1: int
        x2: int
        y2: int


