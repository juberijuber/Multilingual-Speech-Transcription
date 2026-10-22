/**
 * HistoryPage.jsx — Dashboard showing all saved transcriptions.
 *
 * Features:
 *   - Paginated list (10 per page)
 *   - Full-text search (title + transcript)
 *   - Expand/collapse individual cards
 *   - Edit title and transcript inline
 *   - Delete with confirmation
 *   - Copy-to-clipboard
 */

import { useCallback, useEffect, useState } from 'react';
import { transcriptionsApi } from '../api';
import ConfirmDialog from '../components/ConfirmDialog';

const PAGE_SIZE = 10;

export default function HistoryPage({ refreshKey, toast }) {
  const [data, setData]           = useState(null);  // TranscriptionPage
  const [loading, setLoading]     = useState(true);
  const [error, setError]         = useState('');
  const [search, setSearch]       = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [page, setPage]           = useState(1);
  const [expandedId, setExpandedId] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm]   = useState({ title: '', transcript: '' });
  const [deleteTarget, setDeleteTarget] = useState(null);
  const [saving, setSaving]       = useState(false);

  // Debounce search
  useEffect(() => {
    const t = setTimeout(() => {
      setDebouncedSearch(search);
      setPage(1);
    }, 350);
    return () => clearTimeout(t);
  }, [search]);

  // Fetch transcriptions
  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const result = await transcriptionsApi.list({
        search: debouncedSearch,
        page,
        page_size: PAGE_SIZE,
      });
      setData(result);
    } catch (err) {
      setError(`Failed to load transcriptions: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }, [debouncedSearch, page, refreshKey]);

  useEffect(() => { fetchData(); }, [fetchData]);

  // ── Edit ──────────────────────────────────────────────────────────────
  const startEdit = (item) => {
    setEditingId(item.id);
    setEditForm({ title: item.title, transcript: item.transcript });
  };

  const cancelEdit = () => { setEditingId(null); };

  const submitEdit = async (id) => {
    setSaving(true);
    try {
      await transcriptionsApi.update(id, editForm);
      setEditingId(null);
      toast.success('Transcription updated.');
      fetchData();
    } catch (err) {
      toast.error(`Update failed: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  // ── Delete ────────────────────────────────────────────────────────────
  const confirmDelete = async () => {
    if (!deleteTarget) return;
    try {
      await transcriptionsApi.delete(deleteTarget.id);
      setDeleteTarget(null);
      if (expandedId === deleteTarget.id) setExpandedId(null);
      toast.success('Transcription deleted.');
      fetchData();
    } catch (err) {
      toast.error(`Delete failed: ${err.message}`);
    }
  };

  // ── Copy ──────────────────────────────────────────────────────────────
  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      toast.success('Copied to clipboard!');
    } catch {
      toast.error('Could not copy to clipboard.');
    }
  };

  // ── Render ────────────────────────────────────────────────────────────
  return (
    <div className="history-section">
      <h1 className="page-title">Transcription History</h1>

      {/* Search */}
      <div className="search-row">
        <div className="search-input-wrapper">
          <span className="search-icon">🔍</span>
          <input
            id="history-search-input"
            type="search"
            className="search-input"
            placeholder="Search by title or transcript content…"
            value={search}
            onChange={e => setSearch(e.target.value)}
            aria-label="Search transcriptions"
          />
        </div>
        {debouncedSearch && (
          <button
            className="btn btn-ghost btn-sm"
            onClick={() => setSearch('')}
          >
            Clear
          </button>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="alert alert-error" role="alert">{error}</div>
      )}

      {/* Loading */}
      {loading && (
        <div className="loading-row">
          <div className="spinner" />
          <span>Loading transcriptions…</span>
        </div>
      )}

      {/* Results */}
      {!loading && data && (
        <>
          {data.total === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">{debouncedSearch ? '🔍' : '🎙'}</div>
              <div className="empty-title">
                {debouncedSearch
                  ? `No results for "${debouncedSearch}"`
                  : 'No transcriptions yet'}
              </div>
              <div className="empty-hint">
                {debouncedSearch
                  ? 'Try a different search term.'
                  : 'Go to the Recorder tab, record some speech, and save it here.'}
              </div>
            </div>
          ) : (
            <>
              <div className="text-sm text-muted">
                {data.total} transcription{data.total !== 1 ? 's' : ''}
                {debouncedSearch && ` matching "${debouncedSearch}"`}
              </div>

              <div className="transcription-list" role="list">
                {data.items.map(item => (
                  <TranscriptionCard
                    key={item.id}
                    item={item}
                    isExpanded={expandedId === item.id}
                    isEditing={editingId === item.id}
                    editForm={editForm}
                    saving={saving}
                    onToggleExpand={() =>
                      setExpandedId(expandedId === item.id ? null : item.id)
                    }
                    onStartEdit={() => startEdit(item)}
                    onCancelEdit={cancelEdit}
                    onEditFormChange={setEditForm}
                    onSubmitEdit={() => submitEdit(item.id)}
                    onDelete={() => setDeleteTarget(item)}
                    onCopy={() => copyToClipboard(item.transcript)}
                  />
                ))}
              </div>

              {/* Pagination */}
              {(data.has_prev || data.has_next) && (
                <div className="pagination">
                  <button
                    id="pagination-prev-btn"
                    className="btn btn-secondary btn-sm"
                    onClick={() => setPage(p => p - 1)}
                    disabled={!data.has_prev}
                  >
                    ← Prev
                  </button>
                  <span className="page-info">
                    Page {data.page} of {Math.ceil(data.total / PAGE_SIZE)}
                  </span>
                  <button
                    id="pagination-next-btn"
                    className="btn btn-secondary btn-sm"
                    onClick={() => setPage(p => p + 1)}
                    disabled={!data.has_next}
                  >
                    Next →
                  </button>
                </div>
              )}
            </>
          )}
        </>
      )}

      {/* Delete confirmation */}
      {deleteTarget && (
        <ConfirmDialog
          title="Delete Transcription"
          message={`Are you sure you want to delete "${deleteTarget.title}"? This cannot be undone.`}
          onConfirm={confirmDelete}
          onCancel={() => setDeleteTarget(null)}
          confirmLabel="Delete"
          danger
        />
      )}
    </div>
  );
}

