# backend/app/api/routes.py
from fastapi import APIRouter, UploadFile, File #, WebSocket, WebSocketDisconnect, Depends, HTTPException
import logging
# import json
from app.services.audio_processing import AudioSegmentation
from pydub import AudioSegment
import io
import tempfile
import os
# import pickle

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/audioCheck")
async def process_audio(audio: UploadFile = File(...)):
    try:
        # 创建临时文件来保存上传的音频
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            # 写入上传的音频数据
            content = await audio.read()
            temp_file.write(content)
            temp_file.flush()
            
            # 使用 pydub 读取音频文件
            # audio_segment = AudioSegment.from_file(temp_file.name, format="webm")
            audio_segment = AudioSegmentation(temp_file.name)
            # properties = audio_segment.getProperies()
            ipa = audio_segment.recognize()
            
            # 获取音频属性
            # properties = {
            #     "channels": audio_segment.channels,
            #     "sample_width_bytes": audio_segment.sample_width,
            #     "frame_rate_hz": audio_segment.frame_rate,
            #     "duration_seconds": len(audio_segment) / 1000.0,
            #     "frame_count": len(audio_segment.get_array_of_samples()),
            #     "file_size_bytes": os.path.getsize(temp_file.name)
            # }
            
            # 删除临时文件
            os.unlink(temp_file.name)
            
            return ipa
            
    except Exception as e:
        return {"error": f"Error processing audio: {str(e)}"}
