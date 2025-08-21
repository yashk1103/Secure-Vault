import React, { useState } from 'react';
import { User } from '../App';
import { apiService } from '../services/apiService';

interface DeleteAccountProps {
  user: User;
  onAccountDeleted: () => void;
  onCancel: () => void;
}

const DeleteAccount: React.FC<DeleteAccountProps> = ({ user, onAccountDeleted, onCancel }) => {
  const [password, setPassword] = useState('');
  const [confirmText, setConfirmText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleDelete = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Validation
      if (!password) {
        setError('Please enter your password');
        return;
      }

      if (confirmText !== 'DELETE') {
        setError('Please type "DELETE" to confirm');
        return;
      }

      // Call API to delete account
      await apiService.deleteAccount(password);
      onAccountDeleted();
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete account');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.7)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        background: 'white',
        padding: '2rem',
        borderRadius: '8px',
        width: '90%',
        maxWidth: '500px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
      }}>
        <h2 style={{ color: '#e53e3e', marginBottom: '1.5rem' }}>
          Delete Account
        </h2>
        
        <div style={{
          background: '#fed7d7',
          border: '1px solid #feb2b2',
          borderRadius: '4px',
          padding: '1rem',
          marginBottom: '1.5rem'
        }}>
          <p style={{ color: '#822727', margin: 0, fontWeight: 'bold' }}>
            ⚠️ This action cannot be undone!
          </p>
          <p style={{ color: '#822727', margin: '0.5rem 0 0 0' }}>
            This will permanently delete your account and all your vault entries.
          </p>
        </div>

        <form onSubmit={handleDelete}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '0.5rem',
              fontWeight: 'bold',
              color: '#2d3748'
            }}>
              Current Password:
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #e2e8f0',
                borderRadius: '4px',
                fontSize: '1rem'
              }}
              placeholder="Enter your password"
              required
              disabled={loading}
            />
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '0.5rem',
              fontWeight: 'bold',
              color: '#2d3748'
            }}>
              Type "DELETE" to confirm:
            </label>
            <input
              type="text"
              value={confirmText}
              onChange={(e) => setConfirmText(e.target.value)}
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #e2e8f0',
                borderRadius: '4px',
                fontSize: '1rem'
              }}
              placeholder="Type DELETE"
              required
              disabled={loading}
            />
          </div>

          {error && (
            <div style={{
              background: '#fed7d7',
              border: '1px solid #feb2b2',
              borderRadius: '4px',
              padding: '0.75rem',
              marginBottom: '1rem',
              color: '#822727'
            }}>
              {error}
            </div>
          )}

          <div style={{ 
            display: 'flex', 
            gap: '1rem',
            justifyContent: 'flex-end'
          }}>
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              style={{
                padding: '0.75rem 1.5rem',
                border: '1px solid #e2e8f0',
                borderRadius: '4px',
                background: 'white',
                color: '#4a5568',
                cursor: 'pointer',
                fontSize: '1rem'
              }}
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || !password || confirmText !== 'DELETE'}
              style={{
                padding: '0.75rem 1.5rem',
                border: 'none',
                borderRadius: '4px',
                background: loading ? '#fed7d7' : '#e53e3e',
                color: 'white',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontSize: '1rem',
                opacity: loading || !password || confirmText !== 'DELETE' ? 0.6 : 1
              }}
            >
              {loading ? 'Deleting...' : 'Delete Account'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default DeleteAccount;
