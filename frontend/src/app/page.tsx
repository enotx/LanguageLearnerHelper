'use client';

import { useState, useRef } from 'react';
import { AudioRecorder } from '@/components/AudioRecorder';
import styles from '@/app/page.module.css';

export default function Home() {
  const [audioProperties, setAudioProperties] = useState<any>(null);

  return (
    <main className={styles.container}>
      <h1 className={styles.title}>Audio Recorder</h1>
      
      <AudioRecorder 
        onRecordingComplete={setAudioProperties}
      />

      {audioProperties && (
        <div className={styles.audioProperties}>
          <h2>Audio Properties:</h2>
          <pre>{JSON.stringify(audioProperties, null, 2)}</pre>
        </div>
      )}
    </main>
  );
}