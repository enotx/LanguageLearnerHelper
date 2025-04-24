from allosaurus.app import read_recognizer
from pydub import AudioSegment
import tempfile
import os

# model = read_recognizer()

class AudioSegmentation:
    def __init__(self, File, audioformat="webm"):
        self.audio_segment = AudioSegment.from_file(File, format=audioformat)
        self.model = read_recognizer()
        

    def process(self, audio_file):
        # 处理音频文件
        result = self.model.transcribe(audio_file)
        return result
    
    def recognize(self):
        with tempfile.NamedTemporaryFile(delete_on_close=False, suffix='.wav') as fp:
            self.audio_segment.export(fp
                                      , format="wav"
                                      , bitrate = "8k")
            ipa = self.model.recognize(fp.name)
        return ipa

    def getProperies(self):
        # 获取音频属性
        properties = {
            "channels": self.audio_segment.channels,
            "sample_width_bytes": self.audio_segment.sample_width,
            "frame_rate_hz": self.audio_segment.frame_rate,
            "duration_seconds": len(self.audio_segment) / 1000.0,
            "frame_count": len(self.audio_segment.get_array_of_samples()),
            # "file_size_bytes": os.path.getsize(File)
        }
        return properties