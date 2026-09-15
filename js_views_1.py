# Views Part 1: Navigation, Dashboard, Goals, and Todos
js_views_1_code = """
// Live Clock & Date
function startClock() {
  function update() {
    const now = new Date();
    const timeEl = document.getElementById('live-time');
    const dateEl = document.getElementById('live-date');
    if (timeEl) {
      timeEl.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }
    if (dateEl) {
      dateEl.textContent = now.toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
    }
  }
  update();
  setInterval(update, 1000);
}

// Router and Navigation with Browser-Style Back Support
let currentView = 'dashboard';
let viewHistory = ['dashboard'];

function navigateTo(viewName, pushHistory = true) {
  if (pushHistory && viewName !== currentView) {
    viewHistory.push(viewName);
    try {
      window.history.pushState({ view: viewName }, '', '#' + viewName);
    } catch(e) {}
  }
  currentView = viewName;
  window.location.hash = viewName;

  // Toggle global back button in header (browser-style step back)
  const backBtn = document.getElementById('global-back-btn');
  if (backBtn) {
    backBtn.style.display = (viewName === 'dashboard' && viewHistory.length <= 1) ? 'none' : 'inline-flex';
  }

  // Update nav links active state
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.toggle('active', link.getAttribute('data-view') === viewName);
  });
  document.querySelectorAll('.mobile-nav-item').forEach(link => {
    link.classList.toggle('active', link.getAttribute('data-view') === viewName);
  });

  // Hide all views and display active
  document.querySelectorAll('.view-container').forEach(view => {
    view.classList.remove('active');
  });
  const target = document.getElementById('view-' + viewName);
  if (target) {
    target.classList.add('active');
  }

  // Close mobile sidebar and open menus if open
  closeMobileSidebar();
  closeLeftDotsMenu();
  closeAllAttendanceMenus();

  // Trigger view renderers
  renderView(viewName);
}

function goBack() {
  const modal = document.getElementById('modal-container');
  if (modal && modal.classList.contains('active')) {
    closeModal();
    return;
  }
  closeAllAttendanceMenus();
  closeLeftDotsMenu();
  closeMobileSidebar();

  if (viewHistory.length > 1) {
    viewHistory.pop(); // discard current
    const prevView = viewHistory[viewHistory.length - 1];
    navigateTo(prevView, false);
  } else {
    navigateTo('dashboard', false);
  }
}

// Browser native back/forward event listener
window.addEventListener('popstate', (e) => {
  const modal = document.getElementById('modal-container');
  if (modal && modal.classList.contains('active')) {
    closeModal();
    return;
  }
  closeAllAttendanceMenus();
  closeLeftDotsMenu();
  closeMobileSidebar();

  if (e.state && e.state.view) {
    if (viewHistory.length > 1) viewHistory.pop();
    navigateTo(e.state.view, false);
  } else if (window.location.hash) {
    const v = window.location.hash.replace('#', '');
    navigateTo(v || 'dashboard', false);
  } else {
    navigateTo('dashboard', false);
  }
});

function renderView(viewName) {
  updateBadges();
  switch (viewName) {
    case 'dashboard':
      renderDashboard();
      break;
    case 'goals':
      renderGoals();
      break;
    case 'todos':
      renderTodos();
      break;
    case 'subjects':
      renderSubjects();
      break;
    case 'chapters':
      renderChapters();
      break;
    case 'teachers':
      renderTeachers();
      break;
    case 'timetable':
      renderTimetable();
      break;
    case 'calendar':
      renderCalendar();
      break;
    case 'planner':
      renderPlanner();
      break;
    case 'notes':
      renderNotes();
      break;
    case 'stickies':
      renderStickies();
      break;
    case 'playlists':
      renderPlaylists();
      break;
    case 'habits':
      renderHabits();
      break;
    case 'timer':
      renderTimerView();
      break;
    case 'statistics':
      renderStatistics();
      break;
    case 'settings':
      renderSettings();
      break;
  }
  renderAllIcons();
}

function updateBadges() {
  if (!currentData) return;
  const setBadge = (id, count) => {
    const el = document.getElementById(id);
    if (el) el.textContent = count;
  };
  setBadge('badge-goals', currentData.goals.filter(g => g.status !== 'Completed').length);
  setBadge('badge-todos', currentData.tasks.filter(t => !t.completed).length);
  setBadge('badge-subjects', currentData.subjects.length);
  setBadge('badge-chapters', currentData.chapters.length);
  setBadge('badge-teachers', currentData.teachers.length);
  setBadge('badge-notes', currentData.notes.length);
  setBadge('badge-stickies', currentData.stickyNotes.filter(s => !s.archived).length);
  setBadge('badge-videos', currentData.videos.length);
  setBadge('badge-habits', currentData.habits.length);
  setBadge('badge-calendar-events', currentData.calendarEvents.length);
  setBadge('badge-documents', (currentData.documents || []).length);
  setBadge('topbar-subjects-count', (currentData.subjects || []).length);

  const leftDocsLabel = document.getElementById('left-docs-count-label');
  if (leftDocsLabel) {
    const docCount = (currentData.documents || []).length;
    leftDocsLabel.textContent = `${docCount} file${docCount === 1 ? '' : 's'} uploaded`;
  }

  // Profile pill update
  const activeProfile = appState.profiles.find(p => p.id === appState.activeProfileId);
  if (activeProfile) {
    const nameEl = document.getElementById('current-profile-name');
    const avatarEl = document.getElementById('current-profile-avatar');
    const greetEl = document.getElementById('dash-greeting-name');
    if (nameEl) nameEl.textContent = activeProfile.name;
    if (avatarEl) avatarEl.textContent = activeProfile.avatar || activeProfile.name.charAt(0);
    if (greetEl) greetEl.textContent = activeProfile.name;
  }
}

function toggleMobileSidebar() {
  const sidebar = document.getElementById('sidebar');
  if (sidebar) sidebar.classList.toggle('mobile-open');
}

function closeMobileSidebar() {
  const sidebar = document.getElementById('sidebar');
  if (sidebar) sidebar.classList.remove('mobile-open');
}

/* =========================================================================
   DASHBOARD VIEW & WIDGETS
   ========================================================================= */

function renderDashboard() {
  renderDashboardStatSummary();
  renderDashboardWidgets();
}

function renderDashboardStatSummary() {
  const container = document.getElementById('dashboard-stat-summary');
  if (container) {
    container.style.display = 'none';
    container.innerHTML = '';
  }
}

function renderDashboardWidgets() {
  const container = document.getElementById('dashboard-widgets-container');
  if (!container) return;

  const prefs = currentData.settings.dashboardWidgets || {};
  const order = currentData.settings.widgetOrder || [
    'importantGoals', 'todos', 'subjects', 'currentChapters', 'timetable', 'continueLearning', 'habits', 'statistics'
  ];

  let html = '';

  order.forEach(widgetId => {
    if (prefs[widgetId] === false) return;

    switch (widgetId) {
      case 'importantGoals':
        html += getWidgetImportantGoalsHtml();
        break;
      case 'todos':
        html += getWidgetTodosHtml();
        break;
      case 'subjects':
        html += getWidgetSubjectsHtml();
        break;
      case 'currentChapters':
        html += getWidgetCurrentChaptersHtml();
        break;
      case 'timetable':
        html += getWidgetTodayTimetableHtml();
        break;
      case 'continueLearning':
        html += getWidgetContinueLearningHtml();
        break;
      case 'habits':
        html += getWidgetHabitsHtml();
        break;
      case 'statistics':
        html += getWidgetStatisticsHtml();
        break;
    }
  });

  container.innerHTML = html;
}

// Widget 1: Important Goals (No progress bars, no progress math, pure goals view)
function getWidgetImportantGoalsHtml() {
  const importantGoals = currentData.goals.filter(g => g.important || g.pinned);
  let listHtml = '';

  if (importantGoals.length === 0) {
    listHtml = '<div class="text-sm text-muted" style="padding: 16px; text-align: center;">No goals marked as important yet. Star or pin goals to see them here.</div>';
  } else {
    listHtml = importantGoals.map(g => `
      <div class="flex items-center justify-between p-2 mb-2" style="border-bottom: 1px solid var(--border); padding: 10px 0;">
        <div style="flex: 1; min-width: 0; padding-right: 12px;">
          <div class="flex items-center gap-2 flex-wrap">
            <span style="font-weight: 600; font-size: 14px; color: var(--text-primary);" class="truncate">${escapeHtml(g.title)}</span>
            <span class="badge ${g.priority === 'Critical' ? 'badge-rose' : g.priority === 'High' ? 'badge-amber' : 'badge-gray'}">${g.priority}</span>
            <span class="badge ${g.status === 'Completed' ? 'badge-emerald' : 'badge-indigo'}">${g.status}</span>
          </div>
          <div class="flex items-center gap-3 mt-1 text-xs text-muted">
            <span>📅 Deadline: ${g.deadline || 'No deadline'}</span>
            <span>📂 ${escapeHtml(g.category || 'General')}</span>
          </div>
        </div>
        <div>
          <button class="btn btn-sm btn-secondary" onclick="toggleGoalStatusOnly('${g.id}')">
            <span>${g.status === 'Completed' ? 'Mark Active' : 'Mark Done'}</span>
          </button>
        </div>
      </div>
    `).join('');
  }

  return `
    <div class="card col-6">
      <div class="card-header">
        <h3 class="card-title">
          <span style="color: #f59e0b;">⭐</span>
          <span>Important Goals</span>
        </h3>
        <button class="btn btn-sm btn-secondary" onclick="navigateTo('goals')">View All</button>
      </div>
      <div>${listHtml}</div>
    </div>
  `;
}

function toggleGoalStatusOnly(id) {
  const g = currentData.goals.find(item => item.id === id);
  if (!g) return;
  g.status = (g.status === 'Completed') ? 'In Progress' : 'Completed';
  saveStorage();
  renderDashboard();
  if (currentView === 'goals') renderGoals();
  showToast(`Goal "${g.title}" updated to ${g.status}`);
}

// Widget 2: Today's To-Do
function getWidgetTodosHtml() {
  const todayStr = new Date().toISOString().split('T')[0];
  const todayTasks = currentData.tasks.filter(t => t.dueDate === todayStr || !t.completed).slice(0, 5);

  let listHtml = '';
  if (todayTasks.length === 0) {
    listHtml = '<div class="text-sm text-muted" style="padding: 16px; text-align: center;">All tasks cleared! Take a break or add new tasks.</div>';
  } else {
    listHtml = todayTasks.map(t => `
      <div class="flex items-center justify-between" style="border-bottom: 1px solid var(--border); padding: 8px 0;">
        <label class="checkbox-label" style="flex: 1;">
          <input type="checkbox" ${t.completed ? 'checked' : ''} onchange="toggleTaskComplete('${t.id}')">
          <span style="${t.completed ? 'text-decoration: line-through; opacity: 0.6;' : ''}; font-weight: 500;">${escapeHtml(t.title)}</span>
        </label>
        <div class="flex items-center gap-2">
          ${t.dueTime ? `<span class="text-xs text-muted">⏰ ${t.dueTime}</span>` : ''}
          <span class="badge ${t.priority === 'Critical' ? 'badge-rose' : t.priority === 'High' ? 'badge-amber' : 'badge-gray'}">${t.priority}</span>
        </div>
      </div>
    `).join('');
  }

  return `
    <div class="card col-6">
      <div class="card-header">
        <h3 class="card-title">
          <span class="icon-slot" data-icon="check-square"></span>
          <span>Actionable To-Do</span>
        </h3>
        <button class="btn btn-sm btn-secondary" onclick="navigateTo('todos')">Manage</button>
      </div>
      <div>${listHtml}</div>
    </div>
  `;
}

// Widget 3: Subjects & Teachers (No progress bars, shows Teacher name, Subject name, and Attendance stats)
function getWidgetSubjectsHtml() {
  const subjectsHtml = currentData.subjects.map(s => {
    return `
      <div class="card" style="padding: 12px; margin-bottom: 10px; border-left: 4px solid ${s.color};">
        <div class="flex items-center justify-between flex-wrap gap-2">
          <div style="flex: 1; min-width: 140px;">
            <div style="font-weight: 700; font-size: 14.5px; color: var(--text-primary);">${escapeHtml(s.name)}</div>
            <div class="text-xs text-muted mt-1">👨‍🏫 Teacher: <strong>${escapeHtml(s.teacherName || 'Not assigned')}</strong></div>
          </div>
          <div class="flex items-center gap-2 flex-wrap">
            <span class="badge badge-rose" title="Total Cancelled Classes">🚫 Cancelled: ${s.cancelledClasses || 0}</span>
            <span class="badge badge-amber" title="Total Absences">❌ Absent: ${s.absentClasses || 0}</span>
            <button class="btn btn-sm btn-secondary" onclick="openSubjectAttendanceHistoryModal('${s.id}')" title="View & Manage Attendance Log">Records</button>
          </div>
        </div>
      </div>
    `;
  }).join('');

  return `
    <div class="card col-6">
      <div class="card-header">
        <h3 class="card-title">
          <span class="icon-slot" data-icon="book-open"></span>
          <span>Subjects & Faculty</span>
        </h3>
        <button class="btn btn-sm btn-secondary" onclick="navigateTo('subjects')">All Subjects</button>
      </div>
      <div>${subjectsHtml}</div>
    </div>
  `;
}

// Widget 4: Current Chapters (No progress bars)
function getWidgetCurrentChaptersHtml() {
  const activeChapters = currentData.chapters.filter(c => c.status === 'In Progress' || c.status === 'Revision Required').slice(0, 4);

  let html = '';
  if (activeChapters.length === 0) {
    html = '<div class="text-sm text-muted" style="padding: 16px; text-align: center;">No chapters currently in progress. Pick a chapter to study!</div>';
  } else {
    html = activeChapters.map(c => {
      const subject = currentData.subjects.find(s => s.id === c.subjectId);
      return `
        <div style="border-bottom: 1px solid var(--border); padding: 10px 0;">
          <div class="flex items-center justify-between mb-1">
            <div style="font-weight: 600; font-size: 13.5px;">
              <span class="badge badge-gray" style="margin-right: 6px;">Ch ${c.chapterNumber}</span>
              ${escapeHtml(c.name)}
            </div>
            <span class="badge ${c.status === 'In Progress' ? 'badge-indigo' : 'badge-amber'}">${c.status}</span>
          </div>
          <div class="flex items-center justify-between text-xs text-muted mt-1">
            <span>📚 ${escapeHtml(subject ? subject.name : 'General')}</span>
            <span>Priority: ${c.priority || 'Normal'}</span>
          </div>
        </div>
      `;
    }).join('');
  }

  return `
    <div class="card col-6">
      <div class="card-header">
        <h3 class="card-title">
          <span class="icon-slot" data-icon="list-tree"></span>
          <span>Current Active Chapters</span>
        </h3>
        <button class="btn btn-sm btn-secondary" onclick="navigateTo('chapters')">Chapters</button>
      </div>
      <div>${html}</div>
    </div>
  `;
}

// Widget 5: Today's Classes with Attendance 3-Dot Action Menu
function getWidgetTodayTimetableHtml() {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const todayName = days[new Date().getDay()];
  const todayStr = new Date().toISOString().split('T')[0];
  const todayClasses = currentData.timetableClasses.filter(c => c.day === todayName);

  let html = '';
  if (todayClasses.length === 0) {
    html = `<div class="text-sm text-muted" style="padding: 16px; text-align: center;">No scheduled lectures for ${todayName}. Great day for self-study!</div>`;
  } else {
    html = todayClasses.map(c => {
      const slot = currentData.timetableSlots.find(s => s.id === c.slotId);
      const slotTime = slot ? slot.label : '';
      const subject = currentData.subjects.find(s => s.id === c.subjectId || s.name === c.subjectName);

      // Check if attendance already marked today for this class or subject
      const subjectRecords = (subject && subject.attendanceRecords) || [];
      const todayRecord = subjectRecords.find(r => r.date === todayStr && (r.classId === c.id || r.subjectId === (subject && subject.id)));

      let statusBadge = '';
      if (todayRecord) {
        if (todayRecord.status === 'cancelled') {
          statusBadge = '<span class="class-attendance-badge badge-rose">🚫 Class Cancelled</span>';
        } else if (todayRecord.status === 'absent') {
          statusBadge = '<span class="class-attendance-badge badge-amber">❌ Absent</span>';
        } else if (todayRecord.status === 'attended') {
          statusBadge = '<span class="class-attendance-badge badge-emerald">✅ Attended</span>';
        }
      }

      return `
        <div class="class-attendance-row" style="border-left: 4px solid ${c.color || 'var(--accent)'};">
          <div style="flex: 1; min-width: 0;">
            <div style="font-weight: 700; font-size: 14px; color: var(--text-primary);">${escapeHtml(c.subjectName)}</div>
            <div class="text-xs text-muted mt-1">
              👨‍🏫 ${escapeHtml(c.teacherName || 'Instructor')} • 📍 Room ${escapeHtml(c.room || 'TBD')} • ⏰ ${slotTime}
            </div>
          </div>
          <div class="flex items-center gap-2" style="position: relative;">
            ${statusBadge}
            <div class="class-menu-container">
              <button class="class-menu-trigger" onclick="toggleTodayClassMenu('${c.id}', event)" title="Attendance Options" aria-label="Attendance options for ${escapeHtml(c.subjectName)}">
                ⋮
              </button>
              <div id="class-menu-${c.id}" class="class-menu-dropdown">
                <button class="class-menu-item danger" onclick="markClassAttendance('${c.id}', 'cancelled', event)">
                  <span>🚫</span>
                  <span>Class Cancelled</span>
                </button>
                <button class="class-menu-item warning" onclick="markClassAttendance('${c.id}', 'absent', event)">
                  <span>❌</span>
                  <span>Absent</span>
                </button>
                <button class="class-menu-item success" onclick="markClassAttendance('${c.id}', 'attended', event)">
                  <span>✅</span>
                  <span>Mark Attended</span>
                </button>
                <div style="border-top: 1px solid var(--border); margin: 3px 0;"></div>
                <button class="class-menu-item" onclick="openSubjectAttendanceHistoryModal('${subject ? subject.id : ''}'); event.stopPropagation();">
                  <span>📋</span>
                  <span>Attendance Records</span>
                </button>
                ${todayRecord ? `
                  <button class="class-menu-item text-muted" onclick="markClassAttendance('${c.id}', 'reset', event)">
                    <span>🔄</span>
                    <span>Reset Today</span>
                  </button>
                ` : ''}
              </div>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  return `
    <div class="card col-6">
      <div class="card-header">
        <h3 class="card-title">
          <span class="icon-slot" data-icon="table"></span>
          <span>Today's Classes (${todayName})</span>
        </h3>
        <button class="btn btn-sm btn-secondary" onclick="navigateTo('timetable')">Full Timetable</button>
      </div>
      <div>${html}</div>
    </div>
  `;
}

// Widget 7: Continue Learning (Videos - No progress bar)
function getWidgetContinueLearningHtml() {
  const videos = currentData.videos.filter(v => !v.completed).slice(0, 3);
  let html = '';

  if (videos.length === 0) {
    html = '<div class="text-sm text-muted" style="padding: 16px; text-align: center;">All videos watched! Add more tutorials in Playlists.</div>';
  } else {
    html = videos.map(v => `
      <div class="flex items-center justify-between" style="border-bottom: 1px solid var(--border); padding: 8px 0;">
        <div style="flex: 1; padding-right: 12px;">
          <div style="font-weight: 600; font-size: 13px; color: var(--text-primary);">${escapeHtml(v.customTitle)}</div>
          <div class="text-xs text-muted mt-1">Duration: ${v.duration || 0} mins • Course Tutorial</div>
        </div>
        <button class="btn btn-sm btn-primary" onclick="openVideoPlayerModal('${v.id}')">
          ${getIconHtml('play')}
          <span>Play</span>
        </button>
      </div>
    `).join('');
  }

  return `
    <div class="card col-6">
      <div class="card-header">
        <h3 class="card-title">
          <span class="icon-slot" data-icon="video"></span>
          <span>Continue Learning</span>
        </h3>
        <button class="btn btn-sm btn-secondary" onclick="navigateTo('playlists')">Playlists</button>
      </div>
      <div>${html}</div>
    </div>
  `;
}

// Widget 8: Habits Today
function getWidgetHabitsHtml() {
  const habits = currentData.habits.slice(0, 4);
  let html = '';

  if (habits.length === 0) {
    html = '<div class="text-sm text-muted" style="padding: 16px; text-align: center;">No habits registered yet. Create daily study habits to build consistency!</div>';
  } else {
    html = habits.map(h => `
      <div class="flex items-center justify-between" style="border-bottom: 1px solid var(--border); padding: 8px 0;">
        <div class="flex items-center gap-3">
          <button class="btn btn-sm ${h.completedToday ? 'btn-primary' : 'btn-secondary'}" onclick="toggleHabitToday('${h.id}')" style="border-radius: 50%; width: 28px; height: 28px; padding: 0;">
            ${h.completedToday ? getIconHtml('check') : ''}
          </button>
          <div>
            <div style="font-weight: 600; font-size: 13px; ${h.completedToday ? 'text-decoration: line-through; opacity: 0.7;' : ''}">${escapeHtml(h.name)}</div>
            <div class="text-xs text-muted">${h.category} • Frequency: ${h.frequency}</div>
          </div>
        </div>
        <div class="flex items-center gap-1 font-semibold" style="color: #f59e0b; font-size: 13px;">
          ${getIconHtml('flame')}
          <span>${h.streak}d</span>
        </div>
      </div>
    `).join('');
  }

  return `
    <div class="card col-6">
      <div class="card-header">
        <h3 class="card-title">
          <span class="icon-slot" data-icon="flame"></span>
          <span>Today's Habit Check</span>
        </h3>
        <button class="btn btn-sm btn-secondary" onclick="navigateTo('habits')">Habits</button>
      </div>
      <div>${html}</div>
    </div>
  `;
}

// Widget 9: Quick Statistics
function getWidgetStatisticsHtml() {
  return `
    <div class="card col-6">
      <div class="card-header">
        <h3 class="card-title">
          <span class="icon-slot" data-icon="bar-chart-3"></span>
          <span>Weekly Study Pulse</span>
        </h3>
        <button class="btn btn-sm btn-secondary" onclick="navigateTo('statistics')">Detailed Stats</button>
      </div>
      <div id="dashboard-quick-stats-graph">
        <!-- SVG mini chart rendered by JS -->
        ${renderMiniSvgActivityChart()}
      </div>
    </div>
  `;
}

function renderMiniSvgActivityChart() {
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const values = [4.5, 6.0, 5.2, 7.5, 6.8, 3.5, 4.0];
  const max = 10;
  
  const bars = days.map((day, i) => {
    const height = Math.round((values[i] / max) * 110);
    const y = 130 - height;
    const x = 30 + i * 46;
    return `
      <g>
        <rect x="${x}" y="${y}" width="24" height="${height}" rx="4" fill="var(--accent)" opacity="0.85"></rect>
        <text x="${x + 12}" y="148" font-size="11" font-weight="600" fill="var(--text-muted)" text-anchor="middle">${day}</text>
        <text x="${x + 12}" y="${y - 6}" font-size="10" font-weight="700" fill="var(--text-primary)" text-anchor="middle">${values[i]}h</text>
      </g>
    `;
  }).join('');

  return `
    <svg width="100%" height="160" viewBox="0 0 360 160" style="overflow: visible;">
      ${bars}
    </svg>
  `;
}

// Dashboard Customization Modal
function openDashboardCustomizeModal() {
  const prefs = currentData.settings.dashboardWidgets || {};
  const order = currentData.settings.widgetOrder || [
    'importantGoals', 'todos', 'subjects', 'currentChapters', 'timetable', 'stickyNotes', 'continueLearning', 'habits', 'statistics'
  ];

  const widgetLabels = {
    importantGoals: '⭐ Important Goals',
    todos: '✅ Actionable To-Do',
    subjects: '📚 Subjects Syllabus Progress',
    currentChapters: '📖 Current Active Chapters',
    timetable: '🗓 Today\\'s Classes',
    stickyNotes: '📝 Recent Sticky Notes',
    continueLearning: '🎥 Continue Learning Videos',
    habits: '🎯 Today\\'s Habits',
    statistics: '📊 Performance Statistics'
  };

  const listItems = order.map((key, idx) => `
    <div class="flex items-center justify-between p-2 mb-2" style="background: var(--bg-input); border-radius: var(--radius-sm); padding: 8px 12px; margin-bottom: 8px;">
      <label class="checkbox-label">
        <input type="checkbox" id="dash-toggle-${key}" ${prefs[key] !== false ? 'checked' : ''}>
        <span style="font-weight: 600;">${widgetLabels[key] || key}</span>
      </label>
      <div class="flex items-center gap-1">
        <button class="btn btn-sm btn-secondary" onclick="moveDashboardWidget('${key}', -1)" ${idx === 0 ? 'disabled' : ''}>▲</button>
        <button class="btn btn-sm btn-secondary" onclick="moveDashboardWidget('${key}', 1)" ${idx === order.length - 1 ? 'disabled' : ''}>▼</button>
      </div>
    </div>
  `).join('');

  openModal({
    title: 'Customize Dashboard Sections',
    body: `
      <p class="text-sm text-muted mb-3" style="margin-bottom: 14px;">Toggle visibility or adjust the order of dashboard cards to tailor your homepage overview.</p>
      <div>${listItems}</div>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="saveDashboardCustomization()">Save Preferences</button>
    `
  });
}

function moveDashboardWidget(key, direction) {
  const order = currentData.settings.widgetOrder;
  const idx = order.indexOf(key);
  if (idx < 0) return;
  const targetIdx = idx + direction;
  if (targetIdx < 0 || targetIdx >= order.length) return;

  const temp = order[idx];
  order[idx] = order[targetIdx];
  order[targetIdx] = temp;

  saveStorage();
  openDashboardCustomizeModal();
  renderDashboard();
}

function saveDashboardCustomization() {
  const prefs = currentData.settings.dashboardWidgets || {};
  const order = currentData.settings.widgetOrder;

  order.forEach(key => {
    const el = document.getElementById('dash-toggle-' + key);
    if (el) prefs[key] = el.checked;
  });

  currentData.settings.dashboardWidgets = prefs;
  saveStorage();
  closeModal();
  renderDashboard();
  showToast('Dashboard customization saved!');
}

/* =========================================================================
   GOALS MANAGER & MERGE GOALS
   ========================================================================= */

let goalFilter = 'all';
let goalSort = 'deadline';
let goalSearch = '';
let selectedGoalIds = new Set();

function renderGoals() {
  const container = document.getElementById('goals-list-container');
  if (!container) return;

  let filtered = [...currentData.goals];

  // Filter
  if (goalFilter === 'important') filtered = filtered.filter(g => g.important || g.pinned);
  else if (goalFilter === 'pending') filtered = filtered.filter(g => g.status !== 'Completed');
  else if (goalFilter === 'completed') filtered = filtered.filter(g => g.status === 'Completed');
  else if (goalFilter === 'today') {
    const today = new Date().toISOString().split('T')[0];
    filtered = filtered.filter(g => g.deadline === today);
  } else if (goalFilter === 'week') {
    const now = new Date();
    const nextWeek = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
    filtered = filtered.filter(g => g.deadline && g.deadline <= nextWeek);
  }

  // Search
  if (goalSearch) {
    const q = goalSearch.toLowerCase();
    filtered = filtered.filter(g => g.title.toLowerCase().includes(q) || (g.description && g.description.toLowerCase().includes(q)));
  }

  // Sort
  filtered.sort((a, b) => {
    if (goalSort === 'deadline') return (a.deadline || '9999') > (b.deadline || '9999') ? 1 : -1;
    if (goalSort === 'priority') {
      const pMap = { 'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1 };
      return (pMap[b.priority] || 0) - (pMap[a.priority] || 0);
    }
    if (goalSort === 'progress') return b.progress - a.progress;
    if (goalSort === 'title') return a.title.localeCompare(b.title);
    if (goalSort === 'created') return (b.created || '').localeCompare(a.created || '');
    return 0;
  });

  // Update Merge Button visibility
  updateMergeButton();

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="col-12 card" style="text-align: center; padding: 40px;">
        <div style="font-size: 36px; margin-bottom: 10px;">🎯</div>
        <h3 style="font-size: 16px; font-weight: 700;">No goals match your filter</h3>
        <p class="text-sm text-muted mt-1">Adjust your filters or create a new goal to start tracking progress.</p>
        <button class="btn btn-primary btn-sm mt-3" style="margin-top: 14px;" onclick="openGoalModal()">+ Create Goal</button>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(g => {
    const isSelected = selectedGoalIds.has(g.id);
    const subtaskCompleted = (g.subtasks || []).filter(s => s.completed).length;
    const subtaskTotal = (g.subtasks || []).length;

    return `
      <div class="card col-6" style="${isSelected ? 'border-color: var(--accent); background: var(--accent-light);' : ''}">
        <div class="card-header">
          <div class="flex items-center gap-2">
            <input type="checkbox" style="width: 16px; height: 16px; cursor: pointer; accent-color: var(--accent);" 
                   ${isSelected ? 'checked' : ''} onchange="toggleGoalSelect('${g.id}', this.checked)">
            <button class="btn btn-icon btn-sm btn-secondary" onclick="toggleGoalImportant('${g.id}')" title="Toggle Star/Important">
              <span style="color: ${g.important ? '#f59e0b' : 'var(--text-muted)'};">★</span>
            </button>
            <h3 class="card-title" style="font-size: 14.5px;">${escapeHtml(g.title)}</h3>
          </div>
          <div class="flex items-center gap-1">
            <button class="btn btn-icon btn-sm btn-secondary" onclick="openGoalModal('${g.id}')" title="Edit Goal">${getIconHtml('edit')}</button>
            <button class="btn btn-icon btn-sm btn-danger" onclick="deleteGoal('${g.id}')" title="Delete Goal">${getIconHtml('trash')}</button>
          </div>
        </div>

        <p class="text-sm text-secondary" style="margin-bottom: 12px; line-height: 1.4;">${escapeHtml(g.description || 'No description provided.')}</p>

        <div class="flex items-center gap-2 flex-wrap mb-3" style="margin-bottom: 12px;">
          <span class="badge ${g.priority === 'Critical' ? 'badge-rose' : g.priority === 'High' ? 'badge-amber' : 'badge-gray'}">${g.priority}</span>
          <span class="badge ${g.status === 'Completed' ? 'badge-emerald' : 'badge-indigo'}">${g.status}</span>
          <span class="badge badge-gray">${g.category || 'General'}</span>
          ${g.deadline ? `<span class="badge badge-sky">📅 ${g.deadline}</span>` : ''}
        </div>

        <!-- Subtasks summary -->
        ${subtaskTotal > 0 ? `
          <div style="background: var(--bg-input); padding: 8px 12px; border-radius: var(--radius-sm); margin-bottom: 12px;">
            <div class="flex items-center justify-between text-xs font-semibold mb-1">
              <span>Subtasks Checklist</span>
              <span>${subtaskCompleted}/${subtaskTotal} Done</span>
            </div>
            ${g.subtasks.map(st => `
              <label class="checkbox-label" style="display: flex; font-size: 12px; margin-top: 4px;">
                <input type="checkbox" ${st.completed ? 'checked' : ''} onchange="toggleGoalSubtask('${g.id}', '${st.id}')">
                <span style="${st.completed ? 'text-decoration: line-through; opacity: 0.6;' : ''}">${escapeHtml(st.title)}</span>
              </label>
            `).join('')}
          </div>
        ` : ''}

        <div class="flex items-center justify-between mt-3" style="margin-top: 12px;">
          <span class="text-xs text-muted">Est: ${g.estimatedTime || 0}h | Logged: ${g.actualTime || 0}h</span>
          <button class="btn btn-sm btn-secondary" onclick="toggleGoalStatusOnly('${g.id}')">
            <span>${g.status === 'Completed' ? 'Mark Active' : 'Mark Completed'}</span>
          </button>
        </div>
      </div>
    `;
  }).join('');
}

function filterGoals(filterType) {
  goalFilter = filterType;
  document.querySelectorAll('[data-goal-filter]').forEach(btn => {
    btn.classList.toggle('btn-primary', btn.getAttribute('data-goal-filter') === filterType);
    btn.classList.toggle('btn-secondary', btn.getAttribute('data-goal-filter') !== filterType);
  });
  renderGoals();
}

function sortGoals(sortType) {
  goalSort = sortType;
  renderGoals();
}

function searchGoals(val) {
  goalSearch = val;
  renderGoals();
}

function toggleGoalSelect(id, isChecked) {
  if (isChecked) selectedGoalIds.add(id);
  else selectedGoalIds.delete(id);
  updateMergeButton();
  renderGoals();
}

function updateMergeButton() {
  const btn = document.getElementById('btn-merge-goals');
  const label = document.getElementById('merge-count-label');
  if (!btn || !label) return;
  if (selectedGoalIds.size >= 2) {
    btn.style.display = 'inline-flex';
    label.textContent = `Merge Selected (${selectedGoalIds.size})`;
  } else {
    btn.style.display = 'none';
  }
}

function toggleGoalImportant(id) {
  const g = currentData.goals.find(item => item.id === id);
  if (!g) return;
  g.important = !g.important;
  saveStorage();
  renderGoals();
  logActivity(`Marked goal "${g.title}" as ${g.important ? 'important' : 'normal'}`);
}

function quickCompleteGoal(id) {
  const g = currentData.goals.find(item => item.id === id);
  if (!g) return;
  g.status = 'Completed';
  g.progress = 100;
  if (g.subtasks) g.subtasks.forEach(st => st.completed = true);
  saveStorage();
  renderGoals();
  renderDashboard();
  logActivity(`Completed goal: "${g.title}" (100%)`);
  showToast(`Goal "${g.title}" marked as completed!`);
}

function toggleGoalSubtask(goalId, subtaskId) {
  const g = currentData.goals.find(item => item.id === goalId);
  if (!g || !g.subtasks) return;
  const st = g.subtasks.find(s => s.id === subtaskId);
  if (!st) return;
  st.completed = !st.completed;

  const allDone = g.subtasks.length > 0 && g.subtasks.every(s => s.completed);
  if (allDone) g.status = 'Completed';
  else if (g.status === 'Completed') g.status = 'In Progress';

  saveStorage();
  renderGoals();
  renderDashboard();
}

function deleteGoal(id) {
  const idx = currentData.goals.findIndex(g => g.id === id);
  if (idx < 0) return;
  const deleted = currentData.goals[idx];

  // Save for Undo
  const prevGoals = [...currentData.goals];
  currentData.goals.splice(idx, 1);
  selectedGoalIds.delete(id);
  saveStorage();
  renderGoals();
  renderDashboard();
  logActivity(`Deleted goal: "${deleted.title}"`);

  showToast(`Goal "${deleted.title}" deleted.`, () => {
    currentData.goals = prevGoals;
    saveStorage();
    renderGoals();
    renderDashboard();
    logActivity(`Undid deletion of goal: "${deleted.title}"`);
  });
}

function openGoalModal(id = null) {
  const goal = id ? currentData.goals.find(g => g.id === id) : null;
  const isEdit = !!goal;

  openModal({
    title: isEdit ? 'Edit Goal' : 'Create New Goal',
    body: `
      <form id="goal-form" onsubmit="handleGoalFormSubmit(event, '${id || ''}')">
        <div class="form-group">
          <label>Goal Title *</label>
          <input type="text" class="form-control" id="goal-title" required value="${escapeHtml(goal ? goal.title : '')}" placeholder="e.g., Master Graph Algorithms">
        </div>
        <div class="form-group">
          <label>Description</label>
          <textarea class="form-control" id="goal-desc" placeholder="Scope, key milestones, and motivation...">${escapeHtml(goal ? goal.description : '')}</textarea>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Category</label>
            <select class="form-control" id="goal-category">
              <option value="Study" ${goal && goal.category === 'Study' ? 'selected' : ''}>Study</option>
              <option value="Academics" ${goal && goal.category === 'Academics' ? 'selected' : ''}>Academics</option>
              <option value="Project" ${goal && goal.category === 'Project' ? 'selected' : ''}>Project</option>
              <option value="Career" ${goal && goal.category === 'Career' ? 'selected' : ''}>Career</option>
              <option value="Personal" ${goal && goal.category === 'Personal' ? 'selected' : ''}>Personal</option>
            </select>
          </div>
          <div class="form-group">
            <label>Priority</label>
            <select class="form-control" id="goal-priority">
              <option value="Low" ${goal && goal.priority === 'Low' ? 'selected' : ''}>Low</option>
              <option value="Medium" ${!goal || goal.priority === 'Medium' ? 'selected' : ''}>Medium</option>
              <option value="High" ${goal && goal.priority === 'High' ? 'selected' : ''}>High</option>
              <option value="Critical" ${goal && goal.priority === 'Critical' ? 'selected' : ''}>Critical</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Start Date</label>
            <input type="date" class="form-control" id="goal-start" value="${goal ? goal.startDate || '' : ''}">
          </div>
          <div class="form-group">
            <label>Target Deadline</label>
            <input type="date" class="form-control" id="goal-deadline" value="${goal ? goal.deadline || '' : ''}">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group" style="flex: 1;">
            <label>Status</label>
            <select class="form-control" id="goal-status">
              <option value="Not Started" ${goal && goal.status === 'Not Started' ? 'selected' : ''}>Not Started</option>
              <option value="In Progress" ${!goal || goal.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
              <option value="Completed" ${goal && goal.status === 'Completed' ? 'selected' : ''}>Completed</option>
              <option value="Paused" ${goal && goal.status === 'Paused' ? 'selected' : ''}>Paused</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Est. Hours</label>
            <input type="number" class="form-control" id="goal-est" min="0" value="${goal ? goal.estimatedTime || 0 : 0}">
          </div>
          <div class="form-group">
            <label>Actual Hours</label>
            <input type="number" class="form-control" id="goal-actual" min="0" value="${goal ? goal.actualTime || 0 : 0}">
          </div>
        </div>
        <div class="form-group">
          <label class="checkbox-label">
            <input type="checkbox" id="goal-important" ${goal && goal.important ? 'checked' : ''}>
            <span>Mark as Important / Pinned on Dashboard</span>
          </label>
        </div>
      </form>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="document.getElementById('goal-form').requestSubmit()">${isEdit ? 'Save Changes' : 'Create Goal'}</button>
    `
  });
}

function handleGoalFormSubmit(e, editId) {
  e.preventDefault();
  const title = document.getElementById('goal-title').value.trim();
  if (!title) return;

  const desc = document.getElementById('goal-desc').value.trim();
  const category = document.getElementById('goal-category').value;
  const priority = document.getElementById('goal-priority').value;
  const startDate = document.getElementById('goal-start').value;
  const deadline = document.getElementById('goal-deadline').value;
  const status = document.getElementById('goal-status').value;
  const est = parseFloat(document.getElementById('goal-est').value) || 0;
  const actual = parseFloat(document.getElementById('goal-actual').value) || 0;
  const important = document.getElementById('goal-important').checked;

  if (editId) {
    const g = currentData.goals.find(item => item.id === editId);
    if (g) {
      g.title = title;
      g.description = desc;
      g.category = category;
      g.priority = priority;
      g.startDate = startDate;
      g.deadline = deadline;
      g.status = status;
      g.estimatedTime = est;
      g.actualTime = actual;
      g.important = important;
      g.updated = new Date().toISOString();
      logActivity(`Edited goal: "${title}"`);
    }
  } else {
    const newGoal = {
      id: 'g-' + Date.now(),
      title,
      description: desc,
      category,
      priority,
      startDate,
      deadline,
      status,
      estimatedTime: est,
      actualTime: actual,
      important,
      pinned: important,
      subtasks: [],
      created: new Date().toISOString()
    };
    currentData.goals.push(newGoal);
    logActivity(`Created goal: "${title}"`);
  }

  saveStorage();
  closeModal();
  renderGoals();
  renderDashboard();
  showToast(editId ? 'Goal updated successfully!' : 'New goal created!');
}

// Merge Goals Feature
function openMergeGoalsModal() {
  const selectedGoals = currentData.goals.filter(g => selectedGoalIds.has(g.id));
  if (selectedGoals.length < 2) return;

  const suggestedTitle = selectedGoals.map(g => g.title).join(' & ');
  const combinedDesc = selectedGoals.map(g => `• ${g.title}: ${g.description || ''}`).join('\\n');
  const combinedNotes = selectedGoals.filter(g => g.notes).map(g => `[${g.title}]: ${g.notes}`).join('\\n');
  
  // Combine all subtasks
  const combinedSubtasks = [];
  selectedGoals.forEach(g => {
    (g.subtasks || []).forEach(st => {
      combinedSubtasks.push({ id: 'st-' + Date.now() + '-' + Math.random().toString(36).substr(2, 4), title: `[${g.title}] ${st.title}`, completed: st.completed });
    });
  });

  const avgProgress = Math.round(selectedGoals.reduce((acc, g) => acc + (g.progress || 0), 0) / selectedGoals.length);
  const totalEst = selectedGoals.reduce((acc, g) => acc + (g.estimatedTime || 0), 0);
  const totalActual = selectedGoals.reduce((acc, g) => acc + (g.actualTime || 0), 0);

  openModal({
    title: `Merge ${selectedGoals.length} Selected Goals`,
    body: `
      <div class="alert mb-3" style="background: var(--warning-light); color: var(--warning); padding: 10px; border-radius: var(--radius-sm); margin-bottom: 14px; font-size: 13px;">
        ⚠️ Merging will combine selected goals into a single new consolidated goal. The original goals will be safely archived into history.
      </div>
      <div class="form-group">
        <label>Merged Goal Title *</label>
        <input type="text" class="form-control" id="merge-goal-title" value="${escapeHtml(suggestedTitle)}">
      </div>
      <div class="form-group">
        <label>Consolidated Description</label>
        <textarea class="form-control" id="merge-goal-desc" rows="4">${escapeHtml(combinedDesc)}</textarea>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Consolidated Progress (%)</label>
          <input type="number" class="form-control" id="merge-goal-progress" min="0" max="100" value="${avgProgress}">
        </div>
        <div class="form-group">
          <label>Total Est. Time (hrs)</label>
          <input type="number" class="form-control" id="merge-goal-est" value="${totalEst}">
        </div>
      </div>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="confirmMergeGoals()">Confirm & Merge Goals</button>
    `
  });
}

function confirmMergeGoals() {
  const selectedGoals = currentData.goals.filter(g => selectedGoalIds.has(g.id));
  const newTitle = document.getElementById('merge-goal-title').value.trim();
  if (!newTitle) return;

  const newDesc = document.getElementById('merge-goal-desc').value.trim();
  const progress = parseInt(document.getElementById('merge-goal-progress').value) || 0;
  const est = parseFloat(document.getElementById('merge-goal-est').value) || 0;

  // Preserve earliest or closest deadline
  const deadlines = selectedGoals.map(g => g.deadline).filter(Boolean).sort();
  const deadline = deadlines[0] || '';

  const mergedGoal = {
    id: 'g-' + Date.now(),
    title: newTitle,
    description: newDesc,
    category: selectedGoals[0].category || 'Academics',
    priority: 'High',
    startDate: new Date().toISOString().split('T')[0],
    deadline: deadline,
    status: progress >= 100 ? 'Completed' : 'In Progress',
    progress: progress,
    estimatedTime: est,
    actualTime: selectedGoals.reduce((acc, g) => acc + (g.actualTime || 0), 0),
    important: true,
    pinned: true,
    subtasks: [],
    created: new Date().toISOString()
  };

  // Combine subtasks
  selectedGoals.forEach(g => {
    (g.subtasks || []).forEach(st => {
      mergedGoal.subtasks.push({
        id: 'st-' + Date.now() + '-' + Math.random().toString(36).substr(2, 4),
        title: st.title,
        completed: st.completed
      });
    });
  });

  // Archive / remove originals
  const prevGoals = [...currentData.goals];
  currentData.goals = currentData.goals.filter(g => !selectedGoalIds.has(g.id));
  currentData.goals.push(mergedGoal);
  selectedGoalIds.clear();

  saveStorage();
  closeModal();
  renderGoals();
  renderDashboard();
  logActivity(`Merged ${selectedGoals.length} goals into "${newTitle}"`);

  showToast(`Successfully merged into "${newTitle}"`, () => {
    currentData.goals = prevGoals;
    saveStorage();
    renderGoals();
    renderDashboard();
    logActivity('Undid goal merger.');
  });
}

/* =========================================================================
   TO-DO MANAGER
   ========================================================================= */

let todoCategoryFilter = 'all';
let todoStatusFilter = 'all';
let todoSearchQuery = '';

function renderTodos() {
  const container = document.getElementById('todos-list-container');
  const pillsContainer = document.getElementById('todo-category-pills');
  if (!container) return;

  // Extract all categories
  const categories = ['All', 'Study', 'Academics', 'Homework', 'Personal', 'General'];
  if (pillsContainer) {
    pillsContainer.innerHTML = categories.map(cat => `
      <button class="btn btn-sm ${todoCategoryFilter.toLowerCase() === cat.toLowerCase() ? 'btn-primary' : 'btn-secondary'}" 
              onclick="setTodoCategory('${cat.toLowerCase()}')">
        ${cat}
      </button>
    `).join('');
  }

  let filtered = [...currentData.tasks];

  // Category filter
  if (todoCategoryFilter !== 'all') {
    filtered = filtered.filter(t => (t.category || 'General').toLowerCase() === todoCategoryFilter.toLowerCase());
  }

  // Status filter
  const todayStr = new Date().toISOString().split('T')[0];
  if (todoStatusFilter === 'pending') filtered = filtered.filter(t => !t.completed);
  else if (todoStatusFilter === 'today') filtered = filtered.filter(t => t.dueDate === todayStr);
  else if (todoStatusFilter === 'completed') filtered = filtered.filter(t => t.completed);
  else if (todoStatusFilter === 'high') filtered = filtered.filter(t => t.priority === 'High' || t.priority === 'Critical');

  // Search
  if (todoSearchQuery) {
    const q = todoSearchQuery.toLowerCase();
    filtered = filtered.filter(t => t.title.toLowerCase().includes(q) || (t.notes && t.notes.toLowerCase().includes(q)));
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px;">
        <div style="font-size: 32px; margin-bottom: 8px;">📋</div>
        <h3 style="font-size: 15px; font-weight: 700;">No tasks found</h3>
        <p class="text-sm text-muted">Create a new task to organize your day.</p>
        <button class="btn btn-primary btn-sm mt-3" style="margin-top: 12px;" onclick="openTaskModal()">+ Add Task</button>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map((t, idx) => `
    <div class="flex items-center justify-between p-3 mb-2" style="border-bottom: 1px solid var(--border); padding: 10px 0;">
      <div class="flex items-center gap-3" style="flex: 1;">
        <input type="checkbox" style="width: 18px; height: 18px; cursor: pointer; accent-color: var(--accent);" 
               ${t.completed ? 'checked' : ''} onchange="toggleTaskComplete('${t.id}')">
        <div>
          <div style="font-weight: 600; font-size: 14px; ${t.completed ? 'text-decoration: line-through; opacity: 0.6;' : ''}">
            ${escapeHtml(t.title)}
          </div>
          <div class="flex items-center gap-2 mt-1 text-xs text-muted flex-wrap">
            <span class="badge ${t.priority === 'Critical' ? 'badge-rose' : t.priority === 'High' ? 'badge-amber' : 'badge-gray'}">${t.priority}</span>
            <span class="badge badge-gray">${t.category || 'General'}</span>
            ${t.dueDate ? `<span>📅 Due: ${t.dueDate}</span>` : ''}
            ${t.dueTime ? `<span>⏰ ${t.dueTime}</span>` : ''}
            ${t.recurring && t.recurring !== 'none' ? `<span class="badge badge-sky">🔁 ${t.recurring}</span>` : ''}
          </div>
          ${t.notes ? `<div class="text-xs text-secondary mt-1" style="font-style: italic;">${escapeHtml(t.notes)}</div>` : ''}
        </div>
      </div>
      <div class="flex items-center gap-1">
        <button class="btn btn-sm btn-secondary" onclick="moveTask('${t.id}', -1)" ${idx === 0 ? 'disabled' : ''} title="Move Up">▲</button>
        <button class="btn btn-sm btn-secondary" onclick="moveTask('${t.id}', 1)" ${idx === filtered.length - 1 ? 'disabled' : ''} title="Move Down">▼</button>
        <button class="btn btn-icon btn-sm btn-secondary" onclick="openTaskModal('${t.id}')" title="Edit Task">${getIconHtml('edit')}</button>
        <button class="btn btn-icon btn-sm btn-danger" onclick="deleteTask('${t.id}')" title="Delete Task">${getIconHtml('trash')}</button>
      </div>
    </div>
  `).join('');
}

function setTodoCategory(cat) {
  todoCategoryFilter = cat;
  renderTodos();
}

function filterTodoStatus(val) {
  todoStatusFilter = val;
  renderTodos();
}

function searchTasks(val) {
  todoSearchQuery = val;
  renderTodos();
}

function toggleTaskComplete(id) {
  const t = currentData.tasks.find(item => item.id === id);
  if (!t) return;
  t.completed = !t.completed;
  saveStorage();
  renderTodos();
  renderDashboard();
  logActivity(`${t.completed ? 'Completed' : 'Reopened'} task: "${t.title}"`);
}

function moveTask(id, dir) {
  const idx = currentData.tasks.findIndex(t => t.id === id);
  if (idx < 0) return;
  const targetIdx = idx + dir;
  if (targetIdx < 0 || targetIdx >= currentData.tasks.length) return;

  const temp = currentData.tasks[idx];
  currentData.tasks[idx] = currentData.tasks[targetIdx];
  currentData.tasks[targetIdx] = temp;

  saveStorage();
  renderTodos();
}

function deleteTask(id) {
  const idx = currentData.tasks.findIndex(t => t.id === id);
  if (idx < 0) return;
  const deleted = currentData.tasks[idx];
  const prevTasks = [...currentData.tasks];

  currentData.tasks.splice(idx, 1);
  saveStorage();
  renderTodos();
  renderDashboard();
  logActivity(`Deleted task: "${deleted.title}"`);

  showToast(`Task "${deleted.title}" deleted.`, () => {
    currentData.tasks = prevTasks;
    saveStorage();
    renderTodos();
    renderDashboard();
    logActivity(`Undid deletion of task: "${deleted.title}"`);
  });
}

function openTaskModal(id = null) {
  const task = id ? currentData.tasks.find(t => t.id === id) : null;
  const isEdit = !!task;

  openModal({
    title: isEdit ? 'Edit Task' : 'Add New Task',
    body: `
      <form id="task-form" onsubmit="handleTaskFormSubmit(event, '${id || ''}')">
        <div class="form-group">
          <label>Task Title *</label>
          <input type="text" class="form-control" id="task-title" required value="${escapeHtml(task ? task.title : '')}" placeholder="e.g., Complete AVL tree rotations">
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Category</label>
            <select class="form-control" id="task-category">
              <option value="Study" ${task && task.category === 'Study' ? 'selected' : ''}>Study</option>
              <option value="Academics" ${task && task.category === 'Academics' ? 'selected' : ''}>Academics</option>
              <option value="Homework" ${task && task.category === 'Homework' ? 'selected' : ''}>Homework</option>
              <option value="Personal" ${task && task.category === 'Personal' ? 'selected' : ''}>Personal</option>
              <option value="General" ${!task || task.category === 'General' ? 'selected' : ''}>General</option>
            </select>
          </div>
          <div class="form-group">
            <label>Priority</label>
            <select class="form-control" id="task-priority">
              <option value="Low" ${task && task.priority === 'Low' ? 'selected' : ''}>Low</option>
              <option value="Medium" ${!task || task.priority === 'Medium' ? 'selected' : ''}>Medium</option>
              <option value="High" ${task && task.priority === 'High' ? 'selected' : ''}>High</option>
              <option value="Critical" ${task && task.priority === 'Critical' ? 'selected' : ''}>Critical</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Due Date</label>
            <input type="date" class="form-control" id="task-due-date" value="${task ? task.dueDate || '' : new Date().toISOString().split('T')[0]}">
          </div>
          <div class="form-group">
            <label>Due Time</label>
            <input type="time" class="form-control" id="task-due-time" value="${task ? task.dueTime || '' : '18:00'}">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Recurrence</label>
            <select class="form-control" id="task-recurring">
              <option value="none" ${!task || task.recurring === 'none' ? 'selected' : ''}>None (One-time)</option>
              <option value="daily" ${task && task.recurring === 'daily' ? 'selected' : ''}>Daily</option>
              <option value="weekly" ${task && task.recurring === 'weekly' ? 'selected' : ''}>Weekly</option>
              <option value="monthly" ${task && task.recurring === 'monthly' ? 'selected' : ''}>Monthly</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label>Notes & Hints</label>
          <textarea class="form-control" id="task-notes" placeholder="Any special instructions or links...">${escapeHtml(task ? task.notes : '')}</textarea>
        </div>
      </form>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="document.getElementById('task-form').requestSubmit()">${isEdit ? 'Save Task' : 'Create Task'}</button>
    `
  });
}

function handleTaskFormSubmit(e, editId) {
  e.preventDefault();
  const title = document.getElementById('task-title').value.trim();
  if (!title) return;

  const category = document.getElementById('task-category').value;
  const priority = document.getElementById('task-priority').value;
  const dueDate = document.getElementById('task-due-date').value;
  const dueTime = document.getElementById('task-due-time').value;
  const recurring = document.getElementById('task-recurring').value;
  const notes = document.getElementById('task-notes').value.trim();

  if (editId) {
    const t = currentData.tasks.find(item => item.id === editId);
    if (t) {
      t.title = title;
      t.category = category;
      t.priority = priority;
      t.dueDate = dueDate;
      t.dueTime = dueTime;
      t.recurring = recurring;
      t.notes = notes;
      logActivity(`Edited task: "${title}"`);
    }
  } else {
    const newTask = {
      id: 't-' + Date.now(),
      title,
      category,
      priority,
      dueDate,
      dueTime,
      recurring,
      notes,
      completed: false,
      subtasks: [],
      created: new Date().toISOString()
    };
    currentData.tasks.unshift(newTask);
    logActivity(`Created task: "${title}"`);
  }

  saveStorage();
  closeModal();
  renderTodos();
  renderDashboard();
  showToast(editId ? 'Task updated!' : 'Task added!');
}

/* =========================================================================
   ATTENDANCE & CLASS CANCELLATION TRACKING LOGIC
   ========================================================================= */

function toggleTodayClassMenu(classId, event) {
  if (event) event.stopPropagation();
  const menu = document.getElementById(`class-menu-${classId}`);
  if (!menu) return;

  const isOpen = menu.classList.contains('active');
  closeAllAttendanceMenus();
  if (!isOpen) {
    menu.classList.add('active');
  }
}

function closeAllAttendanceMenus() {
  document.querySelectorAll('.class-menu-dropdown.active').forEach(m => m.classList.remove('active'));
}

// Close menus when clicking outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.class-menu-container')) {
    closeAllAttendanceMenus();
  }
});

function markClassAttendance(classId, action, event) {
  if (event) event.stopPropagation();
  closeAllAttendanceMenus();

  const c = currentData.timetableClasses.find(item => item.id === classId);
  if (!c) return;

  const todayStr = new Date().toISOString().split('T')[0];
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const todayDay = days[new Date().getDay()];

  // Find corresponding subject
  let subject = currentData.subjects.find(s => s.id === c.subjectId);
  if (!subject) {
    subject = currentData.subjects.find(s => s.name.trim().toLowerCase() === c.subjectName.trim().toLowerCase());
  }

  if (!subject) {
    showToast(`Subject for "${c.subjectName}" not found.`);
    return;
  }

  if (!subject.attendanceRecords) subject.attendanceRecords = [];
  if (typeof subject.cancelledClasses !== 'number') subject.cancelledClasses = 0;
  if (typeof subject.absentClasses !== 'number') subject.absentClasses = 0;

  // Check if an entry for this class today already exists
  const existingIdx = subject.attendanceRecords.findIndex(r => r.date === todayStr && (r.classId === classId || r.subjectId === subject.id));

  if (action === 'reset') {
    if (existingIdx >= 0) {
      const prev = subject.attendanceRecords[existingIdx];
      if (prev.status === 'cancelled') subject.cancelledClasses = Math.max(0, subject.cancelledClasses - 1);
      if (prev.status === 'absent') subject.absentClasses = Math.max(0, subject.absentClasses - 1);
      subject.attendanceRecords.splice(existingIdx, 1);
      logActivity(`Reset attendance status for "${c.subjectName}"`);
      showToast(`Attendance record cleared for ${c.subjectName}`);
    }
  } else if (action === 'cancelled') {
    if (existingIdx >= 0) {
      const prev = subject.attendanceRecords[existingIdx];
      if (prev.status === 'absent') subject.absentClasses = Math.max(0, subject.absentClasses - 1);
      if (prev.status !== 'cancelled') subject.cancelledClasses += 1;
      subject.attendanceRecords[existingIdx] = {
        id: prev.id || ('att-' + Date.now()),
        date: todayStr,
        day: todayDay,
        status: 'cancelled',
        classId: c.id,
        subjectId: subject.id,
        subjectName: subject.name,
        timestamp: new Date().toISOString()
      };
    } else {
      subject.cancelledClasses += 1;
      subject.attendanceRecords.push({
        id: 'att-' + Date.now(),
        date: todayStr,
        day: todayDay,
        status: 'cancelled',
        classId: c.id,
        subjectId: subject.id,
        subjectName: subject.name,
        timestamp: new Date().toISOString()
      });
    }
    logActivity(`Marked "${c.subjectName}" class as CANCELLED`);
    showToast(`Class for "${subject.name}" marked as Cancelled. Total: ${subject.cancelledClasses}`);
  } else if (action === 'absent') {
    if (existingIdx >= 0) {
      const prev = subject.attendanceRecords[existingIdx];
      if (prev.status === 'cancelled') subject.cancelledClasses = Math.max(0, subject.cancelledClasses - 1);
      if (prev.status !== 'absent') subject.absentClasses += 1;
      subject.attendanceRecords[existingIdx] = {
        id: prev.id || ('att-' + Date.now()),
        date: todayStr,
        day: todayDay,
        status: 'absent',
        classId: c.id,
        subjectId: subject.id,
        subjectName: subject.name,
        timestamp: new Date().toISOString()
      };
    } else {
      subject.absentClasses += 1;
      subject.attendanceRecords.push({
        id: 'att-' + Date.now(),
        date: todayStr,
        day: todayDay,
        status: 'absent',
        classId: c.id,
        subjectId: subject.id,
        subjectName: subject.name,
        timestamp: new Date().toISOString()
      });
    }
    logActivity(`Marked ABSENT for "${c.subjectName}"`);
    showToast(`Marked Absent for "${subject.name}". Total Absences: ${subject.absentClasses}`);
  } else if (action === 'attended') {
    if (existingIdx >= 0) {
      const prev = subject.attendanceRecords[existingIdx];
      if (prev.status === 'cancelled') subject.cancelledClasses = Math.max(0, subject.cancelledClasses - 1);
      if (prev.status === 'absent') subject.absentClasses = Math.max(0, subject.absentClasses - 1);
      subject.attendanceRecords[existingIdx] = {
        id: prev.id || ('att-' + Date.now()),
        date: todayStr,
        day: todayDay,
        status: 'attended',
        classId: c.id,
        subjectId: subject.id,
        subjectName: subject.name,
        timestamp: new Date().toISOString()
      };
    } else {
      subject.attendanceRecords.push({
        id: 'att-' + Date.now(),
        date: todayStr,
        day: todayDay,
        status: 'attended',
        classId: c.id,
        subjectId: subject.id,
        subjectName: subject.name,
        timestamp: new Date().toISOString()
      });
    }
    logActivity(`Marked ATTENDED for "${c.subjectName}"`);
    showToast(`Marked Attended for "${subject.name}"`);
  }

  saveStorage();
  renderDashboard();
  if (currentView === 'subjects') renderSubjects();
}

function openSubjectAttendanceHistoryModal(subjectId) {
  let s = null;
  if (subjectId) {
    s = currentData.subjects.find(item => item.id === subjectId);
  }
  if (!s && currentData.subjects.length > 0) {
    s = currentData.subjects[0];
  }
  if (!s) {
    showToast('No subjects available.');
    return;
  }

  if (!s.attendanceRecords) s.attendanceRecords = [];
  if (typeof s.cancelledClasses !== 'number') s.cancelledClasses = 0;
  if (typeof s.absentClasses !== 'number') s.absentClasses = 0;

  // Options for subject selector if user wants to switch subject in modal
  const subjectSelectOptions = currentData.subjects.map(sub => `
    <option value="${sub.id}" ${sub.id === s.id ? 'selected' : ''}>${escapeHtml(sub.name)}</option>
  `).join('');

  const recordsHtml = s.attendanceRecords.length === 0 ? `
    <div class="text-sm text-muted" style="text-align: center; padding: 24px; background: var(--bg-input); border-radius: var(--radius-sm);">
      No attendance or cancellation records logged yet for this subject.
    </div>
  ` : `
    <div style="max-height: 280px; overflow-y: auto;">
      <table class="table" style="width: 100%; font-size: 13px;">
        <thead>
          <tr>
            <th>Date</th>
            <th>Day</th>
            <th>Status</th>
            <th style="text-align: right;">Action</th>
          </tr>
        </thead>
        <tbody>
          ${[...s.attendanceRecords].reverse().map(r => `
            <tr>
              <td><strong>${r.date}</strong></td>
              <td class="text-muted">${r.day || '-'}</td>
              <td>
                <span class="badge ${r.status === 'cancelled' ? 'badge-rose' : r.status === 'absent' ? 'badge-amber' : 'badge-emerald'}">
                  ${r.status === 'cancelled' ? '🚫 Cancelled' : r.status === 'absent' ? '❌ Absent' : '✅ Attended'}
                </span>
              </td>
              <td style="text-align: right;">
                <button class="btn btn-icon btn-sm btn-danger" onclick="deleteAttendanceRecord('${s.id}', '${r.id}')" title="Delete record">
                  ${getIconHtml('trash')}
                </button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;

  openModal({
    title: `Attendance & Cancellation Records — ${escapeHtml(s.name)}`,
    body: `
      <div>
        <div class="form-group mb-3">
          <label>Select Subject</label>
          <select class="form-control" onchange="openSubjectAttendanceHistoryModal(this.value)">
            ${subjectSelectOptions}
          </select>
        </div>

        <div class="flex items-center gap-3 mb-4 flex-wrap">
          <div class="card" style="flex: 1; padding: 12px; background: rgba(239, 68, 68, 0.08); border-left: 4px solid var(--danger);">
            <div class="text-xs text-muted">Total Cancelled Classes</div>
            <div style="font-size: 22px; font-weight: 800; color: var(--danger);">${s.cancelledClasses || 0}</div>
          </div>
          <div class="card" style="flex: 1; padding: 12px; background: rgba(245, 158, 11, 0.08); border-left: 4px solid var(--warning);">
            <div class="text-xs text-muted">Total Absences</div>
            <div style="font-size: 22px; font-weight: 800; color: var(--warning);">${s.absentClasses || 0}</div>
          </div>
          <div class="card" style="flex: 1; padding: 12px; background: var(--bg-input);">
            <div class="text-xs text-muted">Total Logged Entries</div>
            <div style="font-size: 22px; font-weight: 800; color: var(--text-primary);">${s.attendanceRecords.length}</div>
          </div>
        </div>

        <!-- Add Manual Record Section -->
        <div class="card mb-4" style="padding: 14px; background: var(--bg-surface);">
          <div style="font-size: 13.5px; font-weight: 700; margin-bottom: 8px;">➕ Add Attendance / Cancellation Entry</div>
          <div class="form-row">
            <div class="form-group" style="flex: 1;">
              <label>Record Date</label>
              <input type="date" class="form-control" id="manual-att-date" value="${new Date().toISOString().split('T')[0]}">
            </div>
            <div class="form-group" style="flex: 1;">
              <label>Status</label>
              <select class="form-control" id="manual-att-status">
                <option value="cancelled">🚫 Class Cancelled</option>
                <option value="absent">❌ Absent</option>
                <option value="attended">✅ Attended</option>
              </select>
            </div>
            <div class="form-group" style="align-self: flex-end;">
              <button class="btn btn-primary" onclick="handleManualAttendanceSubmit('${s.id}')">Add Entry</button>
            </div>
          </div>
        </div>

        <!-- Logged Table -->
        <div class="card" style="padding: 14px;">
          <div style="font-size: 13.5px; font-weight: 700; margin-bottom: 8px;">📜 Logged Records History</div>
          ${recordsHtml}
        </div>
      </div>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Close</button>
    `
  });
}

function handleManualAttendanceSubmit(subjectId) {
  const s = currentData.subjects.find(item => item.id === subjectId);
  if (!s) return;

  const dateInput = document.getElementById('manual-att-date');
  const statusInput = document.getElementById('manual-att-status');
  if (!dateInput || !statusInput) return;

  const dateStr = dateInput.value;
  const status = statusInput.value;
  if (!dateStr) return;

  if (!s.attendanceRecords) s.attendanceRecords = [];
  if (typeof s.cancelledClasses !== 'number') s.cancelledClasses = 0;
  if (typeof s.absentClasses !== 'number') s.absentClasses = 0;

  const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const parsedDate = new Date(dateStr + 'T00:00:00');
  const dayName = isNaN(parsedDate.getTime()) ? '' : dayNames[parsedDate.getDay()];

  if (status === 'cancelled') s.cancelledClasses += 1;
  else if (status === 'absent') s.absentClasses += 1;

  s.attendanceRecords.push({
    id: 'att-' + Date.now(),
    date: dateStr,
    day: dayName,
    status: status,
    subjectId: s.id,
    subjectName: s.name,
    timestamp: new Date().toISOString()
  });

  saveStorage();
  logActivity(`Added manual ${status} entry for "${s.name}" on ${dateStr}`);
  showToast(`Attendance entry added for ${s.name}`);
  openSubjectAttendanceHistoryModal(s.id);
  renderDashboard();
  if (currentView === 'subjects') renderSubjects();
}

function deleteAttendanceRecord(subjectId, recordId) {
  const s = currentData.subjects.find(item => item.id === subjectId);
  if (!s || !s.attendanceRecords) return;

  const idx = s.attendanceRecords.findIndex(r => r.id === recordId);
  if (idx < 0) return;

  const rec = s.attendanceRecords[idx];
  if (rec.status === 'cancelled') s.cancelledClasses = Math.max(0, (s.cancelledClasses || 0) - 1);
  if (rec.status === 'absent') s.absentClasses = Math.max(0, (s.absentClasses || 0) - 1);

  s.attendanceRecords.splice(idx, 1);
  saveStorage();
  logActivity(`Deleted attendance entry for "${s.name}"`);
  showToast('Attendance entry removed.');
  openSubjectAttendanceHistoryModal(s.id);
  renderDashboard();
  if (currentView === 'subjects') renderSubjects();
}
"""
