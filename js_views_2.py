# Views Part 2: Subjects, Subject Dashboard, Chapters, Teachers, and Timetable
js_views_2_code = """
/* =========================================================================
   SUBJECTS MANAGER & DETAILED SUBJECT DASHBOARD
   ========================================================================= */

function renderSubjects() {
  const container = document.getElementById('subjects-cards-container');
  if (!container) return;

  if (currentData.subjects.length === 0) {
    container.innerHTML = `
      <div class="col-12 card" style="text-align: center; padding: 40px;">
        <div style="font-size: 36px; margin-bottom: 8px;">📚</div>
        <h3 style="font-size: 16px; font-weight: 700;">No subjects added yet</h3>
        <p class="text-sm text-muted">Add your academic courses to track teacher attendance and schedule.</p>
        <button class="btn btn-primary btn-sm mt-3" style="margin-top: 14px;" onclick="openSubjectModal()">+ Add Subject</button>
      </div>
    `;
    return;
  }

  container.innerHTML = currentData.subjects.map(s => {
    const cancelled = s.cancelledClasses || 0;
    const absent = s.absentClasses || 0;
    const recordsCount = (s.attendanceRecords || []).length;

    return `
      <div class="card col-6" style="border-top: 4px solid ${s.color || 'var(--accent)'}; position: relative;">
        <div class="card-header" style="margin-bottom: 12px;">
          <div>
            <h3 class="card-title" style="font-size: 17px; font-weight: 700; cursor: pointer;" onclick="openSubjectDashboardModal('${s.id}')">
              ${escapeHtml(s.name)}
            </h3>
            <div class="text-sm text-secondary mt-1 flex items-center gap-1">
              <span>👨‍🏫 Teacher:</span>
              <strong style="color: var(--text-primary); font-size: 14px;">${escapeHtml(s.teacherName || 'Not assigned')}</strong>
            </div>
          </div>
          <div class="flex items-center gap-1">
            <button class="btn btn-icon btn-sm btn-secondary" onclick="openSubjectModal('${s.id}')" title="Edit Subject">${getIconHtml('edit')}</button>
            <button class="btn btn-icon btn-sm btn-danger" onclick="deleteSubject('${s.id}')" title="Delete Subject">${getIconHtml('trash')}</button>
          </div>
        </div>

        <!-- Attendance Stats Row -->
        <div class="grid grid-cols-2 gap-2 mb-3" style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 14px;">
          <div style="background: rgba(239, 68, 68, 0.08); border-radius: var(--radius-sm); padding: 10px 12px; border-left: 3px solid var(--danger);">
            <div class="text-xs text-muted">Cancelled Classes</div>
            <div style="font-size: 18px; font-weight: 800; color: var(--danger);">${cancelled}</div>
          </div>
          <div style="background: rgba(245, 158, 11, 0.08); border-radius: var(--radius-sm); padding: 10px 12px; border-left: 3px solid var(--warning);">
            <div class="text-xs text-muted">Absences</div>
            <div style="font-size: 18px; font-weight: 800; color: var(--warning);">${absent}</div>
          </div>
        </div>

        <div class="flex items-center justify-between pt-2" style="border-top: 1px solid var(--border); padding-top: 10px;">
          <button class="btn btn-sm btn-secondary" onclick="openSubjectAttendanceHistoryModal('${s.id}')">
            ${getIconHtml('calendar')}
            <span>Attendance Records (${recordsCount})</span>
          </button>
          <button class="btn btn-sm btn-primary" onclick="openSubjectDashboardModal('${s.id}')">
            <span>Subject Details &rarr;</span>
          </button>
        </div>
      </div>
    `;
  }).join('');
}

function openSubjectChaptersFilter(subjectId) {
  navigateTo('chapters');
  const sel = document.getElementById('chapter-subject-filter');
  if (sel) {
    sel.value = subjectId;
    filterChaptersBySubject(subjectId);
  }
}

// Subject Dashboard Modal
function openSubjectDashboardModal(subjectId) {
  const s = currentData.subjects.find(item => item.id === subjectId);
  if (!s) return;

  const chapters = currentData.chapters.filter(c => c.subjectId === s.id);
  const classes = currentData.timetableClasses.filter(c => c.subjectId === s.id);
  const cancelled = s.cancelledClasses || 0;
  const absent = s.absentClasses || 0;
  const records = s.attendanceRecords || [];

  openModal({
    title: `${s.name} — Subject Overview`,
    body: `
      <div class="p-3 mb-4" style="background: ${s.color || 'var(--accent)'}15; border-left: 5px solid ${s.color || 'var(--accent)'}; border-radius: var(--radius-sm);">
        <h4 style="font-size: 18px; font-weight: 700; color: var(--text-primary); margin:0;">${escapeHtml(s.name)}</h4>
        <div class="text-sm mt-1" style="color: var(--text-secondary);">
          Teacher: <strong style="color: var(--text-primary);">${escapeHtml(s.teacherName || 'Not assigned')}</strong>
        </div>
      </div>

      <div class="dashboard-grid mb-4" style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
        <div class="card" style="padding: 14px; background: rgba(239, 68, 68, 0.08); border-left: 4px solid var(--danger);">
          <div class="text-xs text-muted">Total Cancelled Classes</div>
          <div style="font-size: 22px; font-weight: 800; color: var(--danger);">${cancelled}</div>
        </div>
        <div class="card" style="padding: 14px; background: rgba(245, 158, 11, 0.08); border-left: 4px solid var(--warning);">
          <div class="text-xs text-muted">Total Absences</div>
          <div style="font-size: 22px; font-weight: 800; color: var(--warning);">${absent}</div>
        </div>
      </div>

      <div class="flex items-center justify-between mb-4">
        <button class="btn btn-secondary btn-sm" onclick="closeModal(); openSubjectAttendanceHistoryModal('${s.id}')">
          ${getIconHtml('calendar')}
          <span>Manage Attendance & Cancellation Logs</span>
        </button>
      </div>

      <div class="card mb-4" style="padding: 14px;">
        <h5 style="font-size: 13.5px; font-weight: 700; margin-bottom: 8px;">📅 Scheduled Weekly Classes</h5>
        <div class="text-xs text-secondary">
          ${classes.length > 0 ? classes.map(c => `
            <div style="padding: 4px 0; border-bottom: 1px solid var(--border);">
              • <strong>${c.day}:</strong> ${c.startTime || ''} - ${c.endTime || ''} (Room ${escapeHtml(c.room || 'TBD')})
            </div>
          `).join('') : '<div class="text-muted">No classes scheduled in timetable.</div>'}
        </div>
      </div>

      <h5 style="font-size: 14px; font-weight: 700; margin-bottom: 8px;">Chapters List (${chapters.length})</h5>
      <div style="max-height: 180px; overflow-y: auto; margin-bottom: 16px; border: 1px solid var(--border); border-radius: var(--radius-sm);">
        ${chapters.length > 0 ? chapters.map(c => `
          <div class="flex items-center justify-between p-2" style="border-bottom: 1px solid var(--border); font-size: 12.5px;">
            <div>
              <span class="badge badge-gray" style="margin-right: 6px;">Ch ${c.chapterNumber}</span>
              <strong>${escapeHtml(c.name)}</strong>
            </div>
            <span class="badge ${c.status === 'Completed' ? 'badge-emerald' : 'badge-indigo'}">${c.status}</span>
          </div>
        `).join('') : '<div class="p-3 text-sm text-muted text-center">No chapters added yet.</div>'}
      </div>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Close</button>
    `
  });
}

function quickToggleChapter(chapterId) {
  const c = currentData.chapters.find(item => item.id === chapterId);
  if (!c) return;
  if (c.status === 'Completed') {
    c.status = 'In Progress';
    c.completionDate = '';
  } else {
    c.status = 'Completed';
    c.completionDate = new Date().toISOString().split('T')[0];
  }
  saveStorage();
  renderChapters();
  renderSubjects();
  renderDashboard();
  closeModal();
  openSubjectDashboardModal(c.subjectId);
}

function openSubjectModal(id = null) {
  const subject = id ? currentData.subjects.find(s => s.id === id) : null;
  const isEdit = !!subject;

  // Teacher options
  const teacherOptions = currentData.teachers.map(t => `
    <option value="${t.id}" ${subject && (subject.teacherId === t.id || subject.teacherName === t.name) ? 'selected' : ''}>${escapeHtml(t.name)}</option>
  `).join('');

  openModal({
    title: isEdit ? 'Edit Subject' : 'Add New Subject',
    body: `
      <form id="subject-form" onsubmit="handleSubjectFormSubmit(event, '${id || ''}')">
        <div class="form-group mb-3">
          <label>Subject Name *</label>
          <input type="text" class="form-control" id="sub-name" required value="${escapeHtml(subject ? subject.name : '')}" placeholder="e.g., Data Structures & Algorithms">
        </div>

        <div class="form-row">
          <div class="form-group" style="flex: 1;">
            <label>Assigned Teacher</label>
            <select class="form-control" id="sub-teacher">
              <option value="">-- Select or type teacher --</option>
              ${teacherOptions}
            </select>
          </div>
          <div class="form-group" style="flex: 1;">
            <label>Or Teacher Name</label>
            <input type="text" class="form-control" id="sub-teacher-custom" value="${escapeHtml(subject ? subject.teacherName || '' : '')}" placeholder="e.g. Dr. Sharma">
          </div>
        </div>

        <div class="form-row">
          <div class="form-group" style="flex: 1;">
            <label>Number of Cancelled Classes</label>
            <input type="number" class="form-control" id="sub-cancelled" min="0" value="${subject ? (subject.cancelledClasses || 0) : 0}">
          </div>
          <div class="form-group" style="flex: 1;">
            <label>Number of Absences</label>
            <input type="number" class="form-control" id="sub-absent" min="0" value="${subject ? (subject.absentClasses || 0) : 0}">
          </div>
        </div>

        <div class="form-group">
          <label>Theme Color</label>
          <input type="color" class="form-control" id="sub-color" value="${subject ? subject.color || '#4f46e5' : '#4f46e5'}" style="height: 38px; padding: 2px;">
        </div>
      </form>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="document.getElementById('subject-form').requestSubmit()">${isEdit ? 'Save Changes' : 'Create Subject'}</button>
    `
  });
}

function handleSubjectFormSubmit(e, editId) {
  e.preventDefault();
  const name = document.getElementById('sub-name').value.trim();
  if (!name) return;

  const teacherId = document.getElementById('sub-teacher').value;
  const customTeacher = document.getElementById('sub-teacher-custom').value.trim();
  const teacher = currentData.teachers.find(t => t.id === teacherId);
  const teacherName = customTeacher || (teacher ? teacher.name : '');

  const cancelledClasses = parseInt(document.getElementById('sub-cancelled').value) || 0;
  const absentClasses = parseInt(document.getElementById('sub-absent').value) || 0;
  const color = document.getElementById('sub-color').value || '#4f46e5';

  if (editId) {
    const s = currentData.subjects.find(item => item.id === editId);
    if (s) {
      s.name = name;
      s.teacherId = teacherId;
      s.teacherName = teacherName;
      s.cancelledClasses = cancelledClasses;
      s.absentClasses = absentClasses;
      s.color = color;
      logActivity(`Edited subject: "${name}"`);
    }
  } else {
    const newSubject = {
      id: 'sub-' + Date.now(),
      name,
      teacherId,
      teacherName,
      cancelledClasses,
      absentClasses,
      color,
      attendanceRecords: []
    };
    currentData.subjects.push(newSubject);
    logActivity(`Created subject: "${name}"`);
  }

  saveStorage();
  closeModal();
  renderSubjects();
  renderDashboard();
  showToast(editId ? 'Subject updated!' : 'Subject added!');
}

function deleteSubject(id) {
  const idx = currentData.subjects.findIndex(s => s.id === id);
  if (idx < 0) return;
  const deleted = currentData.subjects[idx];
  const prevSubjects = [...currentData.subjects];

  currentData.subjects.splice(idx, 1);
  saveStorage();
  renderSubjects();
  renderDashboard();
  logActivity(`Deleted subject: "${deleted.name}"`);

  showToast(`Subject "${deleted.name}" deleted.`, () => {
    currentData.subjects = prevSubjects;
    saveStorage();
    renderSubjects();
    renderDashboard();
    logActivity(`Undid deletion of subject: "${deleted.name}"`);
  });
}

/* =========================================================================
   CHAPTERS MANAGER
   ========================================================================= */

let chapterSubjectFilter = 'all';
let chapterSearchQuery = '';

function renderChapters() {
  const container = document.getElementById('chapters-container');
  const selectFilter = document.getElementById('chapter-subject-filter');
  if (!container) return;

  // Populate subject filter dropdown
  if (selectFilter) {
    selectFilter.innerHTML = `<option value="all">All Subjects (${currentData.chapters.length})</option>` +
      currentData.subjects.map(s => {
        const count = currentData.chapters.filter(c => c.subjectId === s.id).length;
        return `<option value="${s.id}" ${chapterSubjectFilter === s.id ? 'selected' : ''}>${escapeHtml(s.name)} (${count})</option>`;
      }).join('');
  }

  let filtered = [...currentData.chapters];

  if (chapterSubjectFilter !== 'all') {
    filtered = filtered.filter(c => c.subjectId === chapterSubjectFilter);
  }

  if (chapterSearchQuery) {
    const q = chapterSearchQuery.toLowerCase();
    filtered = filtered.filter(c => c.name.toLowerCase().includes(q) || (c.description && c.description.toLowerCase().includes(q)));
  }

  // Sort by chapter number
  filtered.sort((a, b) => (a.chapterNumber || 0) - (b.chapterNumber || 0));

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px;">
        <div style="font-size: 32px; margin-bottom: 8px;">📖</div>
        <h3 style="font-size: 15px; font-weight: 700;">No chapters found</h3>
        <p class="text-sm text-muted">Add chapters to map out your semester syllabus and study milestones.</p>
        <button class="btn btn-primary btn-sm mt-3" style="margin-top: 12px;" onclick="openChapterModal()">+ Add Chapter</button>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div style="overflow-x: auto;">
      <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px;">
        <thead>
          <tr style="border-bottom: 2px solid var(--border); background: var(--bg-input);">
            <th style="padding: 10px 14px;">Ch #</th>
            <th style="padding: 10px 14px;">Chapter Name & Scope</th>
            <th style="padding: 10px 14px;">Subject</th>
            <th style="padding: 10px 14px;">Difficulty</th>
            <th style="padding: 10px 14px;">Status & Progress</th>
            <th style="padding: 10px 14px;">Est / Actual</th>
            <th style="padding: 10px 14px; text-align: right;">Actions</th>
          </tr>
        </thead>
        <tbody>
          ${filtered.map(c => {
            const subject = currentData.subjects.find(s => s.id === c.subjectId);
            return `
              <tr style="border-bottom: 1px solid var(--border);">
                <td style="padding: 12px 14px; font-weight: 700; color: var(--accent);">
                  ${c.chapterNumber || '-'}
                </td>
                <td style="padding: 12px 14px; max-width: 260px;">
                  <div style="font-weight: 600; color: var(--text-primary); ${c.status === 'Completed' ? 'text-decoration: line-through; opacity: 0.7;' : ''}">
                    ${escapeHtml(c.name)}
                  </div>
                  <div class="text-xs text-muted" style="margin-top: 2px;">
                    ${escapeHtml(c.description || 'No notes')}
                  </div>
                </td>
                <td style="padding: 12px 14px;">
                  <span class="badge" style="background: ${subject ? subject.color + '22' : 'var(--bg-input)'}; color: ${subject ? subject.color : 'var(--text-primary)'}; font-weight: 600;">
                    ${escapeHtml(subject ? subject.name : 'Unassigned')}
                  </span>
                </td>
                <td style="padding: 12px 14px;">
                  <span class="badge ${c.difficulty === 'Hard' ? 'badge-rose' : c.difficulty === 'Medium' ? 'badge-amber' : 'badge-emerald'}">
                    ${c.difficulty || 'Medium'}
                  </span>
                </td>
                <td style="padding: 12px 14px;">
                  <span class="badge ${c.status === 'Completed' ? 'badge-emerald' : c.status === 'In Progress' ? 'badge-indigo' : 'badge-gray'}">${c.status}</span>
                </td>
                <td style="padding: 12px 14px; font-size: 12px; color: var(--text-secondary);">
                  ${c.estimatedStudyTime || 0}h / <strong>${c.actualStudyTime || 0}h</strong>
                </td>
                <td style="padding: 12px 14px; text-align: right;">
                  <div class="flex items-center justify-end gap-1">
                    <button class="btn btn-sm btn-secondary" onclick="quickToggleChapter('${c.id}')" title="Toggle Done">
                      ${c.status === 'Completed' ? 'Reopen' : 'Done'}
                    </button>
                    <button class="btn btn-icon btn-sm btn-secondary" onclick="openChapterModal('${c.id}')" title="Edit Chapter">${getIconHtml('edit')}</button>
                    <button class="btn btn-icon btn-sm btn-danger" onclick="deleteChapter('${c.id}')" title="Delete Chapter">${getIconHtml('trash')}</button>
                  </div>
                </td>
              </tr>
            `;
          }).join('')}
        </tbody>
      </table>
    </div>
  `;
}

function filterChaptersBySubject(subjectId) {
  chapterSubjectFilter = subjectId;
  renderChapters();
}

function searchChapters(val) {
  chapterSearchQuery = val;
  renderChapters();
}

function openChapterModal(id = null) {
  const chapter = id ? currentData.chapters.find(c => c.id === id) : null;
  const isEdit = !!chapter;

  const subjectOptions = currentData.subjects.map(s => `
    <option value="${s.id}" ${(chapter && chapter.subjectId === s.id) || (!chapter && chapterSubjectFilter === s.id) ? 'selected' : ''}>
      ${escapeHtml(s.name)}
    </option>
  `).join('');

  openModal({
    title: isEdit ? 'Edit Chapter' : 'Add New Chapter',
    body: `
      <form id="chapter-form" onsubmit="handleChapterFormSubmit(event, '${id || ''}')">
        <div class="form-row">
          <div class="form-group" style="flex: 1;">
            <label>Chapter Number *</label>
            <input type="number" class="form-control" id="ch-number" min="1" required value="${chapter ? chapter.chapterNumber : 1}">
          </div>
          <div class="form-group" style="flex: 3;">
            <label>Chapter Title *</label>
            <input type="text" class="form-control" id="ch-name" required value="${escapeHtml(chapter ? chapter.name : '')}" placeholder="e.g., AVL Trees and Rotations">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Subject</label>
            <select class="form-control" id="ch-subject" required>
              ${subjectOptions}
            </select>
          </div>
          <div class="form-group">
            <label>Difficulty</label>
            <select class="form-control" id="ch-difficulty">
              <option value="Easy" ${chapter && chapter.difficulty === 'Easy' ? 'selected' : ''}>Easy</option>
              <option value="Medium" ${!chapter || chapter.difficulty === 'Medium' ? 'selected' : ''}>Medium</option>
              <option value="Hard" ${chapter && chapter.difficulty === 'Hard' ? 'selected' : ''}>Hard</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group" style="flex: 1;">
            <label>Status</label>
            <select class="form-control" id="ch-status">
              <option value="Not Started" ${chapter && chapter.status === 'Not Started' ? 'selected' : ''}>Not Started</option>
              <option value="In Progress" ${!chapter || chapter.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
              <option value="Completed" ${chapter && chapter.status === 'Completed' ? 'selected' : ''}>Completed</option>
              <option value="Revision Required" ${chapter && chapter.status === 'Revision Required' ? 'selected' : ''}>Revision Required</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Est. Study Hours</label>
            <input type="number" class="form-control" id="ch-est" min="0" value="${chapter ? chapter.estimatedStudyTime || 0 : 10}">
          </div>
          <div class="form-group">
            <label>Actual Study Hours</label>
            <input type="number" class="form-control" id="ch-actual" min="0" value="${chapter ? chapter.actualStudyTime || 0 : 0}">
          </div>
        </div>
        <div class="form-group">
          <label>Description & Scope</label>
          <textarea class="form-control" id="ch-desc" placeholder="Topics covered in this chapter...">${escapeHtml(chapter ? chapter.description : '')}</textarea>
        </div>
        <div class="form-group">
          <label>Study Resources & Links</label>
          <input type="text" class="form-control" id="ch-resources" value="${escapeHtml(chapter ? chapter.resources || '' : '')}" placeholder="Book chapters, websites, slide URLs...">
        </div>
      </form>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="document.getElementById('chapter-form').requestSubmit()">${isEdit ? 'Save Chapter' : 'Add Chapter'}</button>
    `
  });
}

function handleChapterFormSubmit(e, editId) {
  e.preventDefault();
  const name = document.getElementById('ch-name').value.trim();
  if (!name) return;

  const number = parseInt(document.getElementById('ch-number').value) || 1;
  const subjectId = document.getElementById('ch-subject').value;
  const difficulty = document.getElementById('ch-difficulty').value;
  const status = document.getElementById('ch-status').value;
  const est = parseFloat(document.getElementById('ch-est').value) || 0;
  const actual = parseFloat(document.getElementById('ch-actual').value) || 0;
  const desc = document.getElementById('ch-desc').value.trim();
  const resources = document.getElementById('ch-resources').value.trim();

  if (editId) {
    const c = currentData.chapters.find(item => item.id === editId);
    if (c) {
      c.chapterNumber = number;
      c.name = name;
      c.subjectId = subjectId;
      c.difficulty = difficulty;
      c.status = status;
      c.estimatedStudyTime = est;
      c.actualStudyTime = actual;
      c.description = desc;
      c.resources = resources;
      if (status === 'Completed' && !c.completionDate) {
        c.completionDate = new Date().toISOString().split('T')[0];
      }
      logActivity(`Edited chapter: "${name}"`);
    }
  } else {
    const newChapter = {
      id: 'ch-' + Date.now(),
      chapterNumber: number,
      name,
      subjectId,
      difficulty,
      status,
      progress,
      estimatedStudyTime: est,
      actualStudyTime: actual,
      description: desc,
      resources,
      completionDate: status === 'Completed' ? new Date().toISOString().split('T')[0] : ''
    };
    currentData.chapters.push(newChapter);
    logActivity(`Added chapter: "${name}" to subject`);
  }

  saveStorage();
  closeModal();
  renderChapters();
  renderSubjects();
  renderDashboard();
  showToast(editId ? 'Chapter updated!' : 'Chapter added!');
}

function deleteChapter(id) {
  const idx = currentData.chapters.findIndex(c => c.id === id);
  if (idx < 0) return;
  const deleted = currentData.chapters[idx];
  const prevChapters = [...currentData.chapters];

  currentData.chapters.splice(idx, 1);
  saveStorage();
  renderChapters();
  renderSubjects();
  renderDashboard();
  logActivity(`Deleted chapter: "${deleted.name}"`);

  showToast(`Chapter "${deleted.name}" deleted.`, () => {
    currentData.chapters = prevChapters;
    saveStorage();
    renderChapters();
    renderSubjects();
    renderDashboard();
    logActivity(`Undid deletion of chapter: "${deleted.name}"`);
  });
}

/* =========================================================================
   TEACHERS & INSTRUCTORS
   ========================================================================= */

function renderTeachers() {
  const container = document.getElementById('teachers-cards-container');
  if (!container) return;

  if (currentData.teachers.length === 0) {
    container.innerHTML = `
      <div class="col-12 card" style="text-align: center; padding: 40px;">
        <div style="font-size: 36px; margin-bottom: 8px;">👨‍🏫</div>
        <h3 style="font-size: 16px; font-weight: 700;">No teachers added yet</h3>
        <p class="text-sm text-muted">Keep contact details, room numbers, and subject assignments handy.</p>
        <button class="btn btn-primary btn-sm mt-3" style="margin-top: 14px;" onclick="openTeacherModal()">+ Add Teacher</button>
      </div>
    `;
    return;
  }

  container.innerHTML = currentData.teachers.map(t => {
    const assignedSubjects = currentData.subjects.filter(s => s.teacherId === t.id);

    return `
      <div class="card col-4">
        <div class="card-header">
          <div>
            <h3 class="card-title" style="font-size: 15px;">${escapeHtml(t.name)}</h3>
            <div class="text-xs text-muted mt-1">${escapeHtml(t.department || 'Faculty Member')}</div>
          </div>
          <div class="flex items-center gap-1">
            <button class="btn btn-icon btn-sm btn-secondary" onclick="openTeacherModal('${t.id}')" title="Edit Teacher">${getIconHtml('edit')}</button>
            <button class="btn btn-icon btn-sm btn-danger" onclick="deleteTeacher('${t.id}')" title="Delete Teacher">${getIconHtml('trash')}</button>
          </div>
        </div>

        <div class="text-sm text-secondary mb-3" style="margin-bottom: 12px;">
          <div class="flex items-center gap-2 mb-1">
            <span>📍</span>
            <span>Room: <strong>${escapeHtml(t.room || 'N/A')}</strong></span>
          </div>
          ${t.phone ? `
            <div class="flex items-center gap-2 mb-1">
              <span>📞</span>
              <a href="tel:${t.phone}" style="color: var(--accent);">${escapeHtml(t.phone)}</a>
            </div>
          ` : ''}
          ${t.email ? `
            <div class="flex items-center gap-2 mb-1">
              <span>✉️</span>
              <a href="mailto:${t.email}" style="color: var(--accent);">${escapeHtml(t.email)}</a>
            </div>
          ` : ''}
        </div>

        <div class="mb-3">
          <div class="text-xs font-semibold text-muted mb-1">Assigned Subjects:</div>
          <div class="flex items-center gap-1 flex-wrap">
            ${assignedSubjects.length > 0 ? assignedSubjects.map(s => `
              <span class="badge" style="background: ${s.color}22; color: ${s.color}; font-weight: 600;">${escapeHtml(s.name)}</span>
            `).join('') : '<span class="text-xs text-muted">No subjects assigned</span>'}
          </div>
        </div>

        ${t.notes ? `
          <div class="text-xs text-muted" style="background: var(--bg-input); padding: 8px; border-radius: var(--radius-sm); font-style: italic;">
            ${escapeHtml(t.notes)}
          </div>
        ` : ''}
      </div>
    `;
  }).join('');
}

function openTeacherModal(id = null) {
  const teacher = id ? currentData.teachers.find(t => t.id === id) : null;
  const isEdit = !!teacher;

  openModal({
    title: isEdit ? 'Edit Teacher' : 'Add Teacher / Instructor',
    body: `
      <form id="teacher-form" onsubmit="handleTeacherFormSubmit(event, '${id || ''}')">
        <div class="form-group">
          <label>Full Name *</label>
          <input type="text" class="form-control" id="tech-name" required value="${escapeHtml(teacher ? teacher.name : '')}" placeholder="e.g., Nivesh Kumar">
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Department</label>
            <input type="text" class="form-control" id="tech-dept" value="${escapeHtml(teacher ? teacher.department || '' : 'Computer Science')}">
          </div>
          <div class="form-group">
            <label>Office / Room</label>
            <input type="text" class="form-control" id="tech-room" value="${escapeHtml(teacher ? teacher.room || '' : 'CS-415')}">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Phone Number</label>
            <input type="tel" class="form-control" id="tech-phone" value="${escapeHtml(teacher ? teacher.phone || '' : '')}" placeholder="+91 98765 43210">
          </div>
          <div class="form-group">
            <label>Email Address</label>
            <input type="email" class="form-control" id="tech-email" value="${escapeHtml(teacher ? teacher.email || '' : '')}" placeholder="prof@university.edu">
          </div>
        </div>
        <div class="form-group">
          <label>Office Hours & Notes</label>
          <textarea class="form-control" id="tech-notes" placeholder="Available office hours or project guidelines...">${escapeHtml(teacher ? teacher.notes || '' : '')}</textarea>
        </div>
      </form>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="document.getElementById('teacher-form').requestSubmit()">${isEdit ? 'Save Changes' : 'Add Teacher'}</button>
    `
  });
}

function handleTeacherFormSubmit(e, editId) {
  e.preventDefault();
  const name = document.getElementById('tech-name').value.trim();
  if (!name) return;

  const dept = document.getElementById('tech-dept').value.trim();
  const room = document.getElementById('tech-room').value.trim();
  const phone = document.getElementById('tech-phone').value.trim();
  const email = document.getElementById('tech-email').value.trim();
  const notes = document.getElementById('tech-notes').value.trim();

  if (editId) {
    const t = currentData.teachers.find(item => item.id === editId);
    if (t) {
      t.name = name;
      t.department = dept;
      t.room = room;
      t.phone = phone;
      t.email = email;
      t.notes = notes;
      logActivity(`Edited teacher: "${name}"`);
    }
  } else {
    const newTeacher = {
      id: 'tech-' + Date.now(),
      name,
      department: dept,
      room,
      phone,
      email,
      notes
    };
    currentData.teachers.push(newTeacher);
    logActivity(`Added teacher: "${name}"`);
  }

  saveStorage();
  closeModal();
  renderTeachers();
  renderDashboard();
  showToast(editId ? 'Teacher updated!' : 'Teacher added!');
}

function deleteTeacher(id) {
  const idx = currentData.teachers.findIndex(t => t.id === id);
  if (idx < 0) return;
  const deleted = currentData.teachers[idx];
  const prevTeachers = [...currentData.teachers];

  currentData.teachers.splice(idx, 1);
  saveStorage();
  renderTeachers();
  logActivity(`Deleted teacher: "${deleted.name}"`);

  showToast(`Teacher "${deleted.name}" deleted.`, () => {
    currentData.teachers = prevTeachers;
    saveStorage();
    renderTeachers();
    logActivity(`Undid deletion of teacher: "${deleted.name}"`);
  });
}

/* =========================================================================
   TIMETABLE VIEW (Customizable Columns = Days, Rows = Slots, Cells = Classes)
   ========================================================================= */

let draggedClassId = null;

function renderTimetable() {
  const container = document.getElementById('timetable-table-container');
  if (!container) return;

  const days = currentData.timetableDays || ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const slots = currentData.timetableSlots || [];

  if (days.length === 0 || slots.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px;">
        <h3>Timetable Grid is Empty</h3>
        <p class="text-sm text-muted">Add days and time slots to generate your timetable schedule grid.</p>
        <button class="btn btn-primary btn-sm mt-3" onclick="openTimetableGridModal()">Customize Grid</button>
      </div>
    `;
    return;
  }

  let html = `
    <table class="timetable-grid" id="main-timetable-grid">
      <thead>
        <tr>
          <th style="width: 120px;">Time Slot</th>
          ${days.map(d => `<th>${escapeHtml(d)}</th>`).join('')}
        </tr>
      </thead>
      <tbody>
  `;

  slots.forEach(slot => {
    html += `<tr>`;
    html += `<td class="timetable-slot-header"><strong>${escapeHtml(slot.label)}</strong></td>`;

    days.forEach(day => {
      const classItem = currentData.timetableClasses.find(c => c.day === day && c.slotId === slot.id);
      html += `
        <td class="timetable-cell" 
            data-day="${day}" 
            data-slot-id="${slot.id}"
            ondragover="handleTimetableDragOver(event)" 
            ondrop="handleTimetableDrop(event, '${day}', '${slot.id}')"
            onclick="handleTimetableCellClick('${day}', '${slot.id}')">
      `;

      if (classItem) {
        html += `
          <div class="timetable-class-card" 
               draggable="true" 
               ondragstart="handleTimetableDragStart(event, '${classItem.id}')"
               style="background: ${classItem.color || 'var(--accent)'}15; border-left: 4px solid ${classItem.color || 'var(--accent)'};"
               onclick="event.stopPropagation(); openTimetableClassModal('${classItem.id}')">
            <div class="timetable-class-title">${escapeHtml(classItem.subjectName)}</div>
            <div class="timetable-class-meta">
              <span>📍 ${escapeHtml(classItem.room || 'Room')}</span>
              <span>👨‍🏫 ${escapeHtml(classItem.teacherName || '')}</span>
            </div>
            ${classItem.notes ? `<div class="text-xs text-muted" style="margin-top: 3px; font-style: italic;">${escapeHtml(classItem.notes)}</div>` : ''}
          </div>
        `;
      } else {
        html += `<span class="text-xs text-muted" style="opacity: 0.4;">+ Schedule</span>`;
      }

      html += `</td>`;
    });

    html += `</tr>`;
  });

  html += `
      </tbody>
    </table>
  `;

  container.innerHTML = html;
}

// Drag and Drop Timetable handlers
function handleTimetableDragStart(e, classId) {
  draggedClassId = classId;
  e.dataTransfer.setData('text/plain', classId);
  e.dataTransfer.effectAllowed = 'move';
}

function handleTimetableDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  e.currentTarget.style.background = 'var(--accent-light)';
}

function handleTimetableDrop(e, targetDay, targetSlotId) {
  e.preventDefault();
  e.currentTarget.style.background = '';
  const classId = draggedClassId || e.dataTransfer.getData('text/plain');
  if (!classId) return;

  const classItem = currentData.timetableClasses.find(c => c.id === classId);
  if (!classItem) return;

  // Check if target cell is already occupied
  const existingInTarget = currentData.timetableClasses.find(c => c.day === targetDay && c.slotId === targetSlotId && c.id !== classId);
  if (existingInTarget) {
    // Swap slots!
    existingInTarget.day = classItem.day;
    existingInTarget.slotId = classItem.slotId;
  }

  classItem.day = targetDay;
  classItem.slotId = targetSlotId;

  saveStorage();
  renderTimetable();
  renderDashboard();
  showToast(`Moved "${classItem.subjectName}" to ${targetDay}`);
  draggedClassId = null;
}

function handleTimetableCellClick(day, slotId) {
  openTimetableClassModal(null, day, slotId);
}

function openTimetableClassModal(id = null, presetDay = null, presetSlotId = null) {
  const classItem = id ? currentData.timetableClasses.find(c => c.id === id) : null;
  const isEdit = !!classItem;

  const days = currentData.timetableDays;
  const slots = currentData.timetableSlots;

  const dayOptions = days.map(d => `
    <option value="${d}" ${(classItem && classItem.day === d) || (!classItem && presetDay === d) ? 'selected' : ''}>${d}</option>
  `).join('');

  const slotOptions = slots.map(s => `
    <option value="${s.id}" ${(classItem && classItem.slotId === s.id) || (!classItem && presetSlotId === s.id) ? 'selected' : ''}>${escapeHtml(s.label)}</option>
  `).join('');

  const subjectOptions = currentData.subjects.map(s => `
    <option value="${s.id}" ${classItem && classItem.subjectId === s.id ? 'selected' : ''} data-color="${s.color}" data-teacher="${s.teacherName}">${escapeHtml(s.name)}</option>
  `).join('');

  openModal({
    title: isEdit ? 'Edit Scheduled Class' : 'Schedule New Class',
    body: `
      <form id="tt-class-form" onsubmit="handleTimetableClassSubmit(event, '${id || ''}')">
        <div class="form-group">
          <label>Subject *</label>
          <select class="form-control" id="tt-subject" onchange="autoFillTimetableSubject(this)">
            <option value="">-- Choose Subject or Custom --</option>
            ${subjectOptions}
          </select>
        </div>
        <div class="form-group">
          <label>Display Subject Title *</label>
          <input type="text" class="form-control" id="tt-subject-name" required value="${escapeHtml(classItem ? classItem.subjectName : '')}" placeholder="e.g., Operating Systems Lecture">
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Day of Week</label>
            <select class="form-control" id="tt-day">
              ${dayOptions}
            </select>
          </div>
          <div class="form-group">
            <label>Time Slot</label>
            <select class="form-control" id="tt-slot">
              ${slotOptions}
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Instructor Name</label>
            <input type="text" class="form-control" id="tt-teacher" value="${escapeHtml(classItem ? classItem.teacherName || '' : '')}">
          </div>
          <div class="form-group">
            <label>Room / Hall</label>
            <input type="text" class="form-control" id="tt-room" value="${escapeHtml(classItem ? classItem.room || '' : '')}" placeholder="e.g., LH-3">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Color Accent</label>
            <input type="color" class="form-control" id="tt-color" value="${classItem ? classItem.color || '#4f46e5' : '#4f46e5'}" style="height: 38px; padding: 2px;">
          </div>
          <div class="form-group">
            <label class="checkbox-label" style="margin-top: 26px;">
              <input type="checkbox" id="tt-important" ${classItem && classItem.important ? 'checked' : ''}>
              <span>Important / Exam Review</span>
            </label>
          </div>
        </div>
        <div class="form-group">
          <label>Notes & Preparation</label>
          <textarea class="form-control" id="tt-notes" placeholder="e.g., Bring laptop with C++ compiler ready...">${escapeHtml(classItem ? classItem.notes || '' : '')}</textarea>
        </div>
      </form>
    `,
    footer: `
      ${isEdit ? `
        <button class="btn btn-secondary" onclick="duplicateTimetableClass('${classItem.id}')">Duplicate</button>
        <button class="btn btn-danger" onclick="deleteTimetableClass('${classItem.id}')">Delete</button>
      ` : ''}
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="document.getElementById('tt-class-form').requestSubmit()">${isEdit ? 'Save Changes' : 'Schedule Class'}</button>
    `
  });
}

function autoFillTimetableSubject(sel) {
  const opt = sel.selectedOptions[0];
  if (!opt || !opt.value) return;
  const nameEl = document.getElementById('tt-subject-name');
  const teacherEl = document.getElementById('tt-teacher');
  const colorEl = document.getElementById('tt-color');

  if (nameEl) nameEl.value = opt.textContent.trim();
  if (teacherEl && opt.getAttribute('data-teacher')) teacherEl.value = opt.getAttribute('data-teacher');
  if (colorEl && opt.getAttribute('data-color')) colorEl.value = opt.getAttribute('data-color');
}

function handleTimetableClassSubmit(e, editId) {
  e.preventDefault();
  const subjectName = document.getElementById('tt-subject-name').value.trim();
  if (!subjectName) return;

  const subjectId = document.getElementById('tt-subject').value;
  const day = document.getElementById('tt-day').value;
  const slotId = document.getElementById('tt-slot').value;
  const teacherName = document.getElementById('tt-teacher').value.trim();
  const room = document.getElementById('tt-room').value.trim();
  const color = document.getElementById('tt-color').value;
  const important = document.getElementById('tt-important').checked;
  const notes = document.getElementById('tt-notes').value.trim();

  if (editId) {
    const c = currentData.timetableClasses.find(item => item.id === editId);
    if (c) {
      c.subjectName = subjectName;
      c.subjectId = subjectId;
      c.day = day;
      c.slotId = slotId;
      c.teacherName = teacherName;
      c.room = room;
      c.color = color;
      c.important = important;
      c.notes = notes;
      logActivity(`Updated class: "${subjectName}" on ${day}`);
    }
  } else {
    // Remove any existing class in the same slot to prevent overlaps
    currentData.timetableClasses = currentData.timetableClasses.filter(c => !(c.day === day && c.slotId === slotId));

    const newClass = {
      id: 'tc-' + Date.now(),
      subjectName,
      subjectId,
      day,
      slotId,
      teacherName,
      room,
      color,
      important,
      notes
    };
    currentData.timetableClasses.push(newClass);
    logActivity(`Scheduled class: "${subjectName}" on ${day}`);
  }

  saveStorage();
  closeModal();
  renderTimetable();
  renderDashboard();
  showToast(editId ? 'Class schedule updated!' : 'Class scheduled!');
}

function duplicateTimetableClass(id) {
  const c = currentData.timetableClasses.find(item => item.id === id);
  if (!c) return;

  const dup = {
    ...c,
    id: 'tc-' + Date.now(),
    subjectName: c.subjectName + ' (Copy)'
  };
  currentData.timetableClasses.push(dup);
  saveStorage();
  closeModal();
  renderTimetable();
  showToast('Class duplicated. You can drag it to any other cell.');
}

function deleteTimetableClass(id) {
  const idx = currentData.timetableClasses.findIndex(c => c.id === id);
  if (idx < 0) return;
  const deleted = currentData.timetableClasses[idx];
  const prevClasses = [...currentData.timetableClasses];

  currentData.timetableClasses.splice(idx, 1);
  saveStorage();
  closeModal();
  renderTimetable();
  renderDashboard();
  logActivity(`Removed class: "${deleted.subjectName}" from ${deleted.day}`);

  showToast(`Removed "${deleted.subjectName}"`, () => {
    currentData.timetableClasses = prevClasses;
    saveStorage();
    renderTimetable();
    renderDashboard();
    logActivity(`Undid removal of class: "${deleted.subjectName}"`);
  });
}

function clearTimetableConfirmation() {
  openModal({
    title: 'Clear Timetable Grid',
    body: `
      <p class="text-sm text-secondary">Are you sure you want to clear all scheduled classes from the timetable grid? Days and time slot definitions will be preserved.</p>
    `,
    footer: `
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-danger" onclick="confirmClearTimetable()">Clear All Classes</button>
    `
  });
}

function confirmClearTimetable() {
  const prev = [...currentData.timetableClasses];
  currentData.timetableClasses = [];
  saveStorage();
  closeModal();
  renderTimetable();
  renderDashboard();
  logActivity('Cleared all classes from timetable grid.');

  showToast('Timetable grid cleared.', () => {
    currentData.timetableClasses = prev;
    saveStorage();
    renderTimetable();
    renderDashboard();
    logActivity('Undid clearing timetable.');
  });
}

// Timetable Grid Customization Modal (Days & Slots)
function openTimetableGridModal() {
  const days = currentData.timetableDays || [];
  const slots = currentData.timetableSlots || [];

  openModal({
    title: 'Customize Days & Time Slots',
    body: `
      <div class="mb-4">
        <div class="flex items-center justify-between mb-2">
          <label style="font-weight: 700; margin:0;">Active Schedule Days (${days.length})</label>
          <button class="btn btn-sm btn-secondary" onclick="addTimetableDayPrompt()">+ Add Day</button>
        </div>
        <div class="flex items-center gap-2 flex-wrap" id="tt-custom-days-list">
          ${days.map(d => `
            <span class="badge badge-indigo" style="padding: 6px 10px; font-size: 13px; display: inline-flex; align-items: center; gap: 6px;">
              ${escapeHtml(d)}
              <span style="cursor: pointer; font-weight: bold;" onclick="removeTimetableDay('${d}')">✕</span>
            </span>
          `).join('')}
        </div>
      </div>

      <div class="sidebar-divider"></div>

      <div class="mb-3">
        <div class="flex items-center justify-between mb-2">
          <label style="font-weight: 700; margin:0;">Time Slots Rows (${slots.length})</label>
          <button class="btn btn-sm btn-secondary" onclick="addTimetableSlotPrompt()">+ Add Time Slot</button>
        </div>
        <div style="max-height: 180px; overflow-y: auto;">
          ${slots.map(s => `
            <div class="flex items-center justify-between p-2 mb-1" style="background: var(--bg-input); border-radius: var(--radius-sm);">
              <strong>${escapeHtml(s.label)}</strong>
              <button class="btn btn-sm btn-danger" onclick="removeTimetableSlot('${s.id}')">Delete</button>
            </div>
          `).join('')}
        </div>
      </div>
    `,
    footer: `
      <button class="btn btn-primary" onclick="closeModal()">Done</button>
    `
  });
}

function addTimetableDayPrompt() {
  const day = prompt('Enter day name (e.g., Sunday):');
  if (!day || !day.trim()) return;
  const clean = day.trim();
  if (!currentData.timetableDays.includes(clean)) {
    currentData.timetableDays.push(clean);
    saveStorage();
    renderTimetable();
    openTimetableGridModal();
  }
}

function removeTimetableDay(day) {
  if (currentData.timetableDays.length <= 1) {
    showToast('Cannot remove all days!', null, 'danger');
    return;
  }
  currentData.timetableDays = currentData.timetableDays.filter(d => d !== day);
  currentData.timetableClasses = currentData.timetableClasses.filter(c => c.day !== day);
  saveStorage();
  renderTimetable();
  openTimetableGridModal();
}

function addTimetableSlotPrompt() {
  const start = prompt('Enter start time (e.g. 04:00 PM or 16:00):');
  if (!start) return;
  const end = prompt('Enter end time (e.g. 05:00 PM or 17:00):');
  if (!end) return;

  const newSlot = {
    id: 'ts-' + Date.now(),
    label: `${start.trim()} - ${end.trim()}`,
    start: start.trim(),
    end: end.trim()
  };
  currentData.timetableSlots.push(newSlot);
  saveStorage();
  renderTimetable();
  openTimetableGridModal();
}

function removeTimetableSlot(slotId) {
  if (currentData.timetableSlots.length <= 1) {
    showToast('Cannot remove all slots!', null, 'danger');
    return;
  }
  currentData.timetableSlots = currentData.timetableSlots.filter(s => s.id !== slotId);
  currentData.timetableClasses = currentData.timetableClasses.filter(c => c.slotId !== slotId);
  saveStorage();
  renderTimetable();
  openTimetableGridModal();
}
"""
