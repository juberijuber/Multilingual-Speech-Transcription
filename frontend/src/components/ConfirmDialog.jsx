/**
 * ConfirmDialog.jsx — Modal confirmation before destructive actions.
 */

export default function ConfirmDialog({ title, message, onConfirm, onCancel, confirmLabel = 'Delete', danger = true }) {
  return (
    <div className="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="confirm-title">
      <div className="modal-box">
        <h2 id="confirm-title" className="modal-title">{title}</h2>
        <p className="modal-body">{message}</p>
        <div className="modal-actions">
          <button id="confirm-cancel-btn" className="btn btn-secondary" onClick={onCancel}>
            Cancel
          </button>
          <button
            id="confirm-action-btn"
            className={`btn ${danger ? 'btn-danger' : 'btn-primary'}`}
            onClick={onConfirm}
          >
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
