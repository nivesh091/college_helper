# Views Part 3: Calendar, Planner, Notes, Stickies, Playlists, Habits, Timer, Statistics, Settings, Global Search
js_views_3_code = """
/* =========================================================================
   CALENDAR VIEW
   ========================================================================= */

let calendarCurrentDate = new Date();

function renderCalendar() {
  const container = document.getElementById('calendar-view-container');
  const monthYearEl = document.getElementById('calendar-month-year');
  if (!container) return;

  const year = calendarCurrentDate.getFullYear();
  const month = calendarCurrentDate.getMonth();

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  if (monthYearEl) monthYearEl.textContent = `${monthNames[month]} ${year}`;

  const firstDayIndex = new Date(year, month, 1).getDay(); // 0 = Sun
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const daysInPrevMonth = new Date(year, month, 0).getDate();

  const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  let html = `
    <div class="calendar-grid">
      ${dayHeaders.map(dh => `<div class="calendar-day-header">${dh}</div>`).join('')}
  `;

  // Previous month padding
  for (let i = firstDayIndex - 1; i >= 0; i--) {
    const d = daysInPrevMonth - i;
    html += `<div class="calendar-day-cell other-month"><div class="calendar-day-num">${d}</div></div>`;
  }

  // Current month days
  const today = new Date();
  const isCurrentMonthYear = today.getFullYear() === year && today.getMonth() === month;

  for (let day = 1; day <= daysInMonth; day++) {
    const isToday = isCurrentMonthYear && today.getDate() === day;
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

    // Find items for this date
    const events = (currentData.calendarEvents || []).filter(e => e.date === dateStr);
    const tasks = (currentData.tasks || []).filter(t => t.dueDate === dateStr);
    const goals = (currentData.goals || []).filter(g => g.deadline === dateStr);

    html += `
      <div class="calendar-day-cell ${isToday ? 'today' : ''}" onclick="openDayDetailModal('${dateStr}')">
        <div class="calendar-day-num">${day}</div>
        <div class="calendar-events-wrap">
          ${events.map(ev => `
            <div class="calendar-event-pill ${ev.type === 'Exam' ? 'event-exam' : 'event-assignment'}" title="${escapeHtml(ev.title)}">
              ${escapeHtml(ev.title)}
            </div>
          `).join('')}
          ${tasks.map(t => `
            <div class="calendar-event-pill event-task" title="Task: ${escapeHtml(t.title)}">
              ✓ ${escapeHtml(t.title)}
            </div>
          `).join('')}
          ${goals.map(g => `
            <div class="calendar-event-pill event-goal" title="Goal Deadline: ${escapeHtml(g.title)}">
              🎯 ${escapeHtml(g.title)}
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  // Next month padding
  const totalRendered = firstDayIndex + daysInMonth;
  const remainingCells = (7 - (totalRendered % 7)) % 7;
  for (let i = 1; i <= remainingCells; i++) {
    html += `<div class="calendar-day-cell other-month"><div class="calendar-day-num">${i}</div></div>`;
  }

  html += `</div>`;
  container.innerHTML = html;
}

function changeCalendarMonth(delta) {
  calendarCurrentDate.setMonth(calendarCurrentDate.getMonth() + delta);
  renderCalendar();
}

function resetCalendarToToday() {
  calendarCurrentDate = new Date();
  renderCalendar();
}

function openDayDetailModal(dateStr) {
  const events = (currentData.calendarEvents || []).filter(e => e.date === dateStr);
  const tasks = (currentData.tasks || []).filter(t => t.dueDate === dateStr);
  const goals = (currentData.goals || []).filter(g => g.deadline === dateStr);

  openModal({
    title: `Agenda for ${dateStr}`,
    body: `
      <div class="flex items-center justify-between mb-3">
        <span class="badge badge-indigo">Daily Agenda & Timeline</span>
        <button class="btn btn-sm btn-primary" onclick="closeModal(); openCalendarEventModal(null, '${dateStr}')">+ Add Event</button>
      </div>

      <!-- Events -->
      <h5 style="font-size: 13px; font-weight: 700; margin: 12px 0 6px 0;">Scheduled Calendar Events (${events.length})</h5>
      ${events.length > 0 ? events.map(e => `
        <div class="flex items-center justify-between p-2 mb-2" style="background: var(--bg-input); border-radius: var(--radius-sm);">
          <div>
            <strong>${escapeHtml(e.title)}</strong>
            <div class="text-xs text-muted">⏰ ${e.time || 'All day'} • 📍 ${escapeHtml(e.room || 'N/A')}</div>
          </div>
          <div class="flex items-center gap-1">
            <span class="badge ${e.type === 'Exam' ? 'badge-rose' : 'badge-amber'}">${e.type}</span>
            <button class="btn btn-icon btn-sm btn-danger" onclick="deleteCalendarEvent('${e.id}'); closeModal();">${getIconHtml('trash')}</button>
          </div>
        </div>
      `).join('') : '<div class="text-xs text-muted mb-2">No exams or events on this date.</div>'}

      <!-- Tasks -->
      <h5 style="font-size: 13px; font-weight: 700; margin: 12px 0 6px 0;">Tasks Due (${tasks.length})</h5>
      ${tasks.length > 0 ? tasks.map(t => `
        <div class="flex items-center justify-between p-2 mb-2" style="background: var(--bg-input); border-radius: var(--radius-sm);">
          <div style="${t.completed ? 'text-decoration: line-through; opacity: 0.6;' : ''}">${escapeHtml(t.title)}</div>
          <span class="badge ${t.completed ? 'badge-emerald' : 'badge-amber'}">${t.completed ? 'Done' : 'Pending'}</span>
        </div>
      `).join('') : '<div class="text-xs text-muted mb-2">No tasks due today.</div>'}

      <!-- Goals -->
      <h5 style="font-size: 13px; font-weight: 700; margin: 12px 0 6px 0;">Goal Deadlines (${goals.length})</h5>
      ${goals.length > 0 ? goals.map(g => `
        <div class="flex items-center justify-between p-2 mb-2" style="background: var(--bg-input); border-radius: var(--radius-sm);">
          <div>🎯 <strong>${escapeHtml(g.title)}</strong></div>
          <span class="badge badge-indigo">${g.progress}%</span>
        </div>
      `).join('') : '<div class="text-xs text-muted mb-2">No major goal milestones today.</div>'}
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Close</button>
    `
  });
}

function openCalendarEventModal(id = null, defaultDate = null) {
  const ev = id ? currentData.calendarEvents.find(e => e.id === id) : null;
  const isEdit = !!ev;

  openModal({
    title: isEdit ? 'Edit Calendar Event' : 'Add Calendar Event',
    body: `
      <form id="cal-event-form" onsubmit="handleCalendarEventSubmit(event, '${id || ''}')">
        <div class="form-group">
          <label>Event / Exam Title *</label>
          <input type="text" class="form-control" id="ev-title" required value="${escapeHtml(ev ? ev.title : '')}" placeholder="e.g., OS Midterm Examination">
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Event Type</label>
            <select class="form-control" id="ev-type">
              <option value="Exam" ${ev && ev.type === 'Exam' ? 'selected' : ''}>Examination / Test</option>
              <option value="Assignment" ${ev && ev.type === 'Assignment' ? 'selected' : ''}>Assignment Due</option>
              <option value="Event" ${!ev || ev.type === 'Event' ? 'selected' : ''}>General Event / Meeting</option>
              <option value="Milestone" ${ev && ev.type === 'Milestone' ? 'selected' : ''}>Study Milestone</option>
            </select>
          </div>
          <div class="form-group">
            <label>Date *</label>
            <input type="date" class="form-control" id="ev-date" required value="${ev ? ev.date : (defaultDate || new Date().toISOString().split('T')[0])}">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Time</label>
            <input type="time" class="form-control" id="ev-time" value="${ev ? ev.time || '' : '10:00'}">
          </div>
          <div class="form-group">
            <label>Location / Room</label>
            <input type="text" class="form-control" id="ev-room" value="${escapeHtml(ev ? ev.room || '' : '')}" placeholder="e.g., Hall A">
          </div>
        </div>
        <div class="form-group">
          <label>Notes</label>
          <textarea class="form-control" id="ev-notes" placeholder="Syllabus coverage or instructions...">${escapeHtml(ev ? ev.notes || '' : '')}</textarea>
        </div>
      </form>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="document.getElementById('cal-event-form').requestSubmit()">${isEdit ? 'Save Event' : 'Add Event'}</button>
    `
  });
}

function handleCalendarEventSubmit(e, editId) {
  e.preventDefault();
  const title = document.getElementById('ev-title').value.trim();
  if (!title) return;

  const type = document.getElementById('ev-type').value;
  const date = document.getElementById('ev-date').value;
  const time = document.getElementById('ev-time').value;
  const room = document.getElementById('ev-room').value.trim();
  const notes = document.getElementById('ev-notes').value.trim();

  if (editId) {
    const ev = currentData.calendarEvents.find(item => item.id === editId);
    if (ev) {
      ev.title = title;
      ev.type = type;
      ev.date = date;
      ev.time = time;
      ev.room = room;
      ev.notes = notes;
      logActivity(`Edited event: "${title}"`);
    }
  } else {
    const newEvent = {
      id: 'ce-' + Date.now(),
      title,
      type,
      date,
      time,
      room,
      notes
    };
    currentData.calendarEvents.push(newEvent);
    logActivity(`Added event: "${title}" on ${date}`);
  }

  saveStorage();
  closeModal();
  renderCalendar();
  showToast(editId ? 'Event updated!' : 'Event scheduled!');
}

function deleteCalendarEvent(id) {
  const idx = currentData.calendarEvents.findIndex(e => e.id === id);
  if (idx < 0) return;
  const deleted = currentData.calendarEvents[idx];
  currentData.calendarEvents.splice(idx, 1);
  saveStorage();
  renderCalendar();
  showToast(`Event "${deleted.title}" deleted.`);
}

/* =========================================================================
   PLANNER VIEW (Daily & Weekly)
   ========================================================================= */

let plannerTab = 'daily';
let plannerSelectedDate = new Date().toISOString().split('T')[0];

function renderPlanner() {
  const container = document.getElementById('planner-content-container');
  if (!container) return;

  if (plannerTab === 'daily') {
    renderDailyPlanner(container);
  } else {
    renderWeeklyPlanner(container);
  }
}

function switchPlannerTab(tab) {
  plannerTab = tab;
  const btnDaily = document.getElementById('btn-planner-daily');
  const btnWeekly = document.getElementById('btn-planner-weekly');
  if (btnDaily) btnDaily.classList.toggle('btn-primary', tab === 'daily');
  if (btnDaily) btnDaily.classList.toggle('btn-secondary', tab !== 'daily');
  if (btnWeekly) btnWeekly.classList.toggle('btn-primary', tab === 'weekly');
  if (btnWeekly) btnWeekly.classList.toggle('btn-secondary', tab !== 'weekly');
  renderPlanner();
}

function renderDailyPlanner(container) {
  const dateStr = plannerSelectedDate;
  const dateObj = new Date(dateStr + 'T00:00:00');
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const dayName = days[dateObj.getDay()];

  // Today's classes
  const classes = (currentData.timetableClasses || []).filter(c => c.day === dayName);
  // Today's tasks
  const tasks = (currentData.tasks || []).filter(t => t.dueDate === dateStr);
  // Today's habits
  const habits = currentData.habits || [];
  // Today's daily reflections note
  const currentReflection = (currentData.dailyNotes && currentData.dailyNotes[dateStr]) || '';

  container.innerHTML = `
    <div class="card mb-4" style="margin-bottom: 20px;">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <div class="flex items-center gap-2">
          <button class="btn btn-sm btn-secondary" onclick="shiftPlannerDay(-1)">&larr; Prev Day</button>
          <button class="btn btn-sm btn-secondary" onclick="setPlannerToday()">Today</button>
          <button class="btn btn-sm btn-secondary" onclick="shiftPlannerDay(1)">Next Day &rarr;</button>
          <h2 style="font-size: 16px; font-weight: 700; margin-left: 8px;">
            ${dateObj.toLocaleDateString([], { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })}
          </h2>
        </div>
        <input type="date" class="form-control" style="width: auto;" value="${dateStr}" onchange="changePlannerDate(this.value)">
      </div>
    </div>

    <div class="dashboard-grid">
      <!-- Timetable Classes -->
      <div class="card col-6">
        <div class="card-header">
          <h3 class="card-title">
            <span class="icon-slot" data-icon="table"></span>
            <span>Classes for ${dayName} (${classes.length})</span>
          </h3>
          <button class="btn btn-sm btn-secondary" onclick="navigateTo('timetable')">Edit Grid</button>
        </div>
        <div>
          ${classes.length > 0 ? classes.map(c => `
            <div class="flex items-center justify-between p-2 mb-2" style="background: var(--bg-input); border-radius: var(--radius-sm); border-left: 4px solid ${c.color || 'var(--accent)'}; padding: 8px 12px; margin-bottom: 8px;">
              <div>
                <strong>${escapeHtml(c.subjectName)}</strong>
                <div class="text-xs text-muted">👨‍🏫 ${escapeHtml(c.teacherName || '')} • 📍 Room ${escapeHtml(c.room || 'TBD')}</div>
              </div>
              <span class="badge badge-indigo">Scheduled</span>
            </div>
          `).join('') : `<div class="text-sm text-muted p-3 text-center">No scheduled lectures on ${dayName}.</div>`}
        </div>
      </div>

      <!-- Actionable Tasks for Date -->
      <div class="card col-6">
        <div class="card-header">
          <h3 class="card-title">
            <span class="icon-slot" data-icon="check-square"></span>
            <span>Tasks Due (${tasks.length})</span>
          </h3>
          <button class="btn btn-sm btn-primary" onclick="openTaskModal()">+ Add Task</button>
        </div>
        <div>
          ${tasks.length > 0 ? tasks.map(t => `
            <div class="flex items-center justify-between p-2 mb-2" style="border-bottom: 1px solid var(--border);">
              <label class="checkbox-label">
                <input type="checkbox" ${t.completed ? 'checked' : ''} onchange="toggleTaskComplete('${t.id}'); renderPlanner();">
                <span style="${t.completed ? 'text-decoration: line-through; opacity: 0.6;' : ''}; font-weight: 500;">${escapeHtml(t.title)}</span>
              </label>
              <span class="badge ${t.priority === 'High' ? 'badge-amber' : 'badge-gray'}">${t.priority}</span>
            </div>
          `).join('') : `<div class="text-sm text-muted p-3 text-center">No tasks scheduled for this day.</div>`}
        </div>
      </div>

      <!-- Habit Check-ins -->
      <div class="card col-6">
        <div class="card-header">
          <h3 class="card-title">
            <span class="icon-slot" data-icon="flame"></span>
            <span>Habits Check-in</span>
          </h3>
          <button class="btn btn-sm btn-secondary" onclick="navigateTo('habits')">Manage</button>
        </div>
        <div>
          ${habits.map(h => `
            <div class="flex items-center justify-between p-2 mb-2" style="border-bottom: 1px solid var(--border);">
              <label class="checkbox-label">
                <input type="checkbox" ${h.completedToday ? 'checked' : ''} onchange="toggleHabitToday('${h.id}'); renderPlanner();">
                <span style="font-weight: 600;">${escapeHtml(h.name)}</span>
              </label>
              <span class="badge badge-amber">🔥 ${h.streak}d</span>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- Daily Reflection & Notes -->
      <div class="card col-6">
        <div class="card-header">
          <h3 class="card-title">
            <span class="icon-slot" data-icon="file-text"></span>
            <span>Daily Reflections & Notes</span>
          </h3>
          <span class="badge badge-indigo">Auto-saved</span>
        </div>
        <textarea class="form-control" rows="5" placeholder="Write key takeaways, what went well, and study challenges today..." oninput="saveDailyReflection(this.value)">${escapeHtml(currentReflection)}</textarea>
      </div>
    </div>
  `;
}

function shiftPlannerDay(delta) {
  const d = new Date(plannerSelectedDate + 'T00:00:00');
  d.setDate(d.getDate() + delta);
  plannerSelectedDate = d.toISOString().split('T')[0];
  renderPlanner();
}

function setPlannerToday() {
  plannerSelectedDate = new Date().toISOString().split('T')[0];
  renderPlanner();
}

function changePlannerDate(val) {
  if (val) {
    plannerSelectedDate = val;
    renderPlanner();
  }
}

function saveDailyReflection(text) {
  if (!currentData.dailyNotes) currentData.dailyNotes = {};
  currentData.dailyNotes[plannerSelectedDate] = text;
  saveStorage();
}

function renderWeeklyPlanner(container) {
  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  container.innerHTML = `
    <div class="dashboard-grid">
      ${days.map(d => {
        const classes = (currentData.timetableClasses || []).filter(c => c.day === d);
        return `
          <div class="card col-4">
            <h4 style="font-size: 15px; font-weight: 700; border-bottom: 2px solid var(--accent); padding-bottom: 6px; margin-bottom: 10px;">${d}</h4>
            <div class="text-xs font-semibold text-muted mb-2">Classes (${classes.length}):</div>
            ${classes.length > 0 ? classes.map(c => `
              <div class="p-1 mb-1 text-xs" style="background: var(--bg-input); border-radius: var(--radius-sm); border-left: 3px solid ${c.color || 'var(--accent)'};">
                <strong>${escapeHtml(c.subjectName)}</strong> (${escapeHtml(c.room || 'TBD')})
              </div>
            `).join('') : '<div class="text-xs text-muted">No classes scheduled</div>'}
          </div>
        `;
      }).join('')}
    </div>
  `;
}

/* =========================================================================
   GENERAL NOTES & STICKY NOTES
   ========================================================================= */

let notesSubjectFilter = 'all';
let notesSearchQuery = '';

function renderNotes() {
  const container = document.getElementById('notes-cards-container');
  const sel = document.getElementById('notes-subject-filter');
  if (!container) return;

  if (sel) {
    sel.innerHTML = `<option value="all">All Subjects</option>` +
      currentData.subjects.map(s => `<option value="${s.id}" ${notesSubjectFilter === s.id ? 'selected' : ''}>${escapeHtml(s.name)}</option>`).join('');
  }

  let filtered = [...currentData.notes];
  if (notesSubjectFilter !== 'all') filtered = filtered.filter(n => n.subjectId === notesSubjectFilter);
  if (notesSearchQuery) {
    const q = notesSearchQuery.toLowerCase();
    filtered = filtered.filter(n => n.title.toLowerCase().includes(q) || (n.content && n.content.toLowerCase().includes(q)));
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="col-12 card" style="text-align: center; padding: 40px;">
        <div style="font-size: 36px; margin-bottom: 8px;">📝</div>
        <h3 style="font-size: 16px; font-weight: 700;">No notes found</h3>
        <p class="text-sm text-muted">Create in-depth study docs, formulas, and topic takeaways.</p>
        <button class="btn btn-primary btn-sm mt-3" style="margin-top: 12px;" onclick="openNoteModal()">+ Create Note</button>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(n => {
    const subject = currentData.subjects.find(s => s.id === n.subjectId);
    return `
      <div class="card col-6">
        <div class="card-header">
          <div>
            <h3 class="card-title" style="font-size: 15px;">${escapeHtml(n.title)}</h3>
            <div class="text-xs text-muted mt-1">
              ${subject ? `<span class="badge" style="background:${subject.color}22; color:${subject.color}; font-weight:600;">${escapeHtml(subject.name)}</span>` : ''}
              <span>📅 ${n.date || 'Recent'}</span>
            </div>
          </div>
          <div class="flex items-center gap-1">
            <button class="btn btn-icon btn-sm btn-secondary" onclick="openNoteModal('${n.id}')">${getIconHtml('edit')}</button>
            <button class="btn btn-icon btn-sm btn-danger" onclick="deleteNote('${n.id}')">${getIconHtml('trash')}</button>
          </div>
        </div>
        <div class="text-sm text-secondary" style="white-space: pre-wrap; max-height: 180px; overflow-y: auto; line-height: 1.5; margin-bottom: 10px;">
          ${escapeHtml(n.content)}
        </div>
        ${n.tags && n.tags.length > 0 ? `
          <div class="flex items-center gap-1 flex-wrap mt-2">
            ${n.tags.map(t => `<span class="badge badge-gray">#${escapeHtml(t)}</span>`).join('')}
          </div>
        ` : ''}
      </div>
    `;
  }).join('');
}

function filterNotesBySubject(val) {
  notesSubjectFilter = val;
  renderNotes();
}

function searchNotes(val) {
  notesSearchQuery = val;
  renderNotes();
}

function openNoteModal(id = null) {
  const note = id ? currentData.notes.find(n => n.id === id) : null;
  const isEdit = !!note;

  const subjectOptions = currentData.subjects.map(s => `
    <option value="${s.id}" ${note && note.subjectId === s.id ? 'selected' : ''}>${escapeHtml(s.name)}</option>
  `).join('');

  openModal({
    title: isEdit ? 'Edit Study Note' : 'Create Study Note',
    body: `
      <form id="note-form" onsubmit="handleNoteFormSubmit(event, '${id || ''}')">
        <div class="form-group">
          <label>Note Title *</label>
          <input type="text" class="form-control" id="note-title" required value="${escapeHtml(note ? note.title : '')}" placeholder="e.g., Multilevel Feedback Queue Summary">
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Linked Subject</label>
            <select class="form-control" id="note-subject">
              <option value="">-- General Note (None) --</option>
              ${subjectOptions}
            </select>
          </div>
          <div class="form-group">
            <label>Tags (comma-separated)</label>
            <input type="text" class="form-control" id="note-tags" value="${escapeHtml(note && note.tags ? note.tags.join(', ') : '')}" placeholder="os, cpu, exam">
          </div>
        </div>
        <div class="form-group">
          <label>Note Content *</label>
          <textarea class="form-control" id="note-content" rows="8" required placeholder="Type lecture takeaways, formulas, bullet points...">${escapeHtml(note ? note.content : '')}</textarea>
        </div>
      </form>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="document.getElementById('note-form').requestSubmit()">${isEdit ? 'Save Changes' : 'Create Note'}</button>
    `
  });
}

function handleNoteFormSubmit(e, editId) {
  e.preventDefault();
  const title = document.getElementById('note-title').value.trim();
  if (!title) return;

  const subjectId = document.getElementById('note-subject').value;
  const tags = document.getElementById('note-tags').value.split(',').map(t => t.trim()).filter(Boolean);
  const content = document.getElementById('note-content').value.trim();

  if (editId) {
    const n = currentData.notes.find(item => item.id === editId);
    if (n) {
      n.title = title;
      n.subjectId = subjectId;
      n.tags = tags;
      n.content = content;
      logActivity(`Edited note: "${title}"`);
    }
  } else {
    const newNote = {
      id: 'n-' + Date.now(),
      title,
      subjectId,
      tags,
      content,
      date: new Date().toISOString().split('T')[0]
    };
    currentData.notes.unshift(newNote);
    logActivity(`Created note: "${title}"`);
  }

  saveStorage();
  closeModal();
  renderNotes();
  showToast(editId ? 'Note updated!' : 'Note created!');
}

function deleteNote(id) {
  const idx = currentData.notes.findIndex(n => n.id === id);
  if (idx < 0) return;
  const deleted = currentData.notes[idx];
  const prevNotes = [...currentData.notes];

  currentData.notes.splice(idx, 1);
  saveStorage();
  renderNotes();
  logActivity(`Deleted note: "${deleted.title}"`);

  showToast(`Note "${deleted.title}" deleted.`, () => {
    currentData.notes = prevNotes;
    saveStorage();
    renderNotes();
    logActivity(`Undid deletion of note: "${deleted.title}"`);
  });
}

/* STICKY NOTES */
let stickyColorFilter = 'all';
let stickySearchQuery = '';

function renderStickies() {
  const container = document.getElementById('stickies-container');
  if (!container) return;

  let filtered = currentData.stickyNotes.filter(s => !s.archived);
  if (stickyColorFilter !== 'all') filtered = filtered.filter(s => s.color === stickyColorFilter);
  if (stickySearchQuery) {
    const q = stickySearchQuery.toLowerCase();
    filtered = filtered.filter(s => s.title.toLowerCase().includes(q) || s.content.toLowerCase().includes(q));
  }

  // Pinned first
  filtered.sort((a, b) => (b.pinned ? 1 : 0) - (a.pinned ? 1 : 0));

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 40px;" class="card">
        <div style="font-size: 36px; margin-bottom: 8px;">📌</div>
        <h3 style="font-size: 16px; font-weight: 700;">Sticky Wall Empty</h3>
        <p class="text-sm text-muted">Jot down quick reminders, formulas, and flashcards.</p>
        <button class="btn btn-primary btn-sm mt-3" style="margin-top: 12px;" onclick="openStickyModal()">+ Add Sticky Note</button>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(s => `
    <div class="sticky-note-card sticky-${s.color}">
      <div class="sticky-header">
        <div class="flex items-center gap-1">
          <button class="btn btn-icon btn-sm btn-secondary" onclick="toggleStickyPin('${s.id}')" title="Pin to top">
            <span style="color: ${s.pinned ? '#b45309' : 'inherit'}; font-size: 12px;">📌</span>
          </button>
          <div class="sticky-title">${escapeHtml(s.title)}</div>
        </div>
        <div class="flex items-center gap-1">
          <button class="btn btn-icon btn-sm btn-secondary" onclick="openStickyModal('${s.id}')">${getIconHtml('edit')}</button>
          <button class="btn btn-icon btn-sm btn-danger" onclick="deleteSticky('${s.id}')">${getIconHtml('trash')}</button>
        </div>
      </div>
      <div class="sticky-content">${escapeHtml(s.content)}</div>
      <div class="sticky-footer">
        <span>${s.priority || 'Normal'} Priority</span>
        <div class="flex items-center gap-1">
          <span style="width: 10px; height: 10px; border-radius: 50%; display: inline-block; background: currentColor;"></span>
        </div>
      </div>
    </div>
  `).join('');
}

function filterStickies(color) {
  stickyColorFilter = color;
  renderStickies();
}

function searchStickies(val) {
  stickySearchQuery = val;
  renderStickies();
}

function toggleStickyPin(id) {
  const s = currentData.stickyNotes.find(item => item.id === id);
  if (!s) return;
  s.pinned = !s.pinned;
  saveStorage();
  renderStickies();
  renderDashboard();
}

function openStickyModal(id = null) {
  const s = id ? currentData.stickyNotes.find(item => item.id === id) : null;
  const isEdit = !!s;

  openModal({
    title: isEdit ? 'Edit Sticky Note' : 'New Sticky Note',
    body: `
      <form id="sticky-form" onsubmit="handleStickyFormSubmit(event, '${id || ''}')">
        <div class="form-group">
          <label>Sticky Title</label>
          <input type="text" class="form-control" id="sn-title" value="${escapeHtml(s ? s.title : '')}" placeholder="Quick reminder, formula...">
        </div>
        <div class="form-group">
          <label>Color Theme</label>
          <div class="flex items-center gap-2">
            <label><input type="radio" name="sn-color" value="yellow" ${!s || s.color === 'yellow' ? 'checked' : ''}> Yellow</label>
            <label><input type="radio" name="sn-color" value="cyan" ${s && s.color === 'cyan' ? 'checked' : ''}> Cyan</label>
            <label><input type="radio" name="sn-color" value="lime" ${s && s.color === 'lime' ? 'checked' : ''}> Lime</label>
            <label><input type="radio" name="sn-color" value="coral" ${s && s.color === 'coral' ? 'checked' : ''}> Coral</label>
            <label><input type="radio" name="sn-color" value="lavender" ${s && s.color === 'lavender' ? 'checked' : ''}> Lavender</label>
          </div>
        </div>
        <div class="form-group">
          <label>Content *</label>
          <textarea class="form-control" id="sn-content" rows="5" required placeholder="Write your note here...">${escapeHtml(s ? s.content : '')}</textarea>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Priority</label>
            <select class="form-control" id="sn-priority">
              <option value="Low" ${s && s.priority === 'Low' ? 'selected' : ''}>Low</option>
              <option value="Medium" ${!s || s.priority === 'Medium' ? 'selected' : ''}>Medium</option>
              <option value="High" ${s && s.priority === 'High' ? 'selected' : ''}>High</option>
            </select>
          </div>
          <div class="form-group">
            <label class="checkbox-label" style="margin-top: 26px;">
              <input type="checkbox" id="sn-pinned" ${s && s.pinned ? 'checked' : ''}>
              <span>Pin to top</span>
            </label>
          </div>
        </div>
      </form>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="document.getElementById('sticky-form').requestSubmit()">${isEdit ? 'Save Sticky' : 'Create Sticky'}</button>
    `
  });
}

function handleStickyFormSubmit(e, editId) {
  e.preventDefault();
  const title = document.getElementById('sn-title').value.trim() || 'Sticky Note';
  const content = document.getElementById('sn-content').value.trim();
  if (!content) return;

  const color = document.querySelector('input[name="sn-color"]:checked').value;
  const priority = document.getElementById('sn-priority').value;
  const pinned = document.getElementById('sn-pinned').checked;

  if (editId) {
    const s = currentData.stickyNotes.find(item => item.id === editId);
    if (s) {
      s.title = title;
      s.content = content;
      s.color = color;
      s.priority = priority;
      s.pinned = pinned;
      logActivity(`Edited sticky: "${title}"`);
    }
  } else {
    const newSticky = {
      id: 'sn-' + Date.now(),
      title,
      content,
      color,
      priority,
      pinned,
      archived: false,
      created: new Date().toISOString()
    };
    currentData.stickyNotes.unshift(newSticky);
    logActivity(`Created sticky: "${title}"`);
  }

  saveStorage();
  closeModal();
  renderStickies();
  renderDashboard();
  showToast(editId ? 'Sticky updated!' : 'Sticky created!');
}

function deleteSticky(id) {
  const idx = currentData.stickyNotes.findIndex(s => s.id === id);
  if (idx < 0) return;
  const deleted = currentData.stickyNotes[idx];
  const prev = [...currentData.stickyNotes];

  currentData.stickyNotes.splice(idx, 1);
  saveStorage();
  renderStickies();
  renderDashboard();
  logActivity(`Deleted sticky: "${deleted.title}"`);

  showToast(`Sticky "${deleted.title}" deleted.`, () => {
    currentData.stickyNotes = prev;
    saveStorage();
    renderStickies();
    renderDashboard();
    logActivity(`Undid deletion of sticky: "${deleted.title}"`);
  });
}

/* =========================================================================
   PLAYLISTS & VIDEO MANAGER
   ========================================================================= */

function renderPlaylists() {
  const container = document.getElementById('playlists-main-container');
  if (!container) return;

  if (currentData.playlists.length === 0) {
    container.innerHTML = `
      <div class="card" style="text-align: center; padding: 40px;">
        <div style="font-size: 36px; margin-bottom: 8px;">🎥</div>
        <h3 style="font-size: 16px; font-weight: 700;">No video playlists created</h3>
        <p class="text-sm text-muted">Organize course video series, tutorials with custom titles and watch progress.</p>
        <button class="btn btn-primary btn-sm mt-3" style="margin-top: 12px;" onclick="openPlaylistModal()">+ New Playlist</button>
      </div>
    `;
    return;
  }

  container.innerHTML = currentData.playlists.map(pl => {
    const playlistVideos = currentData.videos.filter(v => v.playlistId === pl.id);
    const completedCount = playlistVideos.filter(v => v.completed).length;

    return `
      <div class="card mb-4" style="margin-bottom: 24px; border-top: 4px solid ${pl.color || 'var(--accent)'};">
        <div class="card-header">
          <div>
            <div class="flex items-center gap-2">
              <h3 class="card-title" style="font-size: 16px;">${escapeHtml(pl.name)}</h3>
              <span class="badge badge-indigo">${completedCount}/${playlistVideos.length} Completed</span>
            </div>
            <p class="text-xs text-muted mt-1">${escapeHtml(pl.description || '')}</p>
          </div>
          <div class="flex items-center gap-1">
            <button class="btn btn-sm btn-primary" onclick="openVideoModal(null, '${pl.id}')">+ Add Video</button>
            <button class="btn btn-icon btn-sm btn-secondary" onclick="openPlaylistModal('${pl.id}')">${getIconHtml('edit')}</button>
            <button class="btn btn-icon btn-sm btn-danger" onclick="deletePlaylist('${pl.id}')">${getIconHtml('trash')}</button>
          </div>
        </div>

        <div class="dashboard-grid mt-3">
          ${playlistVideos.length > 0 ? playlistVideos.map(v => `
            <div class="card col-6" style="background: var(--bg-input);">
              <div class="flex items-center justify-between mb-2">
                <strong style="font-size: 13.5px;">${escapeHtml(v.customTitle)}</strong>
                <span class="badge ${v.completed ? 'badge-emerald' : 'badge-amber'}">${v.completed ? 'Watched' : v.progress + '%'}</span>
              </div>
              <p class="text-xs text-secondary mb-2">${escapeHtml(v.description || '')}</p>
              <div class="flex items-center justify-between text-xs text-muted mb-2">
                <span>⏱ Duration: ${v.duration || 0} mins</span>
                <span>${v.notes ? '📝 Has Notes' : ''}</span>
              </div>
              <div class="progress-bar-wrap mb-3" style="height: 5px; margin-bottom: 10px;">
                <div class="progress-bar-fill" style="width: ${v.progress}%;"></div>
              </div>
              <div class="flex items-center justify-between">
                <button class="btn btn-sm btn-primary" onclick="openVideoPlayerModal('${v.id}')">
                  ${getIconHtml('play')}
                  <span>Watch / Player</span>
                </button>
                <div class="flex items-center gap-1">
                  <button class="btn btn-icon btn-sm btn-secondary" onclick="openVideoModal('${v.id}')">${getIconHtml('edit')}</button>
                  <button class="btn btn-icon btn-sm btn-danger" onclick="deleteVideo('${v.id}')">${getIconHtml('trash')}</button>
                </div>
              </div>
            </div>
          `).join('') : '<div class="col-12 text-sm text-muted p-3 text-center">No videos in this playlist yet. Add tutorials to track watch progress!</div>'}
        </div>
      </div>
    `;
  }).join('');
}

function openPlaylistModal(id = null) {
  const pl = id ? currentData.playlists.find(p => p.id === id) : null;
  const isEdit = !!pl;

  openModal({
    title: isEdit ? 'Edit Playlist' : 'New Video Playlist',
    body: `
      <form id="pl-form" onsubmit="handlePlaylistSubmit(event, '${id || ''}')">
        <div class="form-group">
          <label>Playlist Name *</label>
          <input type="text" class="form-control" id="pl-name" required value="${escapeHtml(pl ? pl.name : '')}" placeholder="e.g., Operating Systems Full Course">
        </div>
        <div class="form-group">
          <label>Color Accent</label>
          <input type="color" class="form-control" id="pl-color" value="${pl ? pl.color || '#4f46e5' : '#4f46e5'}" style="height: 38px; padding: 2px;">
        </div>
        <div class="form-group">
          <label>Description</label>
          <textarea class="form-control" id="pl-desc" placeholder="Playlist purpose and overview...">${escapeHtml(pl ? pl.description : '')}</textarea>
        </div>
      </form>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="document.getElementById('pl-form').requestSubmit()">${isEdit ? 'Save Playlist' : 'Create Playlist'}</button>
    `
  });
}

function handlePlaylistSubmit(e, editId) {
  e.preventDefault();
  const name = document.getElementById('pl-name').value.trim();
  if (!name) return;
  const color = document.getElementById('pl-color').value;
  const desc = document.getElementById('pl-desc').value.trim();

  if (editId) {
    const pl = currentData.playlists.find(p => p.id === editId);
    if (pl) {
      pl.name = name;
      pl.color = color;
      pl.description = desc;
      logActivity(`Edited playlist: "${name}"`);
    }
  } else {
    const newPl = {
      id: 'pl-' + Date.now(),
      name,
      color,
      description: desc
    };
    currentData.playlists.push(newPl);
    logActivity(`Created playlist: "${name}"`);
  }

  saveStorage();
  closeModal();
  renderPlaylists();
  showToast(editId ? 'Playlist updated!' : 'Playlist created!');
}

function deletePlaylist(id) {
  const idx = currentData.playlists.findIndex(p => p.id === id);
  if (idx < 0) return;
  const deleted = currentData.playlists[idx];
  currentData.playlists.splice(idx, 1);
  saveStorage();
  renderPlaylists();
  showToast(`Playlist "${deleted.name}" deleted.`);
}

function openVideoModal(id = null, defaultPlaylistId = null) {
  const v = id ? currentData.videos.find(item => item.id === id) : null;
  const isEdit = !!v;

  const plOptions = currentData.playlists.map(pl => `
    <option value="${pl.id}" ${(v && v.playlistId === pl.id) || (!v && defaultPlaylistId === pl.id) ? 'selected' : ''}>${escapeHtml(pl.name)}</option>
  `).join('');

  openModal({
    title: isEdit ? 'Edit Video' : 'Add Learning Video',
    body: `
      <form id="vid-form" onsubmit="handleVideoSubmit(event, '${id || ''}')">
        <div class="form-group">
          <label>Playlist</label>
          <select class="form-control" id="vid-pl">
            ${plOptions}
          </select>
        </div>
        <div class="form-group">
          <label>Custom Video Title *</label>
          <input type="text" class="form-control" id="vid-title" required value="${escapeHtml(v ? v.customTitle : '')}" placeholder="e.g., Lecture 4: CPU Scheduling Algorithms">
        </div>
        <div class="form-group">
          <label>Video URL (YouTube or Web URL)</label>
          <input type="url" class="form-control" id="vid-url" value="${escapeHtml(v ? v.url || '' : '')}" placeholder="https://www.youtube.com/watch?v=...">
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Duration (Minutes)</label>
            <input type="number" class="form-control" id="vid-dur" min="1" value="${v ? v.duration || 30 : 30}">
          </div>
          <div class="form-group">
            <label>Watch Progress (%)</label>
            <input type="number" class="form-control" id="vid-prog" min="0" max="100" value="${v ? v.progress || 0 : 0}">
          </div>
        </div>
        <div class="form-group">
          <label>Overview & Notes</label>
          <textarea class="form-control" id="vid-desc" placeholder="Important timestamps and takeaways...">${escapeHtml(v ? v.description || '' : '')}</textarea>
        </div>
      </form>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="document.getElementById('vid-form').requestSubmit()">${isEdit ? 'Save Video' : 'Add Video'}</button>
    `
  });
}

function handleVideoSubmit(e, editId) {
  e.preventDefault();
  const customTitle = document.getElementById('vid-title').value.trim();
  if (!customTitle) return;

  const playlistId = document.getElementById('vid-pl').value;
  const url = document.getElementById('vid-url').value.trim();
  const duration = parseInt(document.getElementById('vid-dur').value) || 0;
  const progress = parseInt(document.getElementById('vid-prog').value) || 0;
  const description = document.getElementById('vid-desc').value.trim();

  if (editId) {
    const v = currentData.videos.find(item => item.id === editId);
    if (v) {
      v.customTitle = customTitle;
      v.playlistId = playlistId;
      v.url = url;
      v.duration = duration;
      v.progress = progress;
      v.completed = progress >= 100;
      v.description = description;
      logActivity(`Edited video: "${customTitle}"`);
    }
  } else {
    const newVideo = {
      id: 'vid-' + Date.now(),
      playlistId,
      customTitle,
      url,
      duration,
      progress,
      completed: progress >= 100,
      description
    };
    currentData.videos.push(newVideo);
    logActivity(`Added video: "${customTitle}"`);
  }

  saveStorage();
  closeModal();
  renderPlaylists();
  renderDashboard();
  showToast(editId ? 'Video updated!' : 'Video added!');
}

function deleteVideo(id) {
  const idx = currentData.videos.findIndex(v => v.id === id);
  if (idx < 0) return;
  const deleted = currentData.videos[idx];
  currentData.videos.splice(idx, 1);
  saveStorage();
  renderPlaylists();
  renderDashboard();
  showToast(`Video "${deleted.customTitle}" deleted.`);
}

function openVideoPlayerModal(videoId) {
  const v = currentData.videos.find(item => item.id === videoId);
  if (!v) return;

  // Check if YouTube URL to create embed
  let embedHtml = '';
  const ytMatch = v.url && v.url.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([\w-]{11})/);
  if (ytMatch && ytMatch[1]) {
    embedHtml = `
      <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: var(--radius-sm); margin-bottom: 14px;">
        <iframe src="https://www.youtube.com/embed/${ytMatch[1]}" style="position: absolute; top:0; left: 0; width: 100%; height: 100%; border:0;" allowfullscreen></iframe>
      </div>
    `;
  } else if (v.url) {
    embedHtml = `
      <div class="p-4 mb-3 text-center" style="background: var(--bg-input); border-radius: var(--radius-sm);">
        <p class="text-sm mb-2">Direct video link:</p>
        <a href="${escapeHtml(v.url)}" target="_blank" rel="noopener" class="btn btn-primary btn-sm">Open Video in New Tab &rarr;</a>
      </div>
    `;
  }

  openModal({
    title: `Player: ${v.customTitle}`,
    body: `
      ${embedHtml}
      <div class="form-row mb-3">
        <div class="form-group">
          <label>Update Watch Progress (%)</label>
          <input type="range" min="0" max="100" class="form-control" id="player-prog" value="${v.progress}" oninput="document.getElementById('player-prog-val').textContent = this.value + '%'">
          <span class="text-xs font-semibold" id="player-prog-val">${v.progress}%</span>
        </div>
        <div class="form-group">
          <label class="checkbox-label" style="margin-top: 28px;">
            <input type="checkbox" id="player-completed" ${v.completed ? 'checked' : ''}>
            <span>Mark as fully watched</span>
          </label>
        </div>
      </div>
      <div class="form-group">
        <label>Session Notes & Takeaways</label>
        <textarea class="form-control" id="player-notes" rows="4" placeholder="Jot notes while watching...">${escapeHtml(v.notes || '')}</textarea>
      </div>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Close</button>
      <button class="btn btn-primary" onclick="saveVideoProgress('${v.id}')">Save Progress</button>
    `
  });
}

function saveVideoProgress(videoId) {
  const v = currentData.videos.find(item => item.id === videoId);
  if (!v) return;

  const prog = parseInt(document.getElementById('player-prog').value) || 0;
  const completed = document.getElementById('player-completed').checked || prog >= 100;
  const notes = document.getElementById('player-notes').value.trim();

  v.progress = completed ? 100 : prog;
  v.completed = completed;
  v.notes = notes;

  saveStorage();
  closeModal();
  renderPlaylists();
  renderDashboard();
  showToast('Video progress saved!');
}

/* =========================================================================
   HABITS VIEW
   ========================================================================= */

function renderHabits() {
  const container = document.getElementById('habits-list-container');
  const statsContainer = document.getElementById('habits-overall-stats');
  if (!container) return;

  const total = currentData.habits.length;
  const doneToday = currentData.habits.filter(h => h.completedToday).length;

  if (statsContainer) {
    statsContainer.innerHTML = `
      <span class="badge badge-amber" style="font-size: 14px; padding: 6px 12px;">
        🔥 ${doneToday} of ${total} Done Today
      </span>
    `;
  }

  if (total === 0) {
    container.innerHTML = `
      <div class="col-12 card" style="text-align: center; padding: 40px;">
        <div style="font-size: 36px; margin-bottom: 8px;">🔥</div>
        <h3 style="font-size: 16px; font-weight: 700;">No habits registered</h3>
        <p class="text-sm text-muted">Track daily study routines and consistency streaks.</p>
        <button class="btn btn-primary btn-sm mt-3" style="margin-top: 12px;" onclick="openHabitModal()">+ New Habit</button>
      </div>
    `;
    return;
  }

  // Generate last 14 days dates for visual history dots
  const last14Days = [];
  const now = new Date();
  for (let i = 13; i >= 0; i--) {
    const d = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
    last14Days.push(d.toISOString().split('T')[0]);
  }

  container.innerHTML = currentData.habits.map(h => {
    const historySet = new Set(h.history || []);

    return `
      <div class="card col-6">
        <div class="card-header">
          <div>
            <h3 class="card-title" style="font-size: 15px;">${escapeHtml(h.name)}</h3>
            <div class="text-xs text-muted mt-1">${h.category} • ${h.frequency}</div>
          </div>
          <div class="flex items-center gap-2">
            <span class="badge badge-amber" style="font-size: 13px;">🔥 ${h.streak}d Streak</span>
            <button class="btn btn-icon btn-sm btn-secondary" onclick="openHabitModal('${h.id}')">${getIconHtml('edit')}</button>
            <button class="btn btn-icon btn-sm btn-danger" onclick="deleteHabit('${h.id}')">${getIconHtml('trash')}</button>
          </div>
        </div>

        <p class="text-xs text-secondary mb-3">${escapeHtml(h.notes || 'No description.')}</p>

        <!-- 14-day history dots -->
        <div class="mb-3">
          <div class="text-xs text-muted mb-1 font-semibold">14-Day Consistency Track:</div>
          <div class="flex items-center gap-1">
            ${last14Days.map(dateStr => {
              const completedOnDate = historySet.has(dateStr);
              return `
                <div style="width: 16px; height: 16px; border-radius: 4px; background: ${completedOnDate ? 'var(--accent)' : 'var(--bg-input)'}; border: 1px solid var(--border);" title="${dateStr}: ${completedOnDate ? 'Completed' : 'Missed'}"></div>
              `;
            }).join('')}
          </div>
        </div>

        <div class="flex items-center justify-between pt-2" style="border-top: 1px solid var(--border);">
          <span class="text-xs text-muted">Best Streak: ${h.bestStreak || h.streak} days</span>
          <button class="btn btn-sm ${h.completedToday ? 'btn-primary' : 'btn-secondary'}" onclick="toggleHabitToday('${h.id}')">
            ${h.completedToday ? '✓ Done Today' : 'Mark Done Today'}
          </button>
        </div>
      </div>
    `;
  }).join('');
}

function toggleHabitToday(id) {
  const h = currentData.habits.find(item => item.id === id);
  if (!h) return;

  const todayStr = new Date().toISOString().split('T')[0];
  if (!h.history) h.history = [];

  h.completedToday = !h.completedToday;
  if (h.completedToday) {
    if (!h.history.includes(todayStr)) h.history.push(todayStr);
    h.streak = (h.streak || 0) + 1;
    if (h.streak > (h.bestStreak || 0)) h.bestStreak = h.streak;
    logActivity(`Checked habit: "${h.name}" (Streak: ${h.streak}d 🔥)`);
  } else {
    h.history = h.history.filter(d => d !== todayStr);
    h.streak = Math.max(0, (h.streak || 1) - 1);
    logActivity(`Unchecked habit: "${h.name}"`);
  }

  saveStorage();
  renderHabits();
  renderDashboard();
}

function openHabitModal(id = null) {
  const h = id ? currentData.habits.find(item => item.id === id) : null;
  const isEdit = !!h;

  openModal({
    title: isEdit ? 'Edit Habit' : 'New Habit',
    body: `
      <form id="habit-form" onsubmit="handleHabitSubmit(event, '${id || ''}')">
        <div class="form-group">
          <label>Habit Name *</label>
          <input type="text" class="form-control" id="h-name" required value="${escapeHtml(h ? h.name : '')}" placeholder="e.g., 2 DSA Problems Every Morning">
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Category</label>
            <select class="form-control" id="h-cat">
              <option value="Study" ${h && h.category === 'Study' ? 'selected' : ''}>Study & Coding</option>
              <option value="Academics" ${h && h.category === 'Academics' ? 'selected' : ''}>Academics</option>
              <option value="Focus" ${h && h.category === 'Focus' ? 'selected' : ''}>Focus & Timer</option>
              <option value="Health" ${h && h.category === 'Health' ? 'selected' : ''}>Health & Wellbeing</option>
            </select>
          </div>
          <div class="form-group">
            <label>Frequency</label>
            <select class="form-control" id="h-freq">
              <option value="Daily" ${!h || h.frequency === 'Daily' ? 'selected' : ''}>Daily</option>
              <option value="Weekdays" ${h && h.frequency === 'Weekdays' ? 'selected' : ''}>Weekdays</option>
              <option value="Weekly" ${h && h.frequency === 'Weekly' ? 'selected' : ''}>Weekly</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label>Motivation & Notes</label>
          <textarea class="form-control" id="h-notes" placeholder="Why is this habit critical for your semester success?">${escapeHtml(h ? h.notes || '' : '')}</textarea>
        </div>
      </form>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="document.getElementById('habit-form').requestSubmit()">${isEdit ? 'Save Habit' : 'Create Habit'}</button>
    `
  });
}

function handleHabitSubmit(e, editId) {
  e.preventDefault();
  const name = document.getElementById('h-name').value.trim();
  if (!name) return;

  const category = document.getElementById('h-cat').value;
  const frequency = document.getElementById('h-freq').value;
  const notes = document.getElementById('h-notes').value.trim();

  if (editId) {
    const h = currentData.habits.find(item => item.id === editId);
    if (h) {
      h.name = name;
      h.category = category;
      h.frequency = frequency;
      h.notes = notes;
      logActivity(`Edited habit: "${name}"`);
    }
  } else {
    const newHabit = {
      id: 'h-' + Date.now(),
      name,
      category,
      frequency,
      notes,
      streak: 0,
      bestStreak: 0,
      completedToday: false,
      history: []
    };
    currentData.habits.push(newHabit);
    logActivity(`Created habit: "${name}"`);
  }

  saveStorage();
  closeModal();
  renderHabits();
  renderDashboard();
  showToast(editId ? 'Habit updated!' : 'Habit created!');
}

function deleteHabit(id) {
  const idx = currentData.habits.findIndex(h => h.id === id);
  if (idx < 0) return;
  const deleted = currentData.habits[idx];
  currentData.habits.splice(idx, 1);
  saveStorage();
  renderHabits();
  renderDashboard();
  showToast(`Habit "${deleted.name}" deleted.`);
}

/* =========================================================================
   STUDY TIMER & FOCUS MODE
   ========================================================================= */

let timerInterval = null;
let timerMode = 'pomodoro'; // 'pomodoro' (25m), 'shortbreak' (5m), 'longbreak' (15m), 'stopwatch'
let timerSecondsRemaining = 25 * 60;
let timerElapsedSeconds = 0;
let isTimerRunning = false;

function renderTimerView() {
  updateTimerDisplay();
  populateTimerSubjects();
  renderStudySessionsHistory();
}

function populateTimerSubjects() {
  const subSel = document.getElementById('timer-subject-select');
  if (!subSel) return;

  subSel.innerHTML = `<option value="">-- General Study Session --</option>` +
    currentData.subjects.map(s => `<option value="${s.id}">${escapeHtml(s.name)}</option>`).join('');

  updateTimerChapters(subSel.value);
}

function updateTimerChapters(subjectId) {
  const chSel = document.getElementById('timer-chapter-select');
  if (!chSel) return;

  if (!subjectId) {
    chSel.innerHTML = `<option value="">-- General / No Chapter --</option>`;
    return;
  }

  const chapters = currentData.chapters.filter(c => c.subjectId === subjectId);
  chSel.innerHTML = `<option value="">-- Select Chapter --</option>` +
    chapters.map(c => `<option value="${c.id}">Ch ${c.chapterNumber}: ${escapeHtml(c.name)}</option>`).join('');
}

function setTimerMode(mode) {
  pauseTimer();
  timerMode = mode;

  document.querySelectorAll('[id^="timer-mode-"]').forEach(btn => btn.classList.remove('active-timer-mode'));
  const activeBtn = document.getElementById('timer-mode-' + mode);
  if (activeBtn) activeBtn.classList.add('active-timer-mode');

  if (mode === 'pomodoro') timerSecondsRemaining = 25 * 60;
  else if (mode === 'shortbreak') timerSecondsRemaining = 5 * 60;
  else if (mode === 'longbreak') timerSecondsRemaining = 15 * 60;
  else if (mode === 'stopwatch') {
    timerSecondsRemaining = 0;
    timerElapsedSeconds = 0;
  }

  updateTimerDisplay();
}

function updateTimerDisplay() {
  let displayStr = '';
  if (timerMode === 'stopwatch') {
    const mins = Math.floor(timerElapsedSeconds / 60);
    const secs = timerElapsedSeconds % 60;
    displayStr = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  } else {
    const mins = Math.floor(timerSecondsRemaining / 60);
    const secs = timerSecondsRemaining % 60;
    displayStr = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  }

  const timerEl = document.getElementById('study-timer-display');
  const focusEl = document.getElementById('focus-timer-text');
  if (timerEl) timerEl.textContent = displayStr;
  if (focusEl) focusEl.textContent = displayStr;
}

function toggleStudyTimer() {
  if (isTimerRunning) {
    pauseTimer();
  } else {
    startTimer();
  }
}

function startTimer() {
  isTimerRunning = true;
  updateTimerButtons();

  clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    if (timerMode === 'stopwatch') {
      timerElapsedSeconds++;
    } else {
      if (timerSecondsRemaining > 0) {
        timerSecondsRemaining--;
        timerElapsedSeconds++;
      } else {
        // Timer Finished!
        pauseTimer();
        playTimerChime();
        showToast('⏰ Time is up! Great focus session.', null, 'success');
        finishAndLogSession();
      }
    }
    updateTimerDisplay();
  }, 1000);
}

function pauseTimer() {
  isTimerRunning = false;
  clearInterval(timerInterval);
  updateTimerButtons();
}

function resetStudyTimer() {
  pauseTimer();
  setTimerMode(timerMode);
}

function updateTimerButtons() {
  const label = document.getElementById('timer-toggle-label');
  const focusBtn = document.getElementById('focus-timer-btn');
  if (label) label.textContent = isTimerRunning ? 'Pause Session' : 'Start Session';
  if (focusBtn) focusBtn.textContent = isTimerRunning ? 'Pause' : 'Start';
}

function finishAndLogSession() {
  const minsLogged = Math.max(1, Math.round(timerElapsedSeconds / 60));
  const subSel = document.getElementById('timer-subject-select');
  const chSel = document.getElementById('timer-chapter-select');

  const subjectId = subSel ? subSel.value : '';
  const chapterId = chSel ? chSel.value : '';

  const subject = currentData.subjects.find(s => s.id === subjectId);
  const chapter = currentData.chapters.find(c => c.id === chapterId);

  const newSession = {
    id: 'ss-' + Date.now(),
    subjectId: subjectId,
    subjectName: subject ? subject.name : 'General Study',
    chapterName: chapter ? chapter.name : 'General Topics',
    duration: minsLogged,
    mode: timerMode,
    timestamp: new Date().toISOString()
  };

  if (!currentData.studySessions) currentData.studySessions = [];
  currentData.studySessions.unshift(newSession);

  // Update actual hours in chapter
  if (chapter) {
    chapter.actualStudyTime = (chapter.actualStudyTime || 0) + parseFloat((minsLogged / 60).toFixed(1));
  }

  saveStorage();
  logActivity(`Logged study session: ${minsLogged}m on ${newSession.subjectName}`);
  showToast(`Logged ${minsLogged} mins of study!`, null, 'success');

  timerElapsedSeconds = 0;
  resetStudyTimer();
  renderStudySessionsHistory();
  renderDashboard();
}

function renderStudySessionsHistory() {
  const container = document.getElementById('study-sessions-history-list');
  const totalBadge = document.getElementById('total-study-hours-badge');
  if (!container) return;

  const sessions = currentData.studySessions || [];
  const totalMins = sessions.reduce((acc, s) => acc + (s.duration || 0), 0);
  if (totalBadge) totalBadge.textContent = `${(totalMins / 60).toFixed(1)} hrs total`;

  if (sessions.length === 0) {
    container.innerHTML = `<div class="text-sm text-muted p-3 text-center">No study sessions logged yet. Start the timer to record study time!</div>`;
    return;
  }

  container.innerHTML = sessions.map(s => `
    <div class="flex items-center justify-between p-2 mb-2" style="border-bottom: 1px solid var(--border);">
      <div>
        <strong style="font-size: 13px;">${escapeHtml(s.subjectName)}</strong>
        <div class="text-xs text-muted">${escapeHtml(s.chapterName)} • ${new Date(s.timestamp).toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</div>
      </div>
      <span class="badge badge-indigo">${s.duration} mins</span>
    </div>
  `).join('');
}

// Focus Mode
function enterFocusMode() {
  const overlay = document.getElementById('focus-mode-overlay');
  const targetInfo = document.getElementById('focus-target-info');
  if (overlay) overlay.classList.add('active');

  const subSel = document.getElementById('timer-subject-select');
  const opt = subSel && subSel.selectedOptions[0];
  if (targetInfo) {
    targetInfo.textContent = opt && opt.value ? opt.textContent : 'General Deep Work Session';
  }
}

function exitFocusMode() {
  const overlay = document.getElementById('focus-mode-overlay');
  if (overlay) overlay.classList.remove('active');
}

/* =========================================================================
   STATISTICS VIEW (Real Mathematical Calculations & Charts)
   ========================================================================= */

function renderStatistics() {
  const container = document.getElementById('statistics-main-container');
  if (!container) return;

  // Real math calculations
  const totalGoals = currentData.goals.length;
  const completedGoals = currentData.goals.filter(g => g.status === 'Completed').length;
  const goalRate = totalGoals ? Math.round((completedGoals / totalGoals) * 100) : 0;

  const totalTasks = currentData.tasks.length;
  const completedTasks = currentData.tasks.filter(t => t.completed).length;
  const taskRate = totalTasks ? Math.round((completedTasks / totalTasks) * 100) : 0;

  const totalChapters = currentData.chapters.length;
  const completedChapters = currentData.chapters.filter(c => c.status === 'Completed').length;
  const chapterRate = totalChapters ? Math.round((completedChapters / totalChapters) * 100) : 0;

  const totalStudyMins = (currentData.studySessions || []).reduce((acc, s) => acc + (s.duration || 0), 0);
  const totalStudyHours = (totalStudyMins / 60).toFixed(1);

  // Subject-wise study hours breakdown
  const subjectBreakdown = currentData.subjects.map(s => {
    const mins = (currentData.studySessions || [])
      .filter(sess => sess.subjectId === s.id)
      .reduce((acc, sess) => acc + (sess.duration || 0), 0);
    return {
      name: s.name,
      color: s.color,
      hours: (mins / 60).toFixed(1),
      percent: totalStudyMins > 0 ? Math.round((mins / totalStudyMins) * 100) : 0
    };
  });

  container.innerHTML = `
    <!-- Top Analytical Metric Cards -->
    <div class="card col-3">
      <div class="stat-label">Goal Completion Rate</div>
      <div class="stat-value" style="color: var(--accent); font-size: 28px;">${goalRate}%</div>
      <div class="text-xs text-muted mt-1">${completedGoals} of ${totalGoals} Goals Reached</div>
    </div>
    <div class="card col-3">
      <div class="stat-label">Tasks Efficiency</div>
      <div class="stat-value" style="color: var(--success); font-size: 28px;">${taskRate}%</div>
      <div class="text-xs text-muted mt-1">${completedTasks} of ${totalTasks} Tasks Cleared</div>
    </div>
    <div class="card col-3">
      <div class="stat-label">Syllabus Covered</div>
      <div class="stat-value" style="color: var(--warning); font-size: 28px;">${chapterRate}%</div>
      <div class="text-xs text-muted mt-1">${completedChapters} of ${totalChapters} Chapters Finished</div>
    </div>
    <div class="card col-3">
      <div class="stat-label">Total Study Time</div>
      <div class="stat-value" style="color: var(--info); font-size: 28px;">${totalStudyHours} hrs</div>
      <div class="text-xs text-muted mt-1">Logged across all sessions</div>
    </div>

    <!-- Subject Study Distribution -->
    <div class="card col-6">
      <div class="card-header">
        <h3 class="card-title">
          <span class="icon-slot" data-icon="book-open"></span>
          <span>Study Hours Distribution by Subject</span>
        </h3>
      </div>
      <div>
        ${subjectBreakdown.map(sb => `
          <div class="mb-3">
            <div class="flex items-center justify-between text-xs font-semibold mb-1">
              <span>${escapeHtml(sb.name)}</span>
              <span>${sb.hours} hrs (${sb.percent}%)</span>
            </div>
            <div class="progress-bar-wrap" style="height: 7px;">
              <div class="progress-bar-fill" style="width: ${sb.percent}%; background: ${sb.color};"></div>
            </div>
          </div>
        `).join('')}
      </div>
    </div>

    <!-- Habit Streaks Ranking -->
    <div class="card col-6">
      <div class="card-header">
        <h3 class="card-title">
          <span class="icon-slot" data-icon="flame"></span>
          <span>Habit Streaks & Consistency</span>
        </h3>
      </div>
      <div>
        ${currentData.habits.map(h => `
          <div class="flex items-center justify-between p-2 mb-2" style="border-bottom: 1px solid var(--border);">
            <div>
              <strong>${escapeHtml(h.name)}</strong>
              <div class="text-xs text-muted">Category: ${h.category}</div>
            </div>
            <div style="text-align: right;">
              <span class="badge badge-amber" style="font-size: 13px;">🔥 ${h.streak}d Current</span>
              <div class="text-xs text-muted mt-1">Best: ${h.bestStreak || h.streak}d</div>
            </div>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

/* =========================================================================
   SETTINGS & PROFILES MANAGEMENT
   ========================================================================= */

function renderSettings() {
  renderProfilesList();
  renderActivityLog();

  const cardStyleSel = document.getElementById('settings-card-style');
  const densitySel = document.getElementById('settings-density');
  if (cardStyleSel && currentData.settings) cardStyleSel.value = currentData.settings.cardStyle || 'modern';
  if (densitySel && currentData.settings) densitySel.value = currentData.settings.density || 'comfortable';
}

function renderProfilesList() {
  const container = document.getElementById('settings-profiles-list');
  if (!container) return;

  container.innerHTML = appState.profiles.map(p => {
    const isActive = p.id === appState.activeProfileId;
    return `
      <div class="flex items-center justify-between p-2 mb-2" style="background: ${isActive ? 'var(--accent-light)' : 'var(--bg-input)'}; border-radius: var(--radius-sm); border: 1px solid ${isActive ? 'var(--accent)' : 'transparent'};">
        <div class="flex items-center gap-3">
          <div class="profile-avatar" style="width: 32px; height: 32px;">${p.avatar || p.name.charAt(0)}</div>
          <div>
            <strong>${escapeHtml(p.name)}</strong>
            ${isActive ? '<span class="badge badge-indigo" style="margin-left: 6px;">Active Workspace</span>' : ''}
          </div>
        </div>
        <div class="flex items-center gap-2">
          ${!isActive ? `<button class="btn btn-sm btn-secondary" onclick="switchProfile('${p.id}')">Switch</button>` : ''}
          <button class="btn btn-sm btn-danger" onclick="deleteProfile('${p.id}')" ${appState.profiles.length <= 1 ? 'disabled' : ''}>Delete</button>
        </div>
      </div>
    `;
  }).join('');
}

function switchProfile(profileId) {
  if (appState.activeProfileId === profileId) return;
  appState.activeProfileId = profileId;

  if (!appState.profileData[profileId]) {
    appState.profileData[profileId] = getInitialDemoData();
  }
  currentData = appState.profileData[profileId];

  saveStorageImmediate();
  applyThemeAndPreferences();
  navigateTo(currentView);
  showToast(`Switched to workspace profile!`, null, 'success');
}

function openNewProfileModal() {
  openModal({
    title: 'Create New Workspace Profile',
    body: `
      <form id="new-profile-form" onsubmit="handleNewProfileSubmit(event)">
        <div class="form-group">
          <label>Profile Name *</label>
          <input type="text" class="form-control" id="profile-new-name" required placeholder="e.g., Gate Exam 2027 or College Fall">
        </div>
        <div class="form-group">
          <label>Initial Data</label>
          <div class="flex items-center gap-3">
            <label><input type="radio" name="profile-seed" value="demo" checked> Start with Demo Data Template</label>
            <label><input type="radio" name="profile-seed" value="empty"> Start Empty</label>
          </div>
        </div>
      </form>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="document.getElementById('new-profile-form').requestSubmit()">Create Profile</button>
    `
  });
}

function handleNewProfileSubmit(e) {
  e.preventDefault();
  const name = document.getElementById('profile-new-name').value.trim();
  if (!name) return;

  const seed = document.querySelector('input[name="profile-seed"]:checked').value;
  const newId = 'profile-' + Date.now();

  const newProfile = {
    id: newId,
    name,
    avatar: name.charAt(0).toUpperCase(),
    created: new Date().toISOString()
  };

  appState.profiles.push(newProfile);
  if (seed === 'demo') {
    appState.profileData[newId] = getInitialDemoData();
  } else {
    const blank = getInitialDemoData();
    blank.goals = [];
    blank.tasks = [];
    blank.subjects = [];
    blank.chapters = [];
    blank.teachers = [];
    blank.timetableClasses = [];
    blank.stickyNotes = [];
    blank.notes = [];
    blank.videos = [];
    blank.habits = [];
    blank.calendarEvents = [];
    blank.studySessions = [];
    appState.profileData[newId] = blank;
  }

  saveStorageImmediate();
  closeModal();
  switchProfile(newId);
}

function deleteProfile(id) {
  if (appState.profiles.length <= 1) {
    showToast('Cannot delete the only profile!', null, 'danger');
    return;
  }

  appState.profiles = appState.profiles.filter(p => p.id !== id);
  delete appState.profileData[id];

  if (appState.activeProfileId === id) {
    appState.activeProfileId = appState.profiles[0].id;
    currentData = appState.profileData[appState.activeProfileId];
  }

  saveStorageImmediate();
  renderSettings();
  renderDashboard();
  showToast('Profile deleted.');
}

function openProfileModal() {
  renderProfilesList();
  openModal({
    title: 'Switch Profile Workspace',
    body: `
      <p class="text-sm text-muted mb-3">Select a workspace profile to load its isolated data.</p>
      <div id="modal-profiles-container">${document.getElementById('settings-profiles-list') ? document.getElementById('settings-profiles-list').innerHTML : ''}</div>
      <button class="btn btn-primary btn-sm mt-3" onclick="closeModal(); openNewProfileModal();">+ Create New Profile</button>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Close</button>
    `
  });
}

function renderActivityLog() {
  const container = document.getElementById('activity-log-container');
  if (!container) return;

  const logs = currentData.activityLog || [];
  if (logs.length === 0) {
    container.innerHTML = `<div class="text-xs text-muted p-2">No activity recorded yet.</div>`;
    return;
  }

  container.innerHTML = logs.map(l => `
    <div class="flex items-center justify-between p-2 text-xs" style="border-bottom: 1px solid var(--border);">
      <span>${escapeHtml(l.text)}</span>
      <span class="text-muted">${new Date(l.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
    </div>
  `).join('');
}

function clearActivityLog() {
  currentData.activityLog = [];
  saveStorage();
  renderActivityLog();
}

/* THEMES & PREFERENCES */
function cycleTheme() {
  const current = currentData.settings.theme || 'light';
  const next = current === 'light' ? 'dark' : current === 'dark' ? 'system' : 'light';
  setAppTheme(next);
}

function setAppTheme(theme) {
  currentData.settings.theme = theme;
  saveStorage();
  applyThemeAndPreferences();
  showToast(`Theme changed to ${theme}`);
}

function setAppAccent(accent) {
  currentData.settings.accent = accent;
  saveStorage();
  applyThemeAndPreferences();
  showToast(`Accent set to ${accent}`);
}

function setAppCardStyle(style) {
  currentData.settings.cardStyle = style;
  saveStorage();
  applyThemeAndPreferences();
}

function setAppDensity(density) {
  currentData.settings.density = density;
  saveStorage();
  applyThemeAndPreferences();
}

function applyThemeAndPreferences() {
  if (!currentData || !currentData.settings) return;
  const s = currentData.settings;

  // Theme attribute
  let effectiveTheme = s.theme;
  if (effectiveTheme === 'system') {
    effectiveTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  document.documentElement.setAttribute('data-theme', effectiveTheme);

  // Update theme icon
  const iconSlot = document.getElementById('theme-icon-slot');
  if (iconSlot) {
    iconSlot.setAttribute('data-icon', effectiveTheme === 'dark' ? 'moon' : 'sun');
    renderAllIcons();
  }

  // Accent attribute
  document.documentElement.setAttribute('data-accent', s.accent || 'indigo');
  // Card style
  document.documentElement.setAttribute('data-card-style', s.cardStyle || 'modern');
  // Density
  document.documentElement.setAttribute('data-density', s.density || 'comfortable');
}

/* DEMO DATA RESTORE / REMOVE */
function restoreDemoDataAction() {
  openModal({
    title: 'Restore Default Demo Data',
    body: `
      <p class="text-sm text-secondary">This will restore the full set of realistic study examples (Subjects, Chapters, Teachers, Timetable, Goals, Habits, Playlists) into your current profile.</p>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="confirmRestoreDemoData()">Restore Data</button>
    `
  });
}

function confirmRestoreDemoData() {
  currentData = getInitialDemoData();
  appState.profileData[appState.activeProfileId] = currentData;
  saveStorageImmediate();
  closeModal();
  renderView(currentView);
  showToast('Default demo data restored!', null, 'success');
}

function removeDemoDataAction() {
  openModal({
    title: 'Remove Demo Data',
    body: `
      <p class="text-sm text-secondary">This will wipe demo items to give you a completely clean, empty study workspace.</p>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-danger" onclick="confirmRemoveDemoData()">Wipe Demo Data</button>
    `
  });
}

function confirmRemoveDemoData() {
  currentData.goals = [];
  currentData.tasks = [];
  currentData.subjects = [];
  currentData.chapters = [];
  currentData.teachers = [];
  currentData.timetableClasses = [];
  currentData.stickyNotes = [];
  currentData.notes = [];
  currentData.videos = [];
  currentData.habits = [];
  currentData.calendarEvents = [];
  currentData.studySessions = [];

  saveStorageImmediate();
  closeModal();
  renderView(currentView);
  showToast('Demo data removed. Clean workspace ready!', null, 'normal');
}

/* DATA EXPORT & IMPORT */
function exportDataJSON() {
  const jsonStr = JSON.stringify(appState, null, 2);
  const blob = new Blob([jsonStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `StudyPulse_Backup_${new Date().toISOString().split('T')[0]}.json`;
  a.click();
  URL.revokeObjectURL(url);
  showToast('Backup JSON downloaded successfully!');
}

function openImportModal() {
  openModal({
    title: 'Import StudyPulse JSON Backup',
    body: `
      <p class="text-sm text-muted mb-3">Upload a previously exported JSON backup file or paste its content below.</p>
      <div class="form-group">
        <label>Select Backup File</label>
        <input type="file" id="import-file-input" accept=".json" class="form-control" onchange="handleImportFileSelect(event)">
      </div>
      <div class="form-group">
        <label>Or Paste Raw JSON</label>
        <textarea class="form-control" id="import-json-textarea" rows="6" placeholder="{ \\"activeProfileId\\": ... }"></textarea>
      </div>
      <div class="form-group">
        <label>Import Mode</label>
        <div class="flex items-center gap-3">
          <label><input type="radio" name="import-mode" value="replace" checked> Complete Replace / Restore</label>
          <label><input type="radio" name="import-mode" value="merge"> Merge with Current Workspace</label>
        </div>
      </div>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="confirmImportJSON()">Import Data</button>
    `
  });
}

function handleImportFileSelect(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (event) => {
    const area = document.getElementById('import-json-textarea');
    if (area) area.value = event.target.result;
  };
  reader.readAsText(file);
}

function confirmImportJSON() {
  const area = document.getElementById('import-json-textarea');
  if (!area || !area.value.trim()) {
    showToast('Please provide valid JSON content!', null, 'danger');
    return;
  }

  try {
    const parsed = JSON.parse(area.value.trim());
    const mode = document.querySelector('input[name="import-mode"]:checked').value;

    if (mode === 'replace') {
      if (parsed.activeProfileId && parsed.profiles && parsed.profileData) {
        appState = parsed;
      } else if (parsed.goals && parsed.subjects) {
        // Direct single profile payload
        appState.profileData[appState.activeProfileId] = parsed;
      }
      currentData = appState.profileData[appState.activeProfileId];
    } else {
      // Merge
      const incoming = parsed.profileData ? parsed.profileData[parsed.activeProfileId] : parsed;
      if (incoming) {
        if (incoming.goals) currentData.goals = [...currentData.goals, ...incoming.goals];
        if (incoming.tasks) currentData.tasks = [...currentData.tasks, ...incoming.tasks];
        if (incoming.subjects) currentData.subjects = [...currentData.subjects, ...incoming.subjects];
        if (incoming.chapters) currentData.chapters = [...currentData.chapters, ...incoming.chapters];
        if (incoming.teachers) currentData.teachers = [...currentData.teachers, ...incoming.teachers];
      }
    }

    saveStorageImmediate();
    closeModal();
    applyThemeAndPreferences();
    renderView(currentView);
    showToast('Data imported successfully!', null, 'success');
  } catch (err) {
    showToast('Invalid JSON file format!', null, 'danger');
  }
}

/* =========================================================================
   GLOBAL SEARCH & UNIVERSAL QUICK ADD
   ========================================================================= */

function openGlobalSearch() {
  openModal({
    title: 'Global Search (Ctrl+K)',
    body: `
      <div class="form-group mb-3">
        <input type="text" class="form-control" id="global-search-input" autofocus placeholder="Search goals, tasks, subjects, chapters, notes, stickies, teachers..." oninput="handleGlobalSearch(this.value)">
      </div>
      <div id="global-search-results" style="max-height: 340px; overflow-y: auto;">
        <div class="text-xs text-muted p-3 text-center">Type at least 2 characters to search across everything.</div>
      </div>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Close</button>
    `
  });
  setTimeout(() => {
    const inp = document.getElementById('global-search-input');
    if (inp) inp.focus();
  }, 100);
}

function handleGlobalSearch(query) {
  const resContainer = document.getElementById('global-search-results');
  if (!resContainer) return;
  const q = query.trim().toLowerCase();
  if (q.length < 2) {
    resContainer.innerHTML = `<div class="text-xs text-muted p-3 text-center">Type at least 2 characters to search.</div>`;
    return;
  }

  const results = [];

  // Search Goals
  currentData.goals.forEach(g => {
    if (g.title.toLowerCase().includes(q) || (g.description && g.description.toLowerCase().includes(q))) {
      results.push({ type: 'Goal', title: g.title, meta: `${g.progress}% • ${g.priority}`, action: () => { closeModal(); navigateTo('goals'); } });
    }
  });

  // Search Tasks
  currentData.tasks.forEach(t => {
    if (t.title.toLowerCase().includes(q)) {
      results.push({ type: 'Task', title: t.title, meta: t.completed ? 'Completed' : 'Pending', action: () => { closeModal(); navigateTo('todos'); } });
    }
  });

  // Search Subjects
  currentData.subjects.forEach(s => {
    if (s.name.toLowerCase().includes(q) || (s.code && s.code.toLowerCase().includes(q))) {
      results.push({ type: 'Subject', title: s.name, meta: `${s.code || ''} • Teacher: ${s.teacherName || 'N/A'}`, action: () => { closeModal(); openSubjectDashboardModal(s.id); } });
    }
  });

  // Search Chapters
  currentData.chapters.forEach(c => {
    if (c.name.toLowerCase().includes(q)) {
      results.push({ type: 'Chapter', title: c.name, meta: `Ch ${c.chapterNumber} • ${c.status}`, action: () => { closeModal(); navigateTo('chapters'); } });
    }
  });

  // Search Notes
  currentData.notes.forEach(n => {
    if (n.title.toLowerCase().includes(q) || n.content.toLowerCase().includes(q)) {
      results.push({ type: 'Note', title: n.title, meta: n.date || '', action: () => { closeModal(); navigateTo('notes'); } });
    }
  });

  // Search Teachers
  currentData.teachers.forEach(t => {
    if (t.name.toLowerCase().includes(q)) {
      results.push({ type: 'Teacher', title: t.name, meta: t.department || '', action: () => { closeModal(); navigateTo('teachers'); } });
    }
  });

  if (results.length === 0) {
    resContainer.innerHTML = `<div class="text-xs text-muted p-4 text-center">No results found for "${escapeHtml(query)}".</div>`;
    return;
  }

  resContainer.innerHTML = results.map(r => `
    <div class="flex items-center justify-between p-2 mb-1" style="background: var(--bg-input); border-radius: var(--radius-sm); cursor: pointer;" onclick="event.stopPropagation(); this.triggerAction();">
      <div>
        <span class="badge badge-indigo" style="font-size: 10px; margin-right: 6px;">${r.type}</span>
        <strong style="font-size: 13px;">${escapeHtml(r.title)}</strong>
        <span class="text-xs text-muted" style="margin-left: 6px;">${escapeHtml(r.meta)}</span>
      </div>
      <span class="text-xs text-muted">&rarr;</span>
    </div>
  `).join('');

  // Attach action triggers to DOM nodes
  const rows = resContainer.querySelectorAll('.flex');
  rows.forEach((row, i) => {
    row.triggerAction = results[i].action;
  });
}

function openQuickAddModal() {
  openModal({
    title: 'Universal Quick Add',
    body: `
      <p class="text-sm text-muted mb-3">What would you like to add to your workspace?</p>
      <div class="dashboard-grid">
        <button class="btn btn-secondary col-6" style="padding: 16px; justify-content: flex-start;" onclick="closeModal(); openGoalModal();">
          ${getIconHtml('target')}
          <span>New Goal</span>
        </button>
        <button class="btn btn-secondary col-6" style="padding: 16px; justify-content: flex-start;" onclick="closeModal(); openTaskModal();">
          ${getIconHtml('check-square')}
          <span>New To-Do Task</span>
        </button>
        <button class="btn btn-secondary col-6" style="padding: 16px; justify-content: flex-start;" onclick="closeModal(); openSubjectModal();">
          ${getIconHtml('book-open')}
          <span>New Subject</span>
        </button>
        <button class="btn btn-secondary col-6" style="padding: 16px; justify-content: flex-start;" onclick="closeModal(); openChapterModal();">
          ${getIconHtml('list-tree')}
          <span>New Chapter</span>
        </button>
        <button class="btn btn-secondary col-6" style="padding: 16px; justify-content: flex-start;" onclick="closeModal(); openTimetableClassModal();">
          ${getIconHtml('table')}
          <span>Schedule Class</span>
        </button>
        <button class="btn btn-secondary col-6" style="padding: 16px; justify-content: flex-start;" onclick="closeModal(); openNoteModal();">
          ${getIconHtml('file-text')}
          <span>New Note</span>
        </button>
        <button class="btn btn-secondary col-6" style="padding: 16px; justify-content: flex-start;" onclick="closeModal(); openStickyModal();">
          ${getIconHtml('sticky-note')}
          <span>New Sticky Note</span>
        </button>
        <button class="btn btn-secondary col-6" style="padding: 16px; justify-content: flex-start;" onclick="closeModal(); openHabitModal();">
          ${getIconHtml('flame')}
          <span>New Habit</span>
        </button>
        <button class="btn btn-secondary col-6" style="padding: 16px; justify-content: flex-start;" onclick="closeModal(); openUploadDocumentsModal();">
          ${getIconHtml('upload')}
          <span>Upload Document</span>
        </button>
        <button class="btn btn-secondary col-6" style="padding: 16px; justify-content: flex-start;" onclick="closeModal(); openTopSubjectsModal();">
          ${getIconHtml('book-open')}
          <span>Subjects & Faculty</span>
        </button>
      </div>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
    `
  });
}

/* =========================================================================
   LEFT THREE DOTS & TOPBAR SUBJECTS CONTROLLER
   ========================================================================= */

function toggleLeftDotsMenu(e) {
  if (e) {
    e.preventDefault();
    e.stopPropagation();
  }
  const menu = document.getElementById('left-dots-menu');
  if (!menu) return;
  const isHidden = menu.style.display === 'none' || !menu.style.display;
  menu.style.display = isHidden ? 'block' : 'none';
  if (isHidden) {
    renderAllIcons();
  }
}

function closeLeftDotsMenu() {
  const menu = document.getElementById('left-dots-menu');
  if (menu) menu.style.display = 'none';
}

// Close left dots menu on outside click
document.addEventListener('click', (e) => {
  const menu = document.getElementById('left-dots-menu');
  const btn = document.getElementById('left-dots-btn');
  if (menu && menu.style.display === 'block') {
    if (!menu.contains(e.target) && (!btn || !btn.contains(e.target))) {
      closeLeftDotsMenu();
    }
  }
});

/* =========================================================================
   TOPBAR SUBJECTS LIST VIEW (WITH TEACHER SUBTITLE - STRICTLY NO EDIT)
   ========================================================================= */

function openTopSubjectsModal() {
  const subjects = currentData.subjects || [];
  
  const bodyHtml = subjects.length === 0
    ? `
      <div style="text-align: center; padding: 40px 20px;">
        <div style="font-size: 38px; margin-bottom: 8px;">📚</div>
        <h4 style="font-size: 16px; font-weight: 700; margin-bottom: 4px;">No Subjects Enrolled</h4>
        <p class="text-sm text-muted">Add your academic courses to start tracking syllabus progress and faculty information.</p>
        <button class="btn btn-primary btn-sm mt-3" onclick="closeModal(); navigateTo('subjects'); openSubjectModal();">
          + Add New Subject
        </button>
      </div>
    `
    : `
      <div class="mb-3 flex items-center justify-between">
        <span class="text-xs font-semibold text-muted uppercase tracking-wider">
          Enrolled Courses (${subjects.length})
        </span>
        <span class="text-xs text-secondary">
          Click any course to view syllabus breakdown
        </span>
      </div>

      <div class="top-subjects-list" style="display: flex; flex-direction: column; gap: 10px; max-height: 480px; overflow-y: auto; padding-right: 4px;">
        ${subjects.map(s => {
          // Calculate syllabus progress
          const chapters = (currentData.chapters || []).filter(c => c.subjectId === s.id);
          const totalChapters = chapters.length || s.totalChapters || 1;
          const completedChapters = chapters.filter(c => c.status === 'Completed').length;
          const progress = Math.round((completedChapters / totalChapters) * 100);

          // Get teacher name - ONLY show subject name and teacher name as requested
          const teacherName = s.teacherName || 'Not Assigned';

          return `
            <div class="top-subject-item-card" style="border: 1px solid var(--border); border-left: 5px solid ${s.color || 'var(--accent)'}; border-radius: var(--radius-md); padding: 14px 16px; background: var(--bg-card); transition: all 0.2s ease;">
              <div class="flex items-center justify-between gap-3">
                <div style="flex: 1; min-width: 0;">
                  <!-- Subject Name -->
                  <h4 style="font-size: 15px; font-weight: 700; color: var(--text-primary); margin: 0 0 4px 0; line-height: 1.3;">
                    ${escapeHtml(s.name)}
                  </h4>

                  <!-- Subtitle with Teacher Name ONLY (no email, phone, room, etc.) -->
                  <div class="subject-teacher-subtitle text-sm" style="color: var(--text-secondary); font-weight: 500;">
                    Teacher: <span style="color: var(--accent); font-weight: 600;">${escapeHtml(teacherName)}</span>
                  </div>
                </div>

                <!-- Action Button to View Subject Chapters -->
                <button class="btn btn-sm btn-secondary" onclick="closeModal(); openSubjectDashboardModal('${s.id}')" title="View Chapters">
                  <span>View</span>
                  <span>&rarr;</span>
                </button>
              </div>
            </div>
          `;
        }).join('')}
      </div>
    `;

  openModal({
    title: `Academic Subjects & Teachers (${subjects.length})`,
    body: bodyHtml,
    footer: `
      <div class="flex items-center justify-between w-full">
        <button class="btn btn-secondary btn-sm" onclick="closeModal(); navigateTo('subjects');">
          <span>Go to Subjects Page</span>
        </button>
        <button class="btn btn-primary btn-sm" onclick="closeModal()">
          <span>Done</span>
        </button>
      </div>
    `
  });
}

/* =========================================================================
   DOCUMENT UPLOAD & LIBRARY CONTROLLER
   ========================================================================= */

let pendingDocFile = null;

function formatDocBytes(bytes, decimals = 1) {
  if (!bytes || bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function openUploadDocumentsModal(preselectedSubjectId = '') {
  pendingDocFile = null;
  const subjects = currentData.subjects || [];

  openModal({
    title: 'Upload Study Documents & Files',
    body: `
      <p class="text-sm text-secondary mb-3">
        Upload syllabus PDFs, lecture notes, question papers, cheatsheets, or reference guides to your offline study storage.
      </p>

      <form id="upload-doc-form" onsubmit="handleDocumentUploadSubmit(event)">
        <!-- Drag & Drop Zone -->
        <div id="doc-dropzone" class="file-dropzone mb-3" onclick="document.getElementById('doc-file-input').click()">
          <div class="dropzone-icon">
            ${getIconHtml('upload')}
          </div>
          <div class="dropzone-text">
            <strong>Choose a file</strong> or drag & drop here
          </div>
          <div class="text-xs text-muted mt-1">
            Supports PDF, DOCX, TXT, MD, Images, ZIP (Stored in browser storage)
          </div>
          <input type="file" id="doc-file-input" style="display:none;" onchange="handleDocFileSelect(event)" accept=".pdf,.doc,.docx,.txt,.md,.png,.jpg,.jpeg,.zip">
          <div id="selected-file-preview" style="display:none; margin-top: 10px;" class="badge badge-indigo">
            <span class="icon-slot" data-icon="file"></span>
            <span id="selected-file-name" style="margin-left: 4px;">file.pdf</span>
            <span id="selected-file-size" class="text-muted" style="margin-left: 6px;"></span>
          </div>
        </div>

        <div class="form-group mb-3">
          <label class="form-label" for="doc-title-input">Document Title *</label>
          <input type="text" id="doc-title-input" class="form-control" placeholder="e.g. Data Structures Full Notes Chapter 1-5" required>
        </div>

        <div class="form-row mb-3">
          <div class="form-group">
            <label class="form-label" for="doc-subject-select">Link to Subject</label>
            <select id="doc-subject-select" class="form-control">
              <option value="">-- General / No Subject --</option>
              ${subjects.map(s => `
                <option value="${s.id}" ${s.id === preselectedSubjectId ? 'selected' : ''}>
                  ${escapeHtml(s.name)} (${escapeHtml(s.code || 'Course')})
                </option>
              `).join('')}
            </select>
          </div>

          <div class="form-group">
            <label class="form-label" for="doc-category-select">Document Category</label>
            <select id="doc-category-select" class="form-control">
              <option value="Lecture Notes">Lecture Notes</option>
              <option value="Syllabus">Syllabus / Outline</option>
              <option value="Cheatsheet">Cheatsheet & Formulas</option>
              <option value="Assignment">Assignment / Problem Set</option>
              <option value="Past Exam">Past Exam Paper</option>
              <option value="Reference Book">Reference Book / PDF</option>
              <option value="Other">Other Document</option>
            </select>
          </div>
        </div>

        <div class="form-group mb-3">
          <label class="form-label" for="doc-notes-input">Key Takeaways or Description (Optional)</label>
          <textarea id="doc-notes-input" class="form-control" rows="2" placeholder="Brief summary of document contents or important exam topics covered..."></textarea>
        </div>

        <div class="upload-doc-actions flex items-center justify-end gap-2 mt-4">
          <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
          <button type="submit" class="btn btn-primary" id="upload-doc-submit-btn">
            ${getIconHtml('upload')}
            <span>Upload Document</span>
          </button>
        </div>
      </form>
    `
  });

  // Setup drag & drop on dropzone
  setupDocDropzone();
}

function setupDocDropzone() {
  const dropzone = document.getElementById('doc-dropzone');
  if (!dropzone) return;

  ['dragenter', 'dragover'].forEach(name => {
    dropzone.addEventListener(name, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add('dragover');
    }, false);
  });

  ['dragleave', 'drop'].forEach(name => {
    dropzone.addEventListener(name, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove('dragover');
    }, false);
  });

  dropzone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    if (dt && dt.files && dt.files.length > 0) {
      setPendingDocFile(dt.files[0]);
    }
  }, false);
}

function handleDocFileSelect(e) {
  const file = e.target.files && e.target.files[0];
  if (!file) return;
  setPendingDocFile(file);
}

function setPendingDocFile(file) {
  pendingDocFile = file;
  const preview = document.getElementById('selected-file-preview');
  const nameEl = document.getElementById('selected-file-name');
  const sizeEl = document.getElementById('selected-file-size');
  const titleInput = document.getElementById('doc-title-input');

  if (preview && nameEl) {
    nameEl.textContent = file.name;
    if (sizeEl) sizeEl.textContent = '(' + formatDocBytes(file.size) + ')';
    preview.style.display = 'inline-flex';
  }

  if (titleInput && !titleInput.value) {
    const baseName = file.name.replace(/\.[^/.]+$/, "").replace(/[-_]/g, " ");
    titleInput.value = baseName;
  }
}

function handleDocumentUploadSubmit(e) {
  e.preventDefault();
  const title = (document.getElementById('doc-title-input').value || '').trim();
  const subjectId = document.getElementById('doc-subject-select').value;
  const category = document.getElementById('doc-category-select').value;
  const notes = (document.getElementById('doc-notes-input').value || '').trim();

  if (!title) {
    showToast('Please enter a document title', null, 'danger');
    return;
  }

  const fileName = pendingDocFile ? pendingDocFile.name : (title.replace(/\s+/g, '_') + '.pdf');
  const fileSize = pendingDocFile ? formatDocBytes(pendingDocFile.size) : '520 KB';
  const fileType = pendingDocFile ? pendingDocFile.type : 'application/pdf';

  // Read file data if present and under 4MB
  if (pendingDocFile && pendingDocFile.size < 4 * 1024 * 1024) {
    const reader = new FileReader();
    reader.onload = function(loadEvent) {
      saveUploadedDocument({
        id: 'doc-' + Date.now(),
        title: title,
        name: fileName,
        size: fileSize,
        type: fileType,
        subjectId: subjectId,
        category: category,
        notes: notes,
        uploadDate: new Date().toISOString().split('T')[0],
        dataUrl: loadEvent.target.result
      });
    };
    reader.readAsDataURL(pendingDocFile);
  } else {
    // Save metadata
    saveUploadedDocument({
      id: 'doc-' + Date.now(),
      title: title,
      name: fileName,
      size: fileSize,
      type: fileType,
      subjectId: subjectId,
      category: category,
      notes: notes,
      uploadDate: new Date().toISOString().split('T')[0],
      dataUrl: ''
    });
  }
}

function saveUploadedDocument(doc) {
  if (!currentData.documents) currentData.documents = [];
  currentData.documents.unshift(doc);
  saveStorage();
  updateBadges();
  showToast(`Document "${doc.title}" uploaded!`, null, 'success');
  pendingDocFile = null;
  closeModal();
  openDocumentsLibraryModal();
}

function openDocumentsLibraryModal(filterCategory = 'All') {
  const docs = currentData.documents || [];
  const subjects = currentData.subjects || [];

  const filteredDocs = filterCategory === 'All' 
    ? docs 
    : docs.filter(d => d.category === filterCategory);

  const categories = ['All', 'Lecture Notes', 'Syllabus', 'Cheatsheet', 'Assignment', 'Past Exam', 'Reference Book', 'Other'];

  const bodyHtml = `
    <div class="flex items-center justify-between flex-wrap gap-2 mb-3">
      <div class="filter-tabs" style="display: flex; gap: 4px; overflow-x: auto; max-width: 100%; padding-bottom: 2px;">
        ${categories.map(cat => {
          const count = cat === 'All' ? docs.length : docs.filter(d => d.category === cat).length;
          if (cat !== 'All' && count === 0) return '';
          const isActive = filterCategory === cat;
          return `
            <button class="btn btn-sm ${isActive ? 'btn-primary' : 'btn-secondary'}" onclick="openDocumentsLibraryModal('${cat}')" style="padding: 4px 10px; font-size: 11px;">
              ${cat} (${count})
            </button>
          `;
        }).join('')}
      </div>
      <button class="btn btn-sm btn-primary" onclick="openUploadDocumentsModal()" style="font-size: 12px;">
        ${getIconHtml('upload')}
        <span>+ Upload File</span>
      </button>
    </div>

    ${filteredDocs.length === 0 ? `
      <div style="text-align: center; padding: 40px 20px;">
        <div style="font-size: 38px; margin-bottom: 8px;">📂</div>
        <h4 style="font-size: 16px; font-weight: 700; margin-bottom: 4px;">No Documents in this Category</h4>
        <p class="text-sm text-muted">Upload your PDFs, notes, or cheatsheets to build your library.</p>
        <button class="btn btn-primary btn-sm mt-3" onclick="openUploadDocumentsModal()">
          ${getIconHtml('upload')}
          <span>Upload Document</span>
        </button>
      </div>
    ` : `
      <div class="documents-list" style="display: flex; flex-direction: column; gap: 8px; max-height: 480px; overflow-y: auto; padding-right: 4px;">
        ${filteredDocs.map(doc => {
          const subject = subjects.find(s => s.id === doc.subjectId);
          return `
            <div class="doc-item-card">
              <div class="doc-item-icon">
                ${getIconHtml('file')}
              </div>
              <div style="flex: 1; min-width: 0;">
                <div class="flex items-center gap-2 flex-wrap mb-1">
                  <h4 style="font-size: 14px; font-weight: 700; color: var(--text-primary); margin: 0; line-height: 1.3;">
                    ${escapeHtml(doc.title || doc.name)}
                  </h4>
                  <span class="badge badge-indigo" style="font-size: 10px;">${escapeHtml(doc.category || 'Document')}</span>
                  ${subject ? `
                    <span class="badge" style="background: ${subject.color || '#4f46e5'}22; color: ${subject.color || '#4f46e5'}; font-size: 10px; font-weight: 600;">
                      ${escapeHtml(subject.name)}
                    </span>
                  ` : ''}
                </div>
                <div class="flex items-center gap-3 text-xs text-muted">
                  <span>📄 ${escapeHtml(doc.name || 'document.pdf')}</span>
                  <span>💾 ${doc.size || '350 KB'}</span>
                  <span>📅 ${doc.uploadDate || 'Recent'}</span>
                </div>
                ${doc.notes ? `
                  <p class="text-xs text-secondary mt-1" style="margin-bottom: 0; font-style: italic;">
                    ${escapeHtml(doc.notes)}
                  </p>
                ` : ''}
              </div>
              <div class="doc-item-actions flex items-center gap-1">
                <button class="btn btn-sm btn-secondary btn-icon" onclick="downloadDocumentFile('${doc.id}')" title="Download Document">
                  ${getIconHtml('download')}
                </button>
                <button class="btn btn-sm btn-secondary btn-icon" onclick="deleteDocument('${doc.id}')" title="Delete Document" style="color: var(--danger, #ef4444);">
                  ${getIconHtml('trash-2')}
                </button>
              </div>
            </div>
          `;
        }).join('')}
      </div>
    `}
  `;

  openModal({
    title: `Study Documents & Uploads (${docs.length})`,
    body: bodyHtml,
    footer: `
      <div class="flex items-center justify-between w-full">
        <button class="btn btn-primary btn-sm" onclick="openUploadDocumentsModal()">
          ${getIconHtml('upload')}
          <span>+ Upload Another Document</span>
        </button>
        <button class="btn btn-secondary btn-sm" onclick="closeModal()">Close</button>
      </div>
    `
  });
}

function downloadDocumentFile(docId) {
  const doc = (currentData.documents || []).find(d => d.id === docId);
  if (!doc) return;

  if (doc.dataUrl) {
    const a = document.createElement('a');
    a.href = doc.dataUrl;
    a.download = doc.name || 'study-document.pdf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    showToast(`Downloading "${doc.name}"...`, null, 'info');
  } else {
    // Generate readable study export
    const content = `StudyPulse Document: ${doc.title}\nCategory: ${doc.category}\nUpload Date: ${doc.uploadDate}\n\nSummary & Notes:\n${doc.notes || doc.content || 'Stored in offline study repository.'}`;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = (doc.name.endsWith('.pdf') ? doc.name.replace('.pdf', '.txt') : doc.name) || 'document-export.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast(`Downloaded "${doc.title}" details.`, null, 'info');
  }
}

function deleteDocument(docId) {
  const index = (currentData.documents || []).findIndex(d => d.id === docId);
  if (index !== -1) {
    const removed = currentData.documents.splice(index, 1)[0];
    saveStorage();
    updateBadges();
    showToast(`Document "${removed.title}" deleted.`, null, 'warning');
    openDocumentsLibraryModal();
  }
}

/* =========================================================================
   MODAL CONTROLLER
   ========================================================================= */

function openModal({ title, body, footer }) {
  const container = document.getElementById('modal-container');
  const box = document.getElementById('modal-box');
  if (!container || !box) return;

  box.innerHTML = `
    <div class="modal-header">
      <h3 class="modal-title">${title}</h3>
      <button class="modal-close" onclick="closeModal()">&times;</button>
    </div>
    <div class="modal-body">${body}</div>
    ${footer ? `<div class="modal-footer">${footer}</div>` : ''}
  `;

  container.classList.add('active');
  renderAllIcons();
}

function closeModal() {
  const container = document.getElementById('modal-container');
  if (container) container.classList.remove('active');
}

function handleModalBackdropClick(e) {
  if (e.target.id === 'modal-container') {
    closeModal();
  }
}

/* =========================================================================
   PROGRESSIVE WEB APP (PWA) & SERVICE WORKER CONTROLLER
   ========================================================================= */

let deferredPWAInstallPrompt = null;

function initPWAAndServiceWorker() {
  // 1. Register Service Worker if supported
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js', { scope: '/' })
        .then((reg) => {
          console.log('StudyPulse ServiceWorker registered with scope:', reg.scope);
        })
        .catch((err) => {
          console.warn('ServiceWorker registration error:', err);
        });
    });
  }

  // 2. Listen for BeforeInstallPrompt
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPWAInstallPrompt = e;
    updatePWAUIState();
  });

  // 3. Listen for app installed
  window.addEventListener('appinstalled', () => {
    deferredPWAInstallPrompt = null;
    updatePWAUIState();
    showToast('StudyPulse App installed successfully on your device!', null, 'success');
  });

  // 4. Offline / Online network status monitor
  function updateOnlineStatus() {
    const offlineIndicator = document.getElementById('offline-indicator');
    if (!navigator.onLine) {
      if (offlineIndicator) offlineIndicator.style.display = 'flex';
      showToast('You are currently offline. LocalStorage cache is active.', null, 'warning');
    } else {
      if (offlineIndicator) offlineIndicator.style.display = 'none';
    }
  }

  window.addEventListener('online', updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);
  updateOnlineStatus();

  // 5. Initial UI state sync
  updatePWAUIState();
}

function isRunningStandalone() {
  return window.matchMedia('(display-mode: standalone)').matches ||
    window.navigator.standalone === true ||
    document.referrer.includes('android-app://');
}

function updatePWAUIState() {
  const isStandalone = isRunningStandalone();
  const badge = document.getElementById('pwa-status-badge');
  const installBtn = document.getElementById('settings-install-app-btn');
  const headerInstallBtn = document.getElementById('header-install-btn');

  if (isStandalone) {
    if (badge) {
      badge.textContent = 'Installed (Standalone)';
      badge.className = 'badge badge-emerald';
    }
    if (installBtn) {
      installBtn.disabled = true;
      installBtn.innerHTML = `${getIconHtml('check')} <span>App Already Installed</span>`;
    }
    if (headerInstallBtn) {
      headerInstallBtn.style.display = 'none';
    }
  } else {
    if (badge) {
      badge.textContent = deferredPWAInstallPrompt ? 'Ready to Install' : 'Installable PWA';
      badge.className = 'badge badge-indigo';
    }
  }
}

function openAppInNewTab() {
  window.open(window.location.href, '_blank');
}

function copyAppUrl() {
  const url = window.location.href;
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(url).then(() => {
      showToast('App URL copied to clipboard! Open it in Chrome or Safari.', null, 'success');
    }).catch(() => {
      fallbackCopyText(url);
    });
  } else {
    fallbackCopyText(url);
  }
}

function fallbackCopyText(text) {
  try {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast('App URL copied to clipboard! Open it in Chrome or Safari.', null, 'success');
  } catch (e) {
    showToast('Could not copy link automatically.', null, 'warning');
  }
}

function triggerPWAInstall() {
  if (isRunningStandalone()) {
    showToast('StudyPulse is already running as an installed standalone app!', null, 'info');
    return;
  }

  // Check if inside iframe
  const isInIframe = window.self !== window.top;

  if (deferredPWAInstallPrompt && !isInIframe) {
    deferredPWAInstallPrompt.prompt().then(() => {
      return deferredPWAInstallPrompt.userChoice;
    }).then((choiceResult) => {
      if (choiceResult && choiceResult.outcome === 'accepted') {
        showToast('Installing StudyPulse to your device...', null, 'success');
        deferredPWAInstallPrompt = null;
        updatePWAUIState();
      } else {
        showAppInstallationGuideModal();
      }
    }).catch((err) => {
      console.warn('Install prompt error:', err);
      showAppInstallationGuideModal();
    });
    return;
  }

  // If deferred prompt not available (e.g. inside preview iframe, iOS Safari, or needs top window)
  showAppInstallationGuideModal();
}

function showAppInstallationGuideModal() {
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  const isAndroid = /Android/.test(navigator.userAgent);
  const isInIframe = window.self !== window.top;

  let platformContent = '';
  if (isIOS) {
    platformContent = `
      <div class="card p-3 mb-3" style="background: rgba(79, 70, 229, 0.08); border-color: rgba(79, 70, 229, 0.25);">
        <h4 style="font-weight: 700; color: var(--text-primary); margin-bottom: 8px; font-size: 14px;">
          📱 How to Install on iPhone / iPad (Safari):
        </h4>
        <ol class="text-xs text-secondary" style="padding-left: 20px; line-height: 1.8; margin: 0;">
          <li>Make sure you are in Safari (tap <strong>"Open in New Tab"</strong> above if viewing inside preview).</li>
          <li>Tap the <strong>Share</strong> button (box with an upward arrow) in the Safari bottom bar.</li>
          <li>Scroll down in the share sheet and tap <strong>Add to Home Screen</strong>.</li>
          <li>Tap <strong>Add</strong> in the top right corner.</li>
        </ol>
      </div>
    `;
  } else if (isAndroid) {
    platformContent = `
      <div class="card p-3 mb-3" style="background: rgba(16, 185, 129, 0.08); border-color: rgba(16, 185, 129, 0.25);">
        <h4 style="font-weight: 700; color: var(--text-primary); margin-bottom: 8px; font-size: 14px;">
          🤖 How to Install on Android (Chrome):
        </h4>
        <ol class="text-xs text-secondary" style="padding-left: 20px; line-height: 1.8; margin: 0;">
          <li>Make sure you are in Chrome (tap <strong>"Open in New Tab"</strong> above if viewing inside preview).</li>
          <li>Tap the <strong>three dots (⋮)</strong> menu icon in top-right of Chrome.</li>
          <li>Tap <strong>Install app</strong> or <strong>Add to Home screen</strong>.</li>
          <li>Confirm by tapping <strong>Install</strong>.</li>
        </ol>
      </div>
    `;
  } else {
    platformContent = `
      <div class="card p-3 mb-3" style="background: rgba(79, 70, 229, 0.08); border-color: rgba(79, 70, 229, 0.25);">
        <h4 style="font-weight: 700; color: var(--text-primary); margin-bottom: 8px; font-size: 14px;">
          💻 How to Install on Windows / Mac / Chromebook:
        </h4>
        <ol class="text-xs text-secondary" style="padding-left: 20px; line-height: 1.8; margin: 0;">
          <li>Open the app in Chrome or Edge (tap <strong>"Open in New Tab"</strong> above).</li>
          <li>Look at the right side of the browser URL / address bar for the <strong>Install icon</strong> (computer with down-arrow) or menu (⋮) &gt; <strong>"Install StudyPulse"</strong>.</li>
          <li>Click <strong>Install</strong> to launch it in its own standalone window!</li>
        </ol>
      </div>
    `;
  }

  openModal({
    title: 'Install StudyPulse App',
    body: `
      <div style="text-align: center; margin-bottom: 16px;">
        <div style="width: 60px; height: 60px; margin: 0 auto 10px; border-radius: 16px; background: linear-gradient(135deg, #6366f1, #4338ca); display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 20px rgba(79, 70, 229, 0.35); color: #fff;">
          ${getIconHtml('download')}
        </div>
        <h3 style="font-size: 18px; font-weight: 800; color: var(--text-primary); margin-bottom: 4px;">Install StudyPulse PWA</h3>
        <p class="text-xs text-muted" style="max-width: 380px; margin: 0 auto;">
          Installable directly onto your Android phone, iPhone, iPad, Windows, or Mac with 100% offline access.
        </p>
      </div>

      ${isInIframe ? `
        <div class="card p-3 mb-3" style="background: rgba(245, 158, 11, 0.08); border: 2px solid rgba(245, 158, 11, 0.35);">
          <div class="flex items-center gap-2 mb-1">
            <span style="font-size: 16px;">💡</span>
            <strong style="font-size: 13px; color: var(--text-primary);">Preview Window Detected:</strong>
          </div>
          <p class="text-xs text-secondary mb-3" style="margin-bottom: 10px; line-height: 1.5;">
            Browsers block app installation from inside preview frames. Please open the app in a regular browser tab to install it on your home screen or desktop.
          </p>
          <div class="flex items-center gap-2 flex-wrap">
            <button class="btn btn-primary btn-sm" onclick="openAppInNewTab()">
              <span>Open in New Tab ↗</span>
            </button>
            <button class="btn btn-secondary btn-sm" onclick="copyAppUrl()">
              <span>Copy App Link 📋</span>
            </button>
          </div>
        </div>
      ` : `
        <div class="flex items-center justify-between p-2 mb-3 rounded" style="background: var(--bg-surface); border: 1px solid var(--border);">
          <span class="text-xs text-muted">Direct browser URL:</span>
          <button class="btn btn-secondary btn-sm" onclick="copyAppUrl()">
            <span>Copy App Link 📋</span>
          </button>
        </div>
      `}

      ${platformContent}

      <div class="grid grid-2 gap-2 text-xs text-muted mb-2">
        <div class="card p-2" style="background: var(--bg-surface);">
          <strong class="text-primary block mb-1">⚡ 100% Offline Ready</strong>
          Cached via Service Worker, all notes & records preserved without internet.
        </div>
        <div class="card p-2" style="background: var(--bg-surface);">
          <strong class="text-primary block mb-1">📱 Home Screen Launch</strong>
          Opens in dedicated fullscreen window without browser URL bars.
        </div>
      </div>
    `,
    footer: `
      <div class="flex items-center justify-between w-full">
        <button class="btn btn-secondary btn-sm" onclick="closeModal()">Close</button>
        ${deferredPWAInstallPrompt && !isInIframe ? `
          <button class="btn btn-primary btn-sm" onclick="deferredPWAInstallPrompt.prompt(); closeModal();">
            ${getIconHtml('download')}
            <span>Install Now</span>
          </button>
        ` : `
          <button class="btn btn-primary btn-sm" onclick="openAppInNewTab(); closeModal();">
            <span>Open in Full Browser ↗</span>
          </button>
        `}
      </div>
    `
  });
}

/* =========================================================================
   FIRST VISIT DEMO DATA PROMPT
   ========================================================================= */

function checkFirstVisitDemoPrompt() {
  const answered = localStorage.getItem('studypulse_demo_prompt_answered');
  if (answered) return;

  setTimeout(() => {
    openModal({
      title: 'Welcome to StudyPulse Pro! 🎓',
      body: `
        <div style="text-align: center; margin-bottom: 20px;">
          <div style="width: 64px; height: 64px; margin: 0 auto 12px; border-radius: 18px; background: linear-gradient(135deg, #6366f1, #4338ca); display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 24px rgba(79, 70, 229, 0.35); color: #fff; font-size: 26px;">
            📚
          </div>
          <h3 style="font-size: 19px; font-weight: 800; color: var(--text-primary); margin-bottom: 6px;">
            Set Up Your Study Workspace
          </h3>
          <p class="text-sm text-secondary" style="max-width: 440px; margin: 0 auto; line-height: 1.5;">
            Would you like to start with pre-loaded <strong>demo study data</strong> (subjects, chapters, faculty, timetable, goals, and tasks) to explore, or start with a <strong>clean slate</strong>?
          </p>
        </div>

        <div class="grid grid-2 gap-3 mb-3" style="grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));">
          <div class="card p-3" style="border: 2px solid var(--accent); background: var(--bg-card); cursor: pointer; transition: transform 0.15s ease;" onclick="chooseFirstVisitOption('demo')">
            <div class="flex items-center gap-2 mb-2">
              <span style="font-size: 20px;">🚀</span>
              <h4 style="font-weight: 700; color: var(--accent); font-size: 14px; margin: 0;">Load Demo Data (Recommended)</h4>
            </div>
            <p class="text-xs text-muted" style="line-height: 1.5; margin-bottom: 12px;">
              Instantly fills realistic courses (DSA, OS, Math), weekly timetable, tasks, goals, habits, and notes so you can test all features right away.
            </p>
            <button class="btn btn-primary btn-sm w-full" onclick="event.stopPropagation(); chooseFirstVisitOption('demo')">
              <span>Yes, Load Demo Data</span>
            </button>
          </div>

          <div class="card p-3" style="border: 1px solid var(--border); background: var(--bg-card); cursor: pointer; transition: transform 0.15s ease;" onclick="chooseFirstVisitOption('clean')">
            <div class="flex items-center gap-2 mb-2">
              <span style="font-size: 20px;">✨</span>
              <h4 style="font-weight: 700; color: var(--text-primary); font-size: 14px; margin: 0;">Start with Clean Slate</h4>
            </div>
            <p class="text-xs text-muted" style="line-height: 1.5; margin-bottom: 12px;">
              Begins with an empty workspace. Best if you want to immediately enter your own actual classes, schedule, and assignments.
            </p>
            <button class="btn btn-secondary btn-sm w-full" onclick="event.stopPropagation(); chooseFirstVisitOption('clean')">
              <span>No, Start Clean</span>
            </button>
          </div>
        </div>

        <p class="text-xs text-muted text-center" style="margin-bottom: 0;">
          💡 You can always reload demo data or clear your workspace anytime from <strong>Settings & Backup</strong>.
        </p>
      `,
      footer: `
        <div class="flex items-center justify-between w-full">
          <span class="text-xs text-muted">You can customize this anytime in Settings</span>
          <button class="btn btn-secondary btn-sm" onclick="chooseFirstVisitOption('demo')">Dismiss</button>
        </div>
      `
    });
  }, 350);
}

function chooseFirstVisitOption(choice) {
  localStorage.setItem('studypulse_demo_prompt_answered', 'true');
  closeModal();
  if (choice === 'demo') {
    confirmRestoreDemoData();
    showToast('Demo study data loaded! Welcome to StudyPulse.', null, 'success');
  } else if (choice === 'clean') {
    confirmRemoveDemoData();
    showToast('Clean workspace initialized. Ready for your subjects & schedule!', null, 'info');
  }
}

/* =========================================================================
   APPLICATION BOOTSTRAP
   ========================================================================= */

document.addEventListener('DOMContentLoaded', () => {
  initStorage();
  startClock();
  initPWAAndServiceWorker();

  // Handle URL hash routing
  const initialHash = window.location.hash.replace('#', '') || 'dashboard';
  navigateTo(initialHash);

  // Check first visit demo prompt
  checkFirstVisitDemoPrompt();

  // Global Keyboard Shortcuts
  window.addEventListener('keydown', (e) => {
    // Ctrl + K -> Search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      openGlobalSearch();
    }
    // Escape -> Close Modal or Exit Focus Mode
    if (e.key === 'Escape') {
      closeModal();
      exitFocusMode();
    }
  });

  // Screen tap fullscreen listener - do not hijack interactive controls
  document.addEventListener('click', (e) => {
    if (e.target.closest('button, a, input, select, textarea, .btn, .profile-pill, .topbar-subjects-pill, .modal-dialog, [onclick]')) {
      return;
    }
    const isFullscreen = document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement;
    if (!isFullscreen) {
      const elem = document.documentElement;
      const requestMethod = elem.requestFullscreen || elem.webkitRequestFullscreen || elem.mozRequestFullScreen || elem.msRequestFullscreen;
      if (requestMethod) {
        try {
          const res = requestMethod.call(elem);
          if (res && res.catch) {
            res.catch(() => {});
          }
        } catch (err) {}
      }
    }
  });
});
"""
