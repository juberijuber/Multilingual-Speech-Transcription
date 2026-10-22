/**
 * RecorderPage.jsx — Main recording interface.
 *
 * Flow:
 *   1. User presses record → microphone permission requested
 *   2. Audio is captured via MediaRecorder
 *   3. On stop → blob sent to POST /api/speech/transcribe
 *   4. Transcript shown → user can save to database
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { speechApi, transcriptionsApi } from '../api';
import WaveformVisualizer from '../components/WaveformVisualizer';
import { RECORDER_STATE, formatDuration, useRecorder } from '../hooks/useRecorder';

const LANGUAGES = [
  { code: '',   label: '🌐 Auto-detect' },
  { code: 'en', label: '🇬🇧 English' },
  { code: 'hi', label: '🇮🇳 Hindi (हिन्दी)' },
  { code: 'fr', label: '🇫🇷 French' },
  { code: 'de', label: '🇩🇪 German' },
  { code: 'es', label: '🇪🇸 Spanish' },
  { code: 'zh', label: '🇨🇳 Chinese' },
  { code: 'ar', label: '🇸🇦 Arabic' },
  { code: 'pt', label: '🇧🇷 Portuguese' },
  { code: 'ru', label: '🇷🇺 Russian' },
  { code: 'ja', label: '🇯🇵 Japanese' },
  { code: 'ko', label: '🇰🇷 Korean' },
  { code: 'ur', label: '🇵🇰 Urdu' },
  { code: 'bn', label: '🇧🇩 Bengali' },
  { code: 'ta', label: '🇮🇳 Tamil' },
  { code: 'te', label: '🇮🇳 Telugu' },
];

export default function RecorderPage({ onSaved, providerInfo }) {
  const [language, setLanguage]         = useState('');
  const [transcript, setTranscript]     = useState('');
  const [transcriptMeta, setTranscriptMeta] = useState(null); // { language, duration, is_mock }
  const [error, setError]               = useState('');
  const [showSavePanel, setShowSavePanel] = useState(false);
  const [saveTitle, setSaveTitle]       = useState('');
  const [saving, setSaving]             = useState(false);
  const [saveSuccess, setSaveSuccess]   = useState(false);

  const audioBlobRef = useRef(null);

  // ── Recorder hook ──────────────────────────────────────────────────────
  const handleComplete = useCallback(async (blob) => {
    audioBlobRef.current = blob;
    setError('');

    // Send to backend for transcription
    try {
      const result = await speechApi.transcribe(blob, language || null);
      setTranscript(result.transcript);
      setTranscriptMeta({
        language: result.language,
        duration: result.duration_seconds,
        isMock: result.is_mock,
        provider: result.provider,
      });
      setShowSavePanel(true);
      setSaveTitle(generateTitle());
      setSaveSuccess(false);
    } catch (err) {
      setError(`Transcription failed: ${err.message}`);
    }

    recorder.reset();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [language]);

  const handleError = useCallback((msg) => {
    setError(msg);
  }, []);

  const recorder = useRecorder({ onComplete: handleComplete, onError: handleError });

  // ── Toggle recording ───────────────────────────────────────────────────
  const handleToggle = () => {
    if (recorder.isIdle) {
      recorder.startRecording();
    } else if (recorder.isRecording) {
      recorder.stopRecording();
    }
  };

  // ── Save transcription ─────────────────────────────────────────────────
  const handleSave = async () => {
    if (!transcript.trim()) return;
    setSaving(true);
    try {
      await transcriptionsApi.create({
        title: saveTitle || 'Untitled Recording',
        transcript,
        language: transcriptMeta?.language || null,
        duration_seconds: transcriptMeta?.duration || null,
        provider: transcriptMeta?.provider || 'faster_whisper',
      });
      setSaveSuccess(true);
      setShowSavePanel(false);
      onSaved?.();
    } catch (err) {
      setError(`Could not save: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  // ── Discard ────────────────────────────────────────────────────────────
  const handleDiscard = () => {
    setTranscript('');
    setTranscriptMeta(null);
    setShowSavePanel(false);
    setSaveSuccess(false);
    audioBlobRef.current = null;
  };

  const isRecording = recorder.isRecording;

  return (
    <div className="recorder-section">
      {/* Provider info banner */}
      {providerInfo && (
        <div className={`provider-banner ${providerInfo.is_mock ? 'mock' : 'real'}`}>
          {providerInfo.is_mock ? '⚠️' : '✓'}
          {providerInfo.is_mock
            ? ' Demo mode — no real speech recognition. Set SPEECH_PROVIDER=faster_whisper to enable.'
            : ` Faster-Whisper is active — real speech recognition enabled (${providerInfo.supported_languages?.length ?? 99}+ languages)`}
        </div>
      )}

      {/* Main recorder card */}
      <div className={`recorder-card ${isRecording ? 'recording' : ''}`}>
        {/* Controls row */}
        <div className="recorder-controls">
          {/* Record / Stop button */}
          <button
            id="record-toggle-btn"
            className={`btn-record ${isRecording ? 'recording' : ''}`}
            onClick={handleToggle}
            disabled={recorder.isRequesting || recorder.isProcessing}
            aria-label={isRecording ? 'Stop recording' : 'Start recording'}
            title={isRecording ? 'Stop recording' : 'Start recording'}
          >
            {isRecording && <div className="record-ring" />}
            {recorder.isRequesting  ? '⏳' : isRecording ? '⏹' : '🎙'}
          </button>

          {/* Status */}
          <div className="recorder-status">
            <div className="status-label">
              <div className={`status-dot ${isRecording ? 'active' : recorder.isProcessing ? 'processing' : ''}`} />
              {recorder.isRequesting  ? 'Requesting microphone…'
                : isRecording         ? 'Recording'
                : recorder.isProcessing ? 'Transcribing…'
                : 'Ready to record'}
            </div>
            <div className="status-hint">
              {isRecording
                ? 'Click ⏹ to stop and transcribe'
                : recorder.isProcessing
                ? 'Processing audio with Faster-Whisper…'
                : 'Click 🎙 to start recording'}
            </div>
          </div>

          {/* Timer */}
          {isRecording && (
            <div className="timer" aria-live="polite" aria-atomic="true">
              {formatDuration(recorder.elapsed)}
            </div>
          )}

          {/* Language selector */}
          {!isRecording && !recorder.isProcessing && (
            <div className="language-selector">
              <label htmlFor="language-select" className="select-label">Language</label>
              <select
                id="language-select"
                className="lang-select"
                value={language}
                onChange={e => setLanguage(e.target.value)}
                aria-label="Select transcription language"
              >
                {LANGUAGES.map(l => (
                  <option key={l.code} value={l.code}>{l.label}</option>
                ))}
              </select>
            </div>
          )}
        </div>

        {/* Waveform */}
        {isRecording && (
          <WaveformVisualizer audioLevel={recorder.audioLevel} isActive={isRecording} />
        )}

        {/* Transcript area */}
        <div className={`transcript-area ${isRecording ? 'active-recording' : ''}`}>
          {recorder.isProcessing ? (
            <div className="loading-row">
              <div className="spinner" />
              <span>Transcribing audio…</span>
            </div>
          ) : transcript ? (
            <>
              <p className="transcript-text">{transcript}</p>
              {isRecording && <span className="transcript-cursor" />}
            </>
          ) : (
            <p className="transcript-placeholder">
              {isRecording
                ? 'Speak now — transcript will appear here after you stop…'
                : 'Your transcript will appear here after recording.'}
            </p>
          )}
        </div>

        {/* Transcript metadata badges */}
        {transcriptMeta && !isRecording && (
          <div className="transcript-actions">
            <div className="transcript-meta">
              {transcriptMeta.language && (
                <span className="meta-badge">
                  🌐 {transcriptMeta.language.toUpperCase()}
                </span>
              )}
              {transcriptMeta.duration > 0 && (
                <span className="meta-badge">
                  ⏱ {transcriptMeta.duration.toFixed(1)}s
                </span>
              )}
              <span className="meta-badge">🤖 {transcriptMeta.provider}</span>
              {transcriptMeta.isMock && (
                <span className="meta-badge mock">⚠️ Demo text</span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Error alert */}
      {error && (
        <div className="alert alert-error" role="alert">
          <span>⚠️</span>
          <span>{error}</span>
          <button
            className="btn btn-ghost btn-sm"
            onClick={() => setError('')}
            style={{ marginLeft: 'auto' }}
            aria-label="Dismiss error"
          >✕</button>
        </div>
      )}

      {/* Browser support check */}
      {typeof window !== 'undefined' && !window.MediaRecorder && (
        <div className="alert alert-warn" role="alert">
          ⚠️ Your browser does not support the MediaRecorder API. Please use a modern browser (Chrome, Edge, Firefox).
        </div>
      )}

      {/* Save panel */}
      {showSavePanel && transcript && (
        <div className="save-panel">
          <span style={{ color: 'var(--clr-text-2)', fontSize: '0.875rem', whiteSpace: 'nowrap' }}>
            Save as:
          </span>
          <input
            id="save-title-input"
            type="text"
            placeholder="Recording title…"
            value={saveTitle}
            onChange={e => setSaveTitle(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSave()}
            aria-label="Recording title"
            maxLength={255}
          />
          <button
            id="save-transcription-btn"
            className="btn btn-primary"
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? <><div className="spinner spinner-sm" /> Saving…</> : '💾 Save'}
          </button>
          <button
            id="discard-transcription-btn"
            className="btn btn-ghost"
            onClick={handleDiscard}
          >
            Discard
          </button>
        </div>
      )}

      {/* Save success */}
      {saveSuccess && (
        <div className="alert alert-success" role="status">
          ✓ Transcription saved! View it in the History tab.
        </div>
      )}
    </div>
  );
}

function generateTitle() {
  const now = new Date();
  return `Recording ${now.toLocaleDateString()} ${now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
}