// ── TranscriptionCard ─────────────────────────────────────────────────────────

function TranscriptionCard({
  item,
  isExpanded,
  isEditing,
  editForm,
  saving,
  onToggleExpand,
  onStartEdit,
  onCancelEdit,
  onEditFormChange,
  onSubmitEdit,
  onDelete,
  onCopy,
}) {
  return (
    <div
      className={`transcription-card ${isExpanded ? 'expanded' : ''}`}
      role="listitem"
    >
      {/* Card header — always visible */}
      <div className="card-header" onClick={onToggleExpand} style={{ cursor: 'pointer' }}>
        <div>
          <div className="card-title">{item.title}</div>
          {!isExpanded && (
            <div className="card-preview">
              {item.transcript || <em style={{ color: 'var(--clr-text-3)' }}>No transcript</em>}
            </div>
          )}
        </div>
        <div className="card-meta">
          {item.language && (
            <span className="meta-badge">🌐 {item.language.toUpperCase()}</span>
          )}
          {item.duration_seconds > 0 && (
            <span className="meta-badge">⏱ {item.duration_seconds.toFixed(1)}s</span>
          )}
          <span className="card-timestamp">{formatDate(item.created_at)}</span>
          <span style={{ color: 'var(--clr-text-3)', fontSize: '0.8rem' }}>
            {isExpanded ? '▲' : '▼'}
          </span>
        </div>
      </div>

      {/* Expanded content */}
      {isExpanded && (
        <div className="card-expanded-content">
          {isEditing ? (
            /* Edit form */
            <div className="edit-form">
              <div className="form-group">
                <label htmlFor={`edit-title-${item.id}`} className="form-label">Title</label>
                <input
                  id={`edit-title-${item.id}`}
                  type="text"
                  className="form-input"
                  value={editForm.title}
                  onChange={e => onEditFormChange(f => ({ ...f, title: e.target.value }))}
                  maxLength={255}
                />
              </div>
              <div className="form-group">
                <label htmlFor={`edit-transcript-${item.id}`} className="form-label">Transcript</label>
                <textarea
                  id={`edit-transcript-${item.id}`}
                  className="form-textarea"
                  value={editForm.transcript}
                  onChange={e => onEditFormChange(f => ({ ...f, transcript: e.target.value }))}
                  rows={6}
                />
              </div>
              <div className="card-actions">
                <button
                  id={`save-edit-${item.id}`}
                  className="btn btn-primary btn-sm"
                  onClick={onSubmitEdit}
                  disabled={saving}
                >
                  {saving ? <><div className="spinner spinner-sm" /> Saving…</> : '✓ Save changes'}
                </button>
                <button className="btn btn-ghost btn-sm" onClick={onCancelEdit}>Cancel</button>
              </div>
            </div>
          ) : (
            /* View mode */
            <>
              <div className="card-full-transcript">
                {item.transcript || <em style={{ color: 'var(--clr-text-3)' }}>No transcript text</em>}
              </div>
              <div className="card-actions">
                <button
                  id={`edit-btn-${item.id}`}
                  className="btn btn-secondary btn-sm"
                  onClick={onStartEdit}
                >
                  ✏️ Edit
                </button>
                <button
                  id={`copy-btn-${item.id}`}
                  className="btn btn-secondary btn-sm"
                  onClick={onCopy}
                >
                  📋 Copy
                </button>
                <button
                  id={`delete-btn-${item.id}`}
                  className="btn btn-danger btn-sm"
                  onClick={onDelete}
                >
                  🗑 Delete
                </button>
              </div>
            </>
          )}

          {/* Footer metadata */}
          <div style={{ display: 'flex', gap: 'var(--sp-sm)', marginTop: 'var(--sp-sm)', flexWrap: 'wrap' }}>
            <span className="meta-badge">🤖 {item.provider}</span>
            <span className="meta-badge">Created: {formatDate(item.created_at)}</span>
            {item.updated_at !== item.created_at && (
              <span className="meta-badge">Updated: {formatDate(item.updated_at)}</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function formatDate(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}
