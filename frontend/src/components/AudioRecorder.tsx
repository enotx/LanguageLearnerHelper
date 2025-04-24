import { useState, useRef, useCallback } from 'react';
import styles from './AudioRecorder.module.css';

interface AudioRecorderProps {
  onRecordingComplete?: (properties: any) => void;
}

export const AudioRecorder = ({ onRecordingComplete }: AudioRecorderProps) => {
  const [isRecording, setIsRecording] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = useCallback(async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm'
      });
      
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        await sendAudioToServer(audioBlob);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error('Error accessing microphone:', err);
      setError('Failed to access microphone. Please check permissions.');
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  }, [isRecording]);

  const sendAudioToServer = async (audioBlob: Blob) => {
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.webm');

      console.log('Sending audio to server:', formData);
      console.log('API URL:', process.env.NEXT_PUBLIC_API_URL);

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/audioCheck`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (data.error) {
        setError(data.error);
      } else {
        onRecordingComplete?.(data);
      }
    } catch (err) {
      console.error('Error sending audio to server:', err);
      setError('Failed to process audio recording.');
    }
  };

  return (
    <div className={styles.recorder}>
      {error && <div className={styles.error}>{error}</div>}
      
      <div className={styles.controls}>
        {!isRecording ? (
          <button 
            className={`${styles.button} ${styles.recordButton}`}
            onClick={startRecording}
          >
            Start Recording
          </button>
        ) : (
          <button 
            className={`${styles.button} ${styles.stopButton}`}
            onClick={stopRecording}
          >
            Stop Recording
          </button>
        )}
      </div>

      <div className={styles.status}>
        {isRecording ? 'Recording...' : 'Not recording'}
      </div>
    </div>
  );
};