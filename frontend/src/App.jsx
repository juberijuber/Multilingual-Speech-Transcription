/**
 * App.jsx — Root application component.
 *
 * Manages tab navigation between Recorder and History pages.
 * Loads provider info on mount.
 */

import { useEffect, useState } from 'react';
import { speechApi } from './api';
import ToastContainer from './components/Toast';
import { useToast } from './hooks/useToast';
import HistoryPage from './pages/HistoryPage';
import RecorderPage from './pages/RecorderPage';

export default function App() {
  const [activeTab, setActiveTab]     = useState('recorder');
  const [providerInfo, setProviderInfo] = useState(null);
  const [historyKey, setHistoryKey]   = useState(0);

  const { toasts, toast } = useToast();

  // Load provider info on mount
  useEffect(() => {
    speechApi.providerInfo()
      .then(setProviderInfo)
      .catch(() => {
        // Backend not running yet — that's okay
        setProviderInfo({ is_mock: true, provider: 'unavailable' });
      });
  }, []);

  const handleSaved = () => {
    toast.success('Transcription saved to history!');
    setHistoryKey(k => k + 1); // refresh history if user switches tabs
  };

  return (
    <div className="app">
      {/* ── Header ──────────────────────────────────────────────────── */}
      <header className="app-header">
        <div className="container">
          <div className="header-inner">
            <div className="logo">
              <div className="logo-icon" aria-hidden="true">🎙</div>
              <div>
                <div className="logo-text">VoiceLens</div>
                <div className="logo-tagline">Multilingual Speech Transcription</div>
              </div>
            </div>

            <nav aria-label="Main navigation">
              <div className="nav-tabs" role="tablist">
                <button
                  id="tab-recorder"
                  className={`nav-tab ${activeTab === 'recorder' ? 'active' : ''}`}
                  role="tab"
                  aria-selected={activeTab === 'recorder'}
                  aria-controls="panel-recorder"
                  onClick={() => setActiveTab('recorder')}
                >
                  🎙 Recorder
                </button>
                <button
                  id="tab-history"
                  className={`nav-tab ${activeTab === 'history' ? 'active' : ''}`}
                  role="tab"
                  aria-selected={activeTab === 'history'}
                  aria-controls="panel-history"
                  onClick={() => {
                    setActiveTab('history');
                    setHistoryKey(k => k + 1);
                  }}
                >
                  📋 History
                </button>
              </div>
            </nav>
          </div>
        </div>
      </header>

      {/* ── Main ────────────────────────────────────────────────────── */}
      <main className="main-content">
        <div className="container">
          {activeTab === 'recorder' && (
            <section id="panel-recorder" role="tabpanel" aria-labelledby="tab-recorder">
              <div className="page-header">
                <h1 className="page-title">Record &amp; Transcribe</h1>
                <p className="page-subtitle">
                  Speak in any language — Faster-Whisper will transcribe in real time.
                </p>
              </div>
              <RecorderPage
                onSaved={handleSaved}
                providerInfo={providerInfo}
              />
            </section>
          )}

          {activeTab === 'history' && (
            <section id="panel-history" role="tabpanel" aria-labelledby="tab-history">
              <HistoryPage
                refreshKey={historyKey}
                toast={toast}
              />
            </section>
          )}
        </div>
      </main>

      {/* ── Footer ──────────────────────────────────────────────────── */}
      <footer style={{
        borderTop: '1px solid var(--clr-border)',
        padding: 'var(--sp-md) 0',
        textAlign: 'center',
        color: 'var(--clr-text-3)',
        fontSize: '0.78rem',
      }}>
        <div className="container">
          VoiceLens · Powered by Faster-Whisper · Built with React + FastAPI
        </div>
      </footer>

      {/* ── Toasts ──────────────────────────────────────────────────── */}
      <ToastContainer toasts={toasts} />
    </div>
  );
}
