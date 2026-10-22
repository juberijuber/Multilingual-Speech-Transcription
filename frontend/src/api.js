/**
 * api.js — Centralized API client for the FastAPI backend.
 *
 * All paths are relative so they are proxied by the Vite dev server
 * (→ http://localhost:8000) in development, and served from the same
 * origin in production.
 */

const BASE = '/api';

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, options);

  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch {
      // ignore parse error
    }
    throw new Error(detail);
  }

  if (res.status === 204) return null;
  return res.json();
}

// ── Transcriptions CRUD ───────────────────────────────────────────────────

export const transcriptionsApi = {
  /**
   * @param {object} params  { search, page, page_size }
   * @returns {Promise<{ items, total, page, page_size, has_next, has_prev }>}
   */
  list({ search = '', page = 1, page_size = 10 } = {}) {
    const q = new URLSearchParams({ search, page, page_size });
    return request(`/transcriptions?${q}`);
  },

  get(id) {
    return request(`/transcriptions/${id}`);
  },

  /**
   * @param {{ title, transcript, language, duration_seconds, provider }} data
   */
  create(data) {
    return request('/transcriptions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  },

  /**
   * @param {string} id
   * @param {{ title?, transcript?, language? }} data
   */
  update(id, data) {
    return request(`/transcriptions/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  },

  delete(id) {
    return request(`/transcriptions/${id}`, { method: 'DELETE' });
  },
};

// ── Speech ────────────────────────────────────────────────────────────────

export const speechApi = {
  /** Return info about the active speech provider. */
  providerInfo() {
    return request('/speech/provider-info');
  },

  /**
   * Transcribe an audio blob.
   * @param {Blob} audioBlob
   * @param {string|null} language  BCP-47 language code or null for auto-detect
   * @returns {Promise<{ transcript, language, duration_seconds, provider, is_mock }>}
   */
  transcribe(audioBlob, language = null) {
    const form = new FormData();
    form.append('audio', audioBlob, 'recording.webm');
    if (language) form.append('language', language);
    return request('/speech/transcribe', { method: 'POST', body: form });
  },
};
