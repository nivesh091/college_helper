# Styles module for StudyPulse
css_code = """
:root {
  --font-main: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  
  /* Light theme default */
  --bg-app: #f8fafc;
  --bg-sidebar: #ffffff;
  --bg-card: #ffffff;
  --bg-input: #f1f5f9;
  --bg-hover: #f1f5f9;
  --border: #e2e8f0;
  --border-subtle: #f8fafc;
  
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --text-inverse: #ffffff;

  --accent: #4f46e5;
  --accent-hover: #4338ca;
  --accent-light: #eef2ff;
  --accent-text: #4f46e5;

  --success: #10b981;
  --success-light: #ecfdf5;
  --warning: #f59e0b;
  --warning-light: #fffbeb;
  --danger: #ef4444;
  --danger-light: #fef2f2;
  --info: #0284c7;
  --info-light: #f0f9ff;

  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-xl: 20px;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.06);

  --header-height: 64px;
  --sidebar-width: 250px;
}

[data-theme="dark"] {
  --bg-app: #090d16;
  --bg-sidebar: #0f172a;
  --bg-card: #131d31;
  --bg-input: #1e293b;
  --bg-hover: #1e293b;
  --border: #1e293b;
  --border-subtle: #172236;
  
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --text-inverse: #0f172a;

  --accent: #6366f1;
  --accent-hover: #818cf8;
  --accent-light: rgba(99, 102, 241, 0.15);
  --accent-text: #a5b4fc;

  --success: #10b981;
  --success-light: rgba(16, 185, 129, 0.15);
  --warning: #f59e0b;
  --warning-light: rgba(245, 158, 11, 0.15);
  --danger: #ef4444;
  --danger-light: rgba(239, 68, 68, 0.15);
  --info: #38bdf8;
  --info-light: rgba(56, 189, 248, 0.15);

  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.6);
}

/* Dynamic Accent Colors */
[data-accent="emerald"] { --accent: #059669; --accent-hover: #047857; --accent-light: #ecfdf5; --accent-text: #059669; }
[data-accent="violet"] { --accent: #7c3aed; --accent-hover: #6d28d9; --accent-light: #f5f3ff; --accent-text: #7c3aed; }
[data-accent="rose"] { --accent: #e11d48; --accent-hover: #be123c; --accent-light: #fff1f2; --accent-text: #e11d48; }
[data-accent="amber"] { --accent: #d97706; --accent-hover: #b45309; --accent-light: #fffbeb; --accent-text: #d97706; }
[data-accent="sky"] { --accent: #0284c7; --accent-hover: #0369a1; --accent-light: #f0f9ff; --accent-text: #0284c7; }

/* Card styles */
[data-card-style="minimal"] .card { box-shadow: none; border: 1px solid var(--border); }
[data-card-style="elevated"] .card { border: none; box-shadow: var(--shadow-lg); }

/* Density */
[data-density="compact"] {
  --radius-md: 6px;
  --radius-lg: 8px;
}
[data-density="compact"] .card { padding: 12px; }
[data-density="compact"] .form-control { padding: 6px 10px; font-size: 13px; }
[data-density="compact"] .btn { padding: 6px 12px; font-size: 12px; }

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  -webkit-tap-highlight-color: transparent;
}

body {
  font-family: var(--font-main);
  background-color: var(--bg-app);
  color: var(--text-primary);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow-x: clip;
  line-height: 1.5;
  font-size: 14px;
}

/* Scrollbars */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* Utility Classes */
.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.justify-center { justify-content: center; }
.gap-1 { gap: 4px; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.gap-4 { gap: 16px; }
.w-full { width: 100%; }
.text-muted { color: var(--text-muted); }
.text-sm { font-size: 12px; }
.text-xs { font-size: 11px; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }
.truncate { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
  background: var(--bg-card);
  color: var(--text-primary);
  line-height: 1.2;
}
.btn:hover { background: var(--bg-hover); }
.btn:active { transform: scale(0.98); }
.btn-primary {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #9333ea 100%);
  color: #ffffff;
  border-color: transparent;
  box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35);
  font-weight: 600;
}
.btn-primary:hover {
  background: linear-gradient(135deg, #4338ca 0%, #6d28d9 50%, #7e22ce 100%);
  color: #ffffff;
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.45);
  transform: translateY(-1px);
}
.btn-secondary {
  background: var(--bg-card);
  border-color: rgba(148, 163, 184, 0.35);
  color: var(--text-secondary);
}
.btn-secondary:hover {
  background: var(--bg-hover);
  color: var(--accent);
  border-color: rgba(99, 102, 241, 0.4);
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.1);
}
.btn-danger {
  background: linear-gradient(135deg, #ef4444 0%, #e11d48 100%);
  color: #ffffff;
  border-color: transparent;
  box-shadow: 0 3px 10px rgba(239, 68, 68, 0.3);
}
.btn-danger:hover {
  background: linear-gradient(135deg, #dc2626 0%, #be123c 100%);
  color: #ffffff;
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4);
}
.btn-sm { padding: 4px 10px; font-size: 12px; border-radius: var(--radius-sm); }
.btn-lg { padding: 10px 20px; font-size: 15px; }
.btn-icon { padding: 8px; border-radius: var(--radius-md); width: 36px; height: 36px; }

/* Forms */
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 12.5px; font-weight: 600; margin-bottom: 5px; color: var(--text-secondary); }
.form-control {
  width: 100%;
  padding: 8px 12px;
  font-size: 13.5px;
  font-family: inherit;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  color: var(--text-primary);
  outline: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.form-control:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-light);
}
textarea.form-control { resize: vertical; min-height: 75px; }
.form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; }
.checkbox-label { display: inline-flex; align-items: center; gap: 8px; cursor: pointer; font-size: 13px; user-select: none; }
.checkbox-label input[type="checkbox"] { width: 16px; height: 16px; accent-color: var(--accent); cursor: pointer; }

/* Badges */
.badge {
  display: none !important;
}

/* Header Brand & Logo */
.header-brand {
  display: none !important;
}

/* Progress bar */
.progress-bar-wrap,
#view-dashboard .progress-bar-wrap,
.dashboard-grid .progress-bar-wrap {
  display: none !important;
}
.progress-bar-fill {
  height: 100%;
  background: var(--accent);
  border-radius: 999px;
  transition: width 0.3s ease;
}

/* App Header */
#app-header {
  height: var(--header-height);
  background: var(--bg-sidebar);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  z-index: 50;
  box-shadow: 0 4px 20px -2px rgba(99, 102, 241, 0.08);
  flex-shrink: 0;
}
#app-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2.5px;
  background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 20%, #ec4899 40%, #f59e0b 60%, #10b981 80%, #06b6d4 100%);
  z-index: 60;
}

/* Header Live Clock in Logo Space (Desktop & Mobile) */
.header-logo-clock {
  display: inline-flex !important;
  align-items: center;
  gap: 10px;
  padding: 5px 12px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(168, 85, 247, 0.12) 50%, rgba(236, 72, 153, 0.08) 100%);
  border: 1px solid rgba(99, 102, 241, 0.28);
  border-radius: var(--radius-md);
  box-shadow: 0 2px 10px rgba(99, 102, 241, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.2);
  cursor: pointer;
  user-select: none;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  flex-shrink: 0;
}
.header-logo-clock:hover {
  transform: translateY(-1px);
  border-color: rgba(139, 92, 246, 0.5);
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2);
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(168, 85, 247, 0.18) 50%, rgba(236, 72, 153, 0.12) 100%);
}
.logo-clock-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 32px;
  height: 32px;
  border-radius: 9px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.35);
  flex-shrink: 0;
}
.logo-clock-dot {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 9px;
  height: 9px;
  background: #10b981;
  border-radius: 50%;
  border: 2px solid var(--bg-sidebar);
  animation: liveClockPulse 2s infinite ease-in-out;
}
@keyframes liveClockPulse {
  0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70% { transform: scale(1.15); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}
.logo-clock-content {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}
.logo-clock-time {
  font-family: var(--font-mono);
  font-size: 14.5px;
  font-weight: 800;
  letter-spacing: 0.5px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
[data-theme="dark"] .logo-clock-time {
  background: linear-gradient(135deg, #a5b4fc 0%, #d8b4fe 50%, #f9a8d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.logo-clock-date {
  font-size: 10.5px;
  font-weight: 600;
  color: var(--text-secondary);
  white-space: nowrap;
}

.header-actions { display: flex; align-items: center; gap: 10px; }

/* Profile Pill */
.profile-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 10px 4px 6px;
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: 999px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.15s ease;
  position: relative;
}
.profile-pill:hover { background: var(--bg-hover); border-color: var(--accent); }
.profile-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
}

/* Save status indicator */
#save-indicator {
  display: none;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--success);
  background: var(--success-light);
  padding: 4px 10px;
  border-radius: 999px;
  font-weight: 500;
  transition: opacity 0.3s;
}

/* Search Bar trigger */
.search-trigger-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: var(--radius-md);
  background: var(--bg-input);
  border: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 13px;
  cursor: pointer;
}
.search-trigger-btn:hover { border-color: var(--accent); color: var(--text-primary); }
.search-shortcut {
  font-size: 11px;
  padding: 1px 5px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--text-secondary);
}

/* Layout App Shell */
#app-shell { display: flex; flex: 1; position: relative; }

/* Sidebar */
#sidebar {
  width: var(--sidebar-width);
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: var(--header-height);
  height: calc(100vh - var(--header-height));
  z-index: 30;
  transition: transform 0.25s ease;
  overflow-y: auto;
}
.sidebar-nav { padding: 12px; display: flex; flex-direction: column; gap: 4px; flex: 1; }
.nav-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}
.nav-link:hover {
  background: rgba(99, 102, 241, 0.08);
  color: var(--accent);
  transform: translateX(3px);
}
.nav-link.active {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.16) 0%, rgba(168, 85, 247, 0.14) 100%) !important;
  color: #4f46e5 !important;
  font-weight: 700 !important;
  border-left: 3.5px solid #6366f1 !important;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.12) !important;
}
[data-theme="dark"] .nav-link.active {
  color: #a5b4fc !important;
  border-left-color: #818cf8 !important;
}
.nav-link[data-view="dashboard"] .icon-slot { color: #6366f1; }
.nav-link[data-view="planner"] .icon-slot { color: #8b5cf6; }
.nav-link[data-view="timetable"] .icon-slot { color: #0284c7; }
.nav-link[data-view="subjects"] .icon-slot { color: #a855f7; }
.nav-link[data-view="chapters"] .icon-slot { color: #ec4899; }
.nav-link[data-view="goals"] .icon-slot { color: #f59e0b; }
.nav-link[data-view="todos"] .icon-slot { color: #10b981; }
.nav-link[data-view="habits"] .icon-slot { color: #f97316; }
.nav-link[data-view="playlists"] .icon-slot { color: #e11d48; }
.nav-link[data-view="notes"] .icon-slot { color: #059669; }
.nav-link[data-view="timer"] .icon-slot { color: #06b6d4; }
.nav-link[data-view="statistics"] .icon-slot { color: #7c3aed; }
.nav-link[data-view="settings"] .icon-slot { color: #64748b; }
.nav-link-content { display: flex; align-items: center; gap: 10px; }
.nav-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 1px 7px;
  border-radius: 999px;
  background: var(--bg-input);
  color: var(--text-secondary);
}
.nav-link.active .nav-badge {
  background: var(--accent);
  color: #fff;
}
.sidebar-divider {
  height: 1px;
  background: var(--border);
  margin: 8px 0;
}
.sidebar-section-title {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  color: var(--text-muted);
  padding: 4px 12px;
}
.sidebar-footer {
  padding: 12px;
  border-top: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Main Content */
#main-content {
  flex: 1;
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  min-height: calc(100vh - var(--header-height));
}

/* Views */
.view-container { display: none; }
.view-container.active { display: block; animation: fadeIn 0.15s ease; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(3px); }
  to { opacity: 1; transform: translateY(0); }
}

.view-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22px;
  flex-wrap: wrap;
  gap: 12px;
}
.view-title-group h1 { font-size: 22px; font-weight: 700; color: var(--text-primary); }
.view-title-group p { font-size: 13px; color: var(--text-muted); margin-top: 2px; }
.view-actions { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }

/* Cards */
.card {
  background: var(--bg-card);
  border: 1px solid rgba(226, 232, 240, 0.85);
  border-radius: var(--radius-lg);
  padding: 18px;
  box-shadow: 0 4px 16px -2px rgba(99, 102, 241, 0.06), 0 2px 6px -1px rgba(0, 0, 0, 0.03);
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, border-color 0.2s ease;
}
[data-theme="dark"] .card {
  border-color: rgba(30, 41, 59, 0.9);
  box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.4);
}
.card:hover {
  border-color: rgba(99, 102, 241, 0.3);
  box-shadow: 0 10px 25px -4px rgba(99, 102, 241, 0.12), 0 4px 10px -2px rgba(0, 0, 0, 0.04);
  transform: translateY(-2px);
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}
.card-title {
  font-size: 15px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-primary);
}
.card-title .icon-slot {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.12) 100%);
  color: #6366f1;
  padding: 5px;
  flex-shrink: 0;
}
.card-actions { display: flex; align-items: center; gap: 6px; }

/* Dashboard Widgets Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 18px;
}
.col-12 { grid-column: span 12; }
.col-8 { grid-column: span 8; }
.col-6 { grid-column: span 6; }
.col-4 { grid-column: span 4; }

/* Stat Summary Row (Hidden as per requirement) */
.stat-summary-row {
  display: none !important;
}

/* Today's Classes Attendance Action Styles */
.class-attendance-row {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  background: var(--bg-input);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  margin-bottom: 8px;
  transition: all 0.2s ease;
}
.class-attendance-row:hover {
  background: var(--bg-hover);
}
.class-menu-container {
  position: relative;
}
.class-menu-trigger {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  background: transparent;
  border: 1px solid transparent;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s ease;
}
.class-menu-trigger:hover {
  background: var(--bg-card);
  border-color: var(--border);
  color: var(--text-primary);
}
.class-menu-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 4px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: 0 10px 25px rgba(0,0,0,0.3);
  z-index: 100;
  min-width: 170px;
  padding: 6px;
  display: none;
  flex-direction: column;
  gap: 2px;
}
.class-menu-dropdown.active {
  display: flex;
}
.class-menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 7px 10px;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 12.5px;
  font-weight: 500;
  border-radius: var(--radius-sm);
  cursor: pointer;
  text-align: left;
  transition: background 0.15s ease;
}
.class-menu-item:hover {
  background: var(--bg-hover);
}
.class-menu-item.danger {
  color: var(--danger);
}
.class-menu-item.warning {
  color: var(--warning);
}
.class-menu-item.success {
  color: var(--success);
}
.class-attendance-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  font-size: 11px;
  font-weight: 700;
  border-radius: 999px;
}
.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.stat-icon-wrap {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}
.stat-value { font-size: 20px; font-weight: 700; color: var(--text-primary); line-height: 1.1; }
.stat-label { font-size: 12px; color: var(--text-muted); font-weight: 500; }

/* Timetable styling */
.timetable-wrapper {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}
.timetable-toolbar {
  padding: 12px 16px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
}
.timetable-scroll-container {
  overflow-x: auto;
  max-width: 100%;
}
.timetable-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  min-width: 800px;
}
.timetable-table th, .timetable-table td {
  border-right: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  padding: 8px;
}
.timetable-table th:last-child, .timetable-table td:last-child {
  border-right: none;
}
.timetable-table tr:last-child td {
  border-bottom: none;
}
.timetable-header-day {
  background: var(--bg-input);
  font-weight: 600;
  font-size: 13px;
  color: var(--text-primary);
  text-align: center;
  position: sticky;
  top: 0;
  z-index: 10;
  height: 40px;
}
.timetable-time-slot {
  background: var(--bg-input);
  font-family: var(--font-mono);
  font-size: 11.5px;
  font-weight: 600;
  color: var(--text-secondary);
  text-align: center;
  width: 130px;
  min-width: 130px;
  position: sticky;
  left: 0;
  z-index: 11;
}
.timetable-cell {
  background: var(--bg-card);
  height: 90px;
  vertical-align: top;
  position: relative;
  transition: background 0.15s;
  min-width: 125px;
}
.timetable-cell:hover { background: var(--bg-hover); }
.timetable-cell.drag-over { background: var(--accent-light); border: 2px dashed var(--accent); }

.timetable-class-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: var(--radius-sm);
  padding: 6px 8px;
  box-shadow: var(--shadow-sm);
  cursor: grab;
  user-select: none;
  display: flex;
  flex-direction: column;
  gap: 3px;
  position: relative;
  transition: transform 0.1s ease, box-shadow 0.1s ease;
  margin-bottom: 4px;
}
.timetable-class-card:hover { transform: translateY(-1px); box-shadow: var(--shadow-md); }
.timetable-class-card.dragging { opacity: 0.4; }
.class-subject-name { font-weight: 600; font-size: 12px; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.class-teacher-name { font-size: 11px; color: var(--text-muted); }
.class-room-badge { font-size: 10px; background: var(--bg-input); padding: 1px 4px; border-radius: 3px; align-self: flex-start; }

/* Sticky Notes */
.stickies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 16px;
}
.sticky-note-card {
  border-radius: var(--radius-md);
  padding: 16px;
  min-height: 170px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: var(--shadow-md);
  position: relative;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.sticky-note-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.sticky-yellow { background: #fef08a; color: #713f12; border: 1px solid #fde047; }
.sticky-cyan { background: #bae6fd; color: #075985; border: 1px solid #7dd3fc; }
.sticky-lime { background: #d9f99d; color: #365314; border: 1px solid #bef264; }
.sticky-coral { background: #fecdd3; color: #9f1239; border: 1px solid #fda4af; }
.sticky-lavender { background: #e9d5ff; color: #581c87; border: 1px solid #d8b4fe; }
.sticky-peach { background: #fed7aa; color: #7c2d12; border: 1px solid #fdba74; }

.sticky-pin-icon { position: absolute; top: 8px; right: 8px; opacity: 0.7; }
.sticky-title { font-weight: 700; font-size: 13.5px; margin-bottom: 5px; }
.sticky-content { font-size: 12.5px; white-space: pre-wrap; word-break: break-word; flex: 1; }
.sticky-footer { display: flex; align-items: center; justify-content: space-between; font-size: 11px; margin-top: 8px; opacity: 0.85; }

/* Calendar */
.calendar-wrapper { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 16px; }
.calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; }
.cal-day-header { text-align: center; font-weight: 600; font-size: 12px; color: var(--text-muted); padding: 8px 0; }
.cal-day-cell {
  min-height: 80px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 5px;
  background: var(--bg-card);
  cursor: pointer;
  transition: all 0.15s ease;
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.cal-day-cell:hover { background: var(--bg-hover); border-color: var(--accent); }
.cal-day-cell.other-month { opacity: 0.35; background: var(--bg-input); }
.cal-day-cell.today { border-color: var(--accent); background: var(--accent-light); }
.cal-date-num { font-size: 12px; font-weight: 600; margin-bottom: 2px; }
.cal-day-cell.today .cal-date-num { color: var(--accent); font-weight: 700; }
.cal-event-pill { font-size: 10px; padding: 2px 4px; border-radius: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500; }

/* Focus Mode */
#focus-mode-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: #090d16;
  color: #f8fafc;
  z-index: 100;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
#focus-mode-overlay.active { display: flex; animation: fadeIn 0.25s ease; }
.focus-timer-display { font-family: var(--font-mono); font-size: 72px; font-weight: 700; letter-spacing: 2px; margin: 16px 0; }
.focus-card { background: #131d31; border: 1px solid #1e293b; border-radius: var(--radius-xl); padding: 28px; max-width: 550px; width: 100%; text-align: center; box-shadow: var(--shadow-xl); }

/* Modals */
.modal-backdrop {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 60;
  align-items: center;
  justify-content: center;
  padding: 16px;
}
.modal-backdrop.active { display: flex; animation: fadeIn 0.2s ease; }
.modal-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  max-width: 620px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-xl);
  overflow: hidden;
}
.modal-header {
  padding: 14px 18px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.modal-title { font-size: 16px; font-weight: 700; color: var(--text-primary); }
.modal-body {
  padding: 18px;
  overflow-y: auto;
  flex: 1;
}
.modal-footer {
  padding: 12px 18px;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  background: var(--bg-card);
}

/* Toast Notification */
#toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 90;
}
.toast {
  background: var(--text-primary);
  color: var(--text-inverse);
  padding: 10px 16px;
  border-radius: var(--radius-md);
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: var(--shadow-lg);
  animation: slideInUp 0.2s ease;
}
@keyframes slideInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.toast-undo-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: #fff;
  padding: 2px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  font-size: 11px;
}

/* Offline Status Indicator */
.offline-toast {
  position: fixed;
  bottom: 24px;
  left: 24px;
  background: #b45309;
  color: #ffffff;
  padding: 8px 14px;
  border-radius: var(--radius-md);
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 95;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
  animation: slideInUp 0.2s ease;
}
.offline-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ffffff;
  display: inline-block;
}
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}
.animate-pulse {
  animation: pulse 1.5s infinite;
}

/* Topbar Subjects Quick Access Pill */
.topbar-subjects-pill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 6px 12px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 9999px;
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.topbar-subjects-pill:hover {
  border-color: var(--accent);
  background: var(--bg-input);
  box-shadow: var(--shadow-sm);
}
.topbar-subjects-pill .badge-count {
  background: var(--accent);
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  padding: 1px 7px;
  border-radius: 9999px;
  min-width: 18px;
  text-align: center;
  line-height: 1.4;
}

/* Left Three Dots Button & Dropdown */
.left-dots-btn {
  position: relative;
}
.left-dots-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  width: 290px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
  animation: dropdownFadeIn 0.15s ease-out;
}
@keyframes dropdownFadeIn {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}
.left-dots-menu-header {
  padding: 10px 14px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  background: var(--bg-input);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.left-dots-close-btn {
  background: none;
  border: none;
  font-size: 18px;
  color: var(--text-muted);
  cursor: pointer;
  line-height: 1;
}
.left-dots-menu-body {
  padding: 6px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.left-dots-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  border-radius: var(--radius-sm);
  border: none;
  background: transparent;
  color: var(--text-primary);
  text-align: left;
  cursor: pointer;
  width: 100%;
  transition: background 0.15s ease;
}
.left-dots-item:hover {
  background: var(--bg-input);
}
.left-dots-item.primary-action {
  background: rgba(79, 70, 229, 0.08);
}
.left-dots-item.primary-action:hover {
  background: rgba(79, 70, 229, 0.15);
}
.left-dots-item .item-icon-wrap {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  background: var(--bg-input);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  flex-shrink: 0;
}
.left-dots-item .item-icon-wrap.upload-accent {
  background: var(--accent);
  color: #ffffff;
}
.left-dots-item .item-text-group {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.left-dots-item .item-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
}
.left-dots-item .item-subtitle {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}
.left-dots-divider {
  height: 1px;
  background: var(--border);
  margin: 4px 6px;
}

/* File Dropzone & Document Library */
.file-dropzone {
  border: 2px dashed var(--border);
  border-radius: var(--radius-md);
  padding: 24px 16px;
  text-align: center;
  cursor: pointer;
  background: var(--bg-input);
  transition: all 0.2s ease;
}
.file-dropzone:hover, .file-dropzone.dragover {
  border-color: var(--accent);
  background: rgba(79, 70, 229, 0.05);
}
.dropzone-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--bg-card);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 10px;
  color: var(--accent);
  box-shadow: var(--shadow-sm);
}
.dropzone-text {
  font-size: 13.5px;
  color: var(--text-primary);
}
.dropzone-text strong {
  color: var(--accent);
}
.doc-item-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  gap: 12px;
  transition: all 0.15s ease;
}
.doc-item-card:hover {
  border-color: var(--accent);
  box-shadow: var(--shadow-sm);
}
.doc-item-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: rgba(79, 70, 229, 0.1);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* Mobile Nav */
#mobile-bottom-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: var(--bg-card);
  border-top: 1px solid var(--border);
  z-index: 50;
  align-items: center;
  justify-content: space-around;
  padding: 0 4px;
  padding-bottom: env(safe-area-inset-bottom, 0px);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.06);
}
.mobile-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 10.5px;
  font-weight: 500;
  padding: 4px 6px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  flex: 1;
  min-height: 48px;
}
.mobile-nav-item.active { color: var(--accent); font-weight: 700; }

/* =========================================================================
   PROFESSIONAL MOBILE & RESPONSIVE MEDIA QUERIES
   ========================================================================= */

@media (max-width: 1024px) {
  .col-8, .col-6, .col-4, .col-3 { grid-column: span 12; }
  #sidebar {
    position: fixed;
    top: var(--header-height);
    left: 0;
    bottom: 0;
    width: 270px;
    z-index: 60;
    transform: translateX(-100%);
    box-shadow: var(--shadow-xl);
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }
  #sidebar.mobile-open { transform: translateX(0); }
  #mobile-menu-btn { display: inline-flex !important; }
  .header-actions { gap: 6px; }
}

@media (max-width: 768px) {
  :root {
    --header-height: 56px;
  }
  
  /* Topbar header mobile precision & guaranteed visibility */
  #app-header {
    position: sticky !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    max-width: 100vw !important;
    height: var(--header-height) !important;
    min-height: var(--header-height) !important;
    z-index: 50 !important;
    background: var(--bg-sidebar) !important;
    border-bottom: 1px solid var(--border) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding: 0 10px !important;
    box-sizing: border-box !important;
    flex-shrink: 0 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
  }
  .header-left {
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    flex-shrink: 0 !important;
  }
  .header-center,
  .header-clock-date,
  #save-indicator,
  .header-focus-btn,
  .header-settings-btn {
    display: none !important;
  }

  /* Live Clock in Logo Area on Mobile */
  .header-logo-clock {
    display: inline-flex !important;
    align-items: center !important;
    padding: 3px 8px !important;
    gap: 6px !important;
    border-radius: 8px !important;
    flex-shrink: 0 !important;
  }
  .logo-clock-badge {
    width: 26px !important;
    height: 26px !important;
    border-radius: 6px !important;
  }
  .logo-clock-badge .icon-slot {
    width: 14px !important;
    height: 14px !important;
  }
  .logo-clock-dot {
    width: 7px !important;
    height: 7px !important;
  }
  .logo-clock-time {
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.2px !important;
  }
  .logo-clock-date {
    display: none !important;
  }

  .header-actions {
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    flex-shrink: 0 !important;
  }

  /* Compact topbar elements */
  .topbar-subjects-pill {
    display: inline-flex !important;
    align-items: center !important;
    padding: 4px 9px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    gap: 5px !important;
    border-radius: 999px !important;
    flex-shrink: 0 !important;
  }
  .topbar-subjects-pill .icon-slot[data-icon="chevron-down"] {
    display: none !important;
  }
  .profile-pill {
    display: inline-flex !important;
    align-items: center !important;
    padding: 3px 8px 3px 3px !important;
    font-size: 12px !important;
    gap: 5px !important;
    border-radius: 999px !important;
    flex-shrink: 0 !important;
  }
  .profile-pill .icon-slot[data-icon="chevron-down"] {
    display: none !important;
  }
  #header-install-btn,
  #theme-toggle-btn,
  #left-dots-btn,
  #mobile-menu-btn {
    width: 34px !important;
    height: 34px !important;
    min-width: 34px !important;
    padding: 6px !important;
    flex-shrink: 0 !important;
  }

  /* Main content padding with mobile bottom nav clearance */
  #main-content {
    padding: 12px;
    padding-bottom: calc(76px + env(safe-area-inset-bottom, 0px));
    max-width: 100vw;
    overflow-x: clip;
  }

  #mobile-bottom-nav {
    display: flex;
  }

  /* View Header */
  .view-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 14px;
  }
  .view-title-group h1 {
    font-size: 20px;
  }
  .view-title-group p {
    font-size: 12.5px;
  }
  .view-actions {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: flex-start;
  }
  .view-actions .btn {
    flex: 1 1 auto;
    justify-content: center;
    min-height: 38px;
  }

  /* Stat summary row - 2 column grid on mobile */
  .stat-summary-row {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 8px !important;
  }
  .stat-summary-card {
    padding: 10px 12px !important;
  }
  .stat-summary-val {
    font-size: 18px !important;
  }
  .stat-summary-lbl {
    font-size: 11px !important;
  }

  /* Forms & Modals - Professional Bottom Sheet pattern */
  .form-row {
    grid-template-columns: 1fr !important;
    gap: 8px !important;
  }
  .modal-backdrop {
    padding: 0;
    align-items: flex-end;
  }
  .modal-box {
    width: 100% !important;
    max-width: 100% !important;
    max-height: 92vh !important;
    border-radius: 18px 18px 0 0 !important;
    margin: 0 !important;
    border-bottom: none !important;
    box-shadow: 0 -8px 30px rgba(0, 0, 0, 0.25) !important;
    animation: modalSlideUp 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
  }
  @keyframes modalSlideUp {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
  }
  .modal-header {
    padding: 14px 16px;
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    background: var(--bg-card);
    z-index: 10;
  }
  .modal-body {
    padding: 14px 16px;
    max-height: calc(92vh - 125px);
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
  }
  .modal-footer {
    padding: 12px 16px;
    border-top: 1px solid var(--border);
    position: sticky;
    bottom: 0;
    background: var(--bg-card);
    z-index: 10;
  }

  /* Inputs font size 16px to prevent iOS auto-zoom */
  input, select, textarea {
    font-size: 16px !important;
  }

  /* Timetable Horizontal Touch Scroll with clear affordance */
  .timetable-wrap {
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch;
    border-radius: var(--radius-md);
    position: relative;
  }
  .timetable-grid {
    min-width: 640px !important;
  }

  /* Left 3-dots dropdown responsive positioning */
  .left-dots-dropdown {
    width: 270px;
    max-width: 90vw;
  }

  /* Upload Document Section Mobile Media Query */
  .file-dropzone {
    padding: 18px 12px;
    border-radius: var(--radius-md);
  }
  .dropzone-icon {
    width: 38px;
    height: 38px;
    margin-bottom: 8px;
  }
  .doc-item-card {
    padding: 10px 12px;
    gap: 10px;
  }
  .doc-item-icon {
    width: 32px;
    height: 32px;
  }
  #upload-doc-form .form-row {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .documents-list {
    max-height: calc(85vh - 180px) !important;
  }
}

@media (max-width: 480px) {
  #app-header {
    padding: 0 6px !important;
  }
  .header-left {
    gap: 4px !important;
  }
  .header-logo-clock {
    display: inline-flex !important;
    padding: 2px 6px !important;
    gap: 4px !important;
  }
  .logo-clock-badge {
    width: 22px !important;
    height: 22px !important;
    border-radius: 5px !important;
  }
  .logo-clock-badge .icon-slot {
    width: 12px !important;
    height: 12px !important;
  }
  .logo-clock-time {
    font-size: 11px !important;
  }
  .header-brand .brand-title {
    display: none !important;
  }
  .header-actions {
    gap: 4px !important;
  }

  /* Topbar subjects button on mobile - keep text and count visible */
  .topbar-subjects-pill {
    display: inline-flex !important;
    align-items: center !important;
    padding: 4px 7px !important;
    font-size: 11.5px !important;
    gap: 4px !important;
    border-radius: 999px !important;
    flex-shrink: 0 !important;
  }
  .topbar-subjects-pill .topbar-subjects-text {
    display: inline !important;
    font-size: 11px !important;
    font-weight: 600 !important;
  }
  .topbar-subjects-pill .badge-count {
    padding: 1px 4px !important;
    font-size: 10px !important;
  }
  .topbar-subjects-pill .icon-slot[data-icon="chevron-down"] {
    display: none !important;
  }

  .profile-pill {
    display: inline-flex !important;
    align-items: center !important;
    padding: 3px 6px 3px 3px !important;
    font-size: 11.5px !important;
    gap: 4px !important;
    border-radius: 999px !important;
    flex-shrink: 0 !important;
  }
  .profile-avatar {
    width: 22px !important;
    height: 22px !important;
    font-size: 10.5px !important;
  }

  #header-install-btn,
  #theme-toggle-btn,
  #left-dots-btn,
  #mobile-menu-btn {
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    padding: 5px !important;
    flex-shrink: 0 !important;
  }
  .brand-logo {
    width: 28px !important;
    height: 28px !important;
    font-size: 13px !important;
    border-radius: 6px !important;
    flex-shrink: 0 !important;
  }

  /* Left dots popover width */
  .left-dots-dropdown {
    left: 0;
    width: calc(100vw - 16px);
    max-width: 310px;
  }

  /* Full width action buttons inside cards */
  .card-header {
    flex-wrap: wrap;
    gap: 8px;
  }

  /* Horizontal tab bars touch scrollable */
  .nav-pills, .filter-tabs {
    display: flex;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    white-space: nowrap;
    gap: 6px;
    padding-bottom: 4px;
  }
  .nav-pills::-webkit-scrollbar,
  .filter-tabs::-webkit-scrollbar {
    display: none;
  }

  .stat-summary-row {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 6px !important;
  }

  /* Upload Document Section Ultra-Responsive Mobile Rules */
  .file-dropzone {
    padding: 14px 10px;
    min-height: 100px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .dropzone-icon {
    width: 32px;
    height: 32px;
    margin: 0 auto 6px;
  }
  .dropzone-text {
    font-size: 12px;
    line-height: 1.4;
  }
  .doc-item-card {
    flex-direction: column;
    align-items: stretch;
    padding: 12px 10px;
    gap: 8px;
  }
  .doc-item-actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 8px;
    padding-top: 8px;
    border-top: 1px solid var(--border);
    width: 100%;
  }
  .doc-item-actions .btn {
    min-width: 38px;
    min-height: 38px;
    padding: 6px 12px;
  }
  .upload-doc-actions {
    flex-direction: column-reverse;
    width: 100%;
    gap: 8px;
  }
  .upload-doc-actions button {
    width: 100%;
    min-height: 44px;
    justify-content: center;
  }

  /* Subjects Modal Card Mobile Formatting */
  .top-subject-item-card {
    padding: 12px 12px !important;
  }
  .top-subject-item-card h4 {
    font-size: 14px !important;
  }
  .top-subject-item-card .subject-teacher-subtitle {
    font-size: 12.5px !important;
  }
}

@media (max-width: 360px) {
  .stat-summary-row {
    grid-template-columns: 1fr !important;
  }
  #current-profile-name {
    display: none;
  }
  .file-dropzone {
    padding: 10px 6px;
  }
  .filter-tabs .btn {
    padding: 4px 7px;
    font-size: 10px;
  }
  .top-subject-item-card {
    padding: 10px 10px !important;
  }
}

/* ==========================================
     DEVELOPER PROFILE CARD STYLES
     ========================================== */

/* Keyframes: Subtle Entrance Animation */
@keyframes cardAppear {
    from {
        opacity: 0;
        transform: translateY(15px) scale(0.98);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* Modern Glass & Glow Layout */
.developer-card {
    position: relative;
    z-index: 2;
    max-width: 680px;
    width: 100%;
    margin: 2.5rem auto 2rem auto;
    padding: 2.5rem 2rem;
    border-radius: 24px;

    /* Frosted Glass Background */
    background: rgb(26 60 78 / 75%);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);

    color: #cbd5e1;

    /* Glowing Border & Shadow */
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);

    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 1.25rem;
    font-family: inherit;
    box-sizing: border-box;

    /* Smooth Entrance Animation */
    animation: cardAppear 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275),
        box-shadow 0.4s ease,
        border-color 0.4s ease;
}

/* Interactive Hover Effect on Card */
.developer-card:hover {
    transform: translateY(-6px);
    border-color: rgba(99, 102, 241, 0.4);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5),
        0 0 25px rgba(99, 102, 241, 0.15);
}

/* Profile Image Wrapper (Static - No hover rotation) */
.developer-card .profile-img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    padding: 3px;
    background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
    flex-shrink: 0;
    transform: none !important;
    transition: none !important;
    display: block;
}

.developer-card .profile-img:hover {
    transform: none !important;
}

/* Headings & Gradient Typography */
.developer-card .developer-info h2 {
    margin: 0;
    font-size: 1.65rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
}

.developer-card .title {
    display: inline-block;
    margin: 0.3rem 0 1rem 0;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;

    /* Vibrant Gradient Text */
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.developer-card .intro {
    color: #a1a1aa;
    line-height: 1.6;
    font-size: 0.92rem;
    margin: 0 0 1.25rem 0;
    max-width: 540px;
}

/* Pill Badges with Soft Hover */
.developer-card .skills {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    justify-content: center;
}

.developer-card .skills span {
    background: rgba(255, 255, 255, 0.06);
    color: #cbd5e1;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.4rem 0.85rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    transition: all 0.3s ease;
}

.developer-card .skills span:hover {
    background: rgba(99, 102, 241, 0.2);
    border-color: #6366f1;
    color: #ffffff;
    transform: translateY(-2px);
}

/* Glowing Social Action Buttons */
.developer-card .social-links {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    flex-wrap: wrap;
    width: 100%;
}

.developer-card .social-links a {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 42px;
    height: 42px;
    padding: 0;
    color: #ffffff;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.85rem;
    transition: all 0.3s ease;
}

.developer-card .social-links a:hover {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    border-color: transparent;
    color: #ffffff;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.35);
    transform: translateY(-3px);
}

@media (max-width: 800px) {
  .developer-card {
    max-width: 95%;
    margin: 1.5rem auto 75px auto;
    padding: 1.75rem 1.25rem;
  }
}

/* Global Navigation Back Button */
#global-back-btn {
  display: none;
  align-items: center;
  justify-content: center;
  margin-right: 6px;
  flex-shrink: 0;
}

/* Additional Responsive Media Queries for Mobile Dashboard */
@media screen and (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr !important;
    gap: 12px !important;
  }
  .col-6, .col-8, .col-4, .col-12 {
    grid-column: span 12 !important;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }
  .class-attendance-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    padding: 10px;
  }
  .class-attendance-row > div:first-child {
    width: 100%;
  }
  .class-attendance-row > div:last-child {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .class-menu-dropdown {
    right: 0;
    left: auto;
  }
  .view-container {
    padding: 12px 10px !important;
    max-width: 100vw;
    box-sizing: border-box;
  }
  .card-header {
    flex-wrap: wrap;
    gap: 6px;
  }
}
"""
