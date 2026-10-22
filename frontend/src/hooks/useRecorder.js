/**
 * useRecorder.js — Custom hook for microphone recording with MediaRecorder API.
 *
 * States:
 *   idle → requesting → recording → processing → idle
 *
 * The hook chunks audio data into an array while recording, then merges
 * everything into a single Blob when stopped.
 */

import { useCallback, useEffect, useRef, useState } from 'react';

export const RECORDER_STATE = {
  IDLE:        'idle',
  REQUESTING:  'requesting',
  RECORDING:   'recording',
  PROCESSING:  'processing',
};

/**
 * @param {object} opts
 * @param {(blob: Blob) => void} opts.onComplete   called with the final audio Blob
 * @param {(err: string) => void} opts.onError
 */
export function useRecorder({ onComplete, onError } = {}) {
  const [state, setState]         = useState(RECORDER_STATE.IDLE);
  const [elapsed, setElapsed]     = useState(0);   // seconds
  const [audioLevel, setAudioLevel] = useState(0); // 0-100 for waveform

  const mediaRecorderRef = useRef(null);
  const streamRef        = useRef(null);
  const chunksRef        = useRef([]);
  const timerRef         = useRef(null);
  const analyserRef      = useRef(null);
  const animFrameRef     = useRef(null);

  // ── Cleanup ──────────────────────────────────────────────────────────────
  const cleanup = useCallback(() => {
    clearInterval(timerRef.current);
    cancelAnimationFrame(animFrameRef.current);

    if (streamRef.current) {
      streamRef.current.getTracks().forEach(t => t.stop());
      streamRef.current = null;
    }
    mediaRecorderRef.current = null;
    analyserRef.current = null;
    chunksRef.current = [];
  }, []);

  useEffect(() => () => cleanup(), [cleanup]);

  // ── Audio level analyser ─────────────────────────────────────────────────
  const startAnalyser = useCallback((stream) => {
    try {
      const ctx = new AudioContext();
      const source = ctx.createMediaStreamSource(stream);
      const analyser = ctx.createAnalyser();
      analyser.fftSize = 256;
      source.connect(analyser);
      analyserRef.current = analyser;

      const buf = new Uint8Array(analyser.frequencyBinCount);
      const tick = () => {
        analyser.getByteFrequencyData(buf);
        const avg = buf.reduce((a, b) => a + b, 0) / buf.length;
        setAudioLevel(Math.min(100, avg * 2));
        animFrameRef.current = requestAnimationFrame(tick);
      };
      tick();
    } catch {
      // AudioContext might be blocked; not critical
    }
  }, []);

  // ── Start recording ──────────────────────────────────────────────────────
  const startRecording = useCallback(async () => {
    if (state !== RECORDER_STATE.IDLE) return;
    setState(RECORDER_STATE.REQUESTING);

    let stream;
    try {
      stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          sampleRate: 16000,
          echoCancellation: true,
          noiseSuppression: true,
        },
      });
    } catch (err) {
      cleanup();
      setState(RECORDER_STATE.IDLE);
      const msg =
        err.name === 'NotAllowedError'
          ? 'Microphone permission was denied. Please allow microphone access and try again.'
          : err.name === 'NotFoundError'
          ? 'No microphone found. Please connect a microphone and try again.'
          : `Could not access microphone: ${err.message}`;
      onError?.(msg);
      return;
    }

    streamRef.current = stream;
    chunksRef.current = [];

    // Prefer opus codec for compact audio
    const mimeType = getSupportedMimeType();
    const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : {});

    recorder.ondataavailable = e => {
      if (e.data.size > 0) chunksRef.current.push(e.data);
    };

    recorder.onstop = () => {
      setState(RECORDER_STATE.PROCESSING);
      const blob = new Blob(chunksRef.current, { type: mimeType || 'audio/webm' });
      cleanup();
      onComplete?.(blob);
    };

    recorder.onerror = e => {
      cleanup();
      setState(RECORDER_STATE.IDLE);
      onError?.(`Recording error: ${e.error?.message ?? 'unknown'}`);
    };

    recorder.start(500); // collect chunks every 500ms
    mediaRecorderRef.current = recorder;
    startAnalyser(stream);
    setState(RECORDER_STATE.RECORDING);

    // Timer
    setElapsed(0);
    timerRef.current = setInterval(() => setElapsed(s => s + 1), 1000);
  }, [state, cleanup, onComplete, onError, startAnalyser]);

  // ── Stop recording ───────────────────────────────────────────────────────
  const stopRecording = useCallback(() => {
    clearInterval(timerRef.current);
    cancelAnimationFrame(animFrameRef.current);
    if (mediaRecorderRef.current?.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
  }, []);

  // ── Reset to idle ────────────────────────────────────────────────────────
  const reset = useCallback(() => {
    cleanup();
    setState(RECORDER_STATE.IDLE);
    setElapsed(0);
    setAudioLevel(0);
  }, [cleanup]);

  return {
    state,
    elapsed,
    audioLevel,
    startRecording,
    stopRecording,
    reset,
    isIdle:        state === RECORDER_STATE.IDLE,
    isRequesting:  state === RECORDER_STATE.REQUESTING,
    isRecording:   state === RECORDER_STATE.RECORDING,
    isProcessing:  state === RECORDER_STATE.PROCESSING,
  };
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function getSupportedMimeType() {
  const types = [
    'audio/webm;codecs=opus',
    'audio/webm',
    'audio/ogg;codecs=opus',
    'audio/mp4',
  ];
  return types.find(t => MediaRecorder.isTypeSupported(t)) || null;
}

/** Format seconds as MM:SS */
export function formatDuration(sec) {
  const m = Math.floor(sec / 60).toString().padStart(2, '0');
  const s = (sec % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}
