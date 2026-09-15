# Storage, State, and Audio Module
js_state_storage_code = """
const STORAGE_KEY = 'studypulse_appData_v1';

let appState = {
  activeProfileId: 'profile-1',
  profiles: [
    { id: 'profile-1', name: 'Nivesh', avatar: 'N', created: '2026-08-01' },
    { id: 'profile-2', name: 'Study Focus', avatar: 'S', created: '2026-08-01' },
    { id: 'profile-3', name: 'Personal Growth', avatar: 'P', created: '2026-08-01' },
    { id: 'profile-4', name: 'Exam Prep', avatar: 'E', created: '2026-08-01' }
  ],
  profileData: {}
};

let currentData = null;
let undoAction = null;
let saveDebounceTimer = null;

// Initialize Storage
function initStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && parsed.activeProfileId && parsed.profiles && parsed.profileData) {
        appState = parsed;
      } else {
        seedInitialStorage();
      }
    } else {
      seedInitialStorage();
    }
  } catch (err) {
    console.warn('Storage read error, seeding default:', err);
    seedInitialStorage();
  }

  // Ensure active profile data exists
  if (!appState.profileData[appState.activeProfileId]) {
    appState.profileData[appState.activeProfileId] = getInitialDemoData();
  }
  currentData = appState.profileData[appState.activeProfileId];
  if (!currentData.documents) {
    currentData.documents = getInitialDemoData().documents || [];
  }
  applyThemeAndPreferences();
}

function seedInitialStorage() {
  appState.profileData = {
    'profile-1': getInitialDemoData()
  };
  saveStorageImmediate();
}

function saveStorage() {
  showSaveIndicator();
  clearTimeout(saveDebounceTimer);
  saveDebounceTimer = setTimeout(() => {
    saveStorageImmediate();
  }, 300);
}

function saveStorageImmediate() {
  try {
    appState.profileData[appState.activeProfileId] = currentData;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(appState));
  } catch (e) {
    console.error('Failed to save to localStorage:', e);
    showToast('LocalStorage save failed! Check storage quota.', null, 'danger');
  }
}

function showSaveIndicator() {
  const el = document.getElementById('save-indicator');
  if (el) {
    el.style.display = 'inline-flex';
    clearTimeout(el.fadeTimer);
    el.fadeTimer = setTimeout(() => {
      el.style.display = 'none';
    }, 1500);
  }
}

// Activity Logging
function logActivity(text) {
  if (!currentData.activityLog) currentData.activityLog = [];
  const entry = {
    id: 'act-' + Date.now() + '-' + Math.random().toString(36).substr(2, 4),
    text: text,
    time: new Date().toISOString()
  };
  currentData.activityLog.unshift(entry);
  if (currentData.activityLog.length > 50) currentData.activityLog.pop();
  saveStorage();
  renderActivityLog();
}

// Toast System with Undo
function showToast(message, onUndo = null, type = 'normal') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  if (type === 'danger') toast.style.background = '#dc2626';
  if (type === 'success') toast.style.background = '#059669';

  let html = `<span>${escapeHtml(message)}</span>`;
  if (onUndo) {
    html += `<button class="toast-undo-btn" id="toast-undo-btn">Undo</button>`;
  }
  toast.innerHTML = html;
  container.appendChild(toast);

  if (onUndo) {
    const btn = toast.querySelector('#toast-undo-btn');
    if (btn) {
      btn.onclick = () => {
        onUndo();
        toast.remove();
      };
    }
  }

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, onUndo ? 6000 : 3500);
}

// Web Audio API Chime for Study Timer
function playTimerChime() {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    const ctx = new AudioContext();
    const now = ctx.currentTime;

    // Pleasant two-tone chime
    const osc1 = ctx.createOscillator();
    const gain1 = ctx.createGain();
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(587.33, now); // D5
    gain1.gain.setValueAtTime(0.25, now);
    gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
    osc1.connect(gain1);
    gain1.connect(ctx.destination);
    osc1.start(now);
    osc1.stop(now + 0.5);

    const osc2 = ctx.createOscillator();
    const gain2 = ctx.createGain();
    osc2.type = 'sine';
    osc2.frequency.setValueAtTime(880, now + 0.25); // A5
    gain2.gain.setValueAtTime(0.25, now + 0.25);
    gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.85);
    osc2.connect(gain2);
    gain2.connect(ctx.destination);
    osc2.start(now + 0.25);
    osc2.stop(now + 0.85);
  } catch (e) {
    console.log('Audio playback prevented or unsupported:', e);
  }
}

// Utility escape HTML
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
"""
