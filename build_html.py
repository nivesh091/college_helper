# HTML markup module for StudyPulse
html_body = """
  <div id="app">
    <!-- Header -->
    <header id="app-header">
      <div class="header-left flex items-center gap-2" style="position: relative;">
        <!-- Left Three Dots Menu Button -->
        <button id="left-dots-btn" class="btn btn-secondary btn-icon left-dots-btn" onclick="toggleLeftDotsMenu(event)" title="Options & Documents" aria-label="More Options">
          <span class="icon-slot" data-icon="more-vertical"></span>
        </button>

        <!-- Left Three Dots Dropdown Menu -->
        <div id="left-dots-menu" class="left-dots-dropdown" style="display:none;" onclick="event.stopPropagation()">
          <div class="left-dots-menu-header">
            <span>Quick Options</span>
            <button class="left-dots-close-btn" onclick="closeLeftDotsMenu()">&times;</button>
          </div>
          <div class="left-dots-menu-body">
            <!-- OPTION UNDER LEFT THREE DOTS TO UPLOAD DOCUMENTS -->
            <button class="left-dots-item primary-action" onclick="openUploadDocumentsModal(); closeLeftDotsMenu();">
              <div class="item-icon-wrap upload-accent">
                <span class="icon-slot" data-icon="upload"></span>
              </div>
              <div class="item-text-group">
                <span class="item-title">Upload Documents</span>
                <span class="item-subtitle">Upload PDFs, notes & syllabus</span>
              </div>
            </button>
            <button class="left-dots-item" onclick="openDocumentsLibraryModal(); closeLeftDotsMenu();">
              <div class="item-icon-wrap">
                <span class="icon-slot" data-icon="file"></span>
              </div>
              <div class="item-text-group">
                <span class="item-title">Document Library</span>
                <span class="item-subtitle" id="left-docs-count-label">Browse uploaded study files</span>
              </div>
            </button>
            <div class="left-dots-divider"></div>
            <button class="left-dots-item" onclick="openTopSubjectsModal(); closeLeftDotsMenu();">
              <div class="item-icon-wrap">
                <span class="icon-slot" data-icon="book-open"></span>
              </div>
              <div class="item-text-group">
                <span class="item-title">Subjects & Teachers</span>
                <span class="item-subtitle">View courses & faculty</span>
              </div>
            </button>
            <button class="left-dots-item" onclick="openQuickAddModal(); closeLeftDotsMenu();">
              <div class="item-icon-wrap">
                <span class="icon-slot" data-icon="plus"></span>
              </div>
              <div class="item-text-group">
                <span class="item-title">Quick Add</span>
                <span class="item-subtitle">Add task, goal, note, habit</span>
              </div>
            </button>
            <div class="left-dots-divider"></div>
            <button class="left-dots-item" id="left-dots-install-btn" onclick="triggerPWAInstall(); closeLeftDotsMenu();">
              <div class="item-icon-wrap" style="color: var(--primary, #4f46e5); background: rgba(79, 70, 229, 0.12);">
                <span class="icon-slot" data-icon="download"></span>
              </div>
              <div class="item-text-group">
                <span class="item-title">Install as App</span>
                <span class="item-subtitle">Install on Phone, Tablet or PC</span>
              </div>
            </button>
            <button class="left-dots-item" onclick="navigateTo('settings'); closeLeftDotsMenu();">
              <div class="item-icon-wrap">
                <span class="icon-slot" data-icon="settings"></span>
              </div>
              <div class="item-text-group">
                <span class="item-title">Settings & Backup</span>
                <span class="item-subtitle">Preferences, theme, data export</span>
              </div>
            </button>
            <div class="left-dots-divider"></div>
            <button class="left-dots-item" onclick="navigateTo('dashboard'); setTimeout(() => { const el = document.getElementById('developer-card-section'); if (el) el.scrollIntoView({ behavior: 'smooth' }); }, 150); closeLeftDotsMenu();">
              <div class="item-icon-wrap" style="color: #6366f1; background: rgba(99, 102, 241, 0.12);">
                <span class="icon-slot" data-icon="user"></span>
              </div>
              <div class="item-text-group">
                <span class="item-title">Developer Profile</span>
                <span class="item-subtitle">Hi, I'm Nivesh Kumar</span>
              </div>
            </button>
          </div>
        </div>

        <button id="global-back-btn" class="btn btn-secondary btn-icon" onclick="goBack()" aria-label="Go Back" title="Go back one step" style="display:none; margin-right: 6px;">
          <span class="icon-slot" data-icon="arrow-left"></span>
        </button>
        <button id="mobile-menu-btn" class="btn btn-secondary btn-icon" style="display:none;" onclick="toggleMobileSidebar()" aria-label="Toggle Navigation">
          <span class="icon-slot" data-icon="menu"></span>
        </button>
        <!-- Live Clock in Logo Space (Desktop & Mobile) -->
        <div id="header-logo-clock" class="header-logo-clock" onclick="navigateTo('dashboard'); return false;" title="Live Time - Click to go to Dashboard">
          <div class="logo-clock-badge">
            <span class="logo-clock-dot"></span>
            <span class="icon-slot" data-icon="clock"></span>
          </div>
          <div class="logo-clock-content">
            <div class="logo-clock-time" id="live-time">--:--:--</div>
            <div class="logo-clock-date" id="live-date">Loading date...</div>
          </div>
        </div>
      </div>

      <div class="header-actions">

        <!-- Subjects Button at top side besides (Nivesh icon) -->
        <button class="topbar-subjects-pill" id="topbar-subjects-btn" onclick="openTopSubjectsModal()" title="View all courses and faculty">
          <span class="icon-slot" data-icon="book-open"></span>
          <span class="topbar-subjects-text">Subjects</span>
          <span class="badge-count" id="topbar-subjects-count">0</span>
          <span class="icon-slot" data-icon="chevron-down"></span>
        </button>

        <!-- Profile Selector Pill (Nivesh) -->
        <div class="profile-pill" onclick="openProfileModal()" title="Switch or manage profiles">
          <div class="profile-avatar" id="current-profile-avatar" style="overflow: hidden; padding: 0;">
            <img src="myimage.jpg" alt="NK" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover;" onerror="this.style.display='none'; this.parentElement.textContent='N';">
          </div>
          <span id="current-profile-name">Nivesh</span>
          <span class="icon-slot" data-icon="chevron-down"></span>
        </div>

        <!-- Theme Toggle -->
        <button id="theme-toggle-btn" class="btn btn-secondary btn-icon" onclick="cycleTheme()" title="Toggle Theme (Light / Dark / System)">
          <span id="theme-icon-slot" class="icon-slot" data-icon="sun"></span>
        </button>

        <!-- Install App Button -->
        <button id="header-install-btn" class="btn btn-secondary btn-icon" onclick="triggerPWAInstall()" title="Install StudyPulse App">
          <span class="icon-slot" data-icon="download"></span>
        </button>

        <!-- Settings Button -->
        <button class="btn btn-secondary btn-icon header-settings-btn" onclick="navigateTo('settings')" title="Settings">
          <span class="icon-slot" data-icon="settings"></span>
        </button>

        <!-- Auto-save Pill -->
        <div id="save-indicator">
          <span class="icon-slot" data-icon="check"></span>
          <span>Saved</span>
        </div>
      </div>
    </header>

    <div id="app-shell">
      <!-- Desktop Sidebar -->
      <aside id="sidebar">
        <div class="sidebar-nav">
          <div class="sidebar-section-title">Overview</div>
          <a class="nav-link" data-view="dashboard" onclick="navigateTo('dashboard')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="layout-dashboard"></span>
              <span>Dashboard</span>
            </div>
          </a>
          <a class="nav-link" data-view="planner" onclick="navigateTo('planner')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="calendar-days"></span>
              <span>Planner</span>
            </div>
          </a>
          <a class="nav-link" data-view="calendar" onclick="navigateTo('calendar')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="calendar"></span>
              <span>Calendar</span>
            </div>
            <span class="nav-badge" id="badge-calendar-events">0</span>
          </a>

          <div class="sidebar-divider"></div>
          <div class="sidebar-section-title">Academic</div>
          
          <a class="nav-link" data-view="subjects" onclick="navigateTo('subjects')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="book-open"></span>
              <span>Subjects</span>
            </div>
            <span class="nav-badge" id="badge-subjects">0</span>
          </a>
          <a class="nav-link" data-view="chapters" onclick="navigateTo('chapters')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="list-tree"></span>
              <span>Chapters</span>
            </div>
            <span class="nav-badge" id="badge-chapters">0</span>
          </a>
          <a class="nav-link" data-view="teachers" onclick="navigateTo('teachers')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="users"></span>
              <span>Teachers</span>
            </div>
            <span class="nav-badge" id="badge-teachers">0</span>
          </a>
          <a class="nav-link" data-view="timetable" onclick="navigateTo('timetable')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="table"></span>
              <span>Timetable</span>
            </div>
          </a>

          <div class="sidebar-divider"></div>
          <div class="sidebar-section-title">Productivity</div>

          <a class="nav-link" data-view="goals" onclick="navigateTo('goals')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="target"></span>
              <span>Goals</span>
            </div>
            <span class="nav-badge" id="badge-goals">0</span>
          </a>
          <a class="nav-link" data-view="todos" onclick="navigateTo('todos')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="check-square"></span>
              <span>To-Do List</span>
            </div>
            <span class="nav-badge" id="badge-todos">0</span>
          </a>
          <a class="nav-link" data-view="habits" onclick="navigateTo('habits')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="flame"></span>
              <span>Habits</span>
            </div>
            <span class="nav-badge" id="badge-habits">0</span>
          </a>
          <a class="nav-link" data-view="timer" onclick="navigateTo('timer')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="timer"></span>
              <span>Study Timer</span>
            </div>
          </a>

          <div class="sidebar-divider"></div>
          <div class="sidebar-section-title">Knowledge & Media</div>

          <a class="nav-link" data-view="notes" onclick="navigateTo('notes')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="file-text"></span>
              <span>Notes</span>
            </div>
            <span class="nav-badge" id="badge-notes">0</span>
          </a>
          <a class="nav-link" data-view="documents" onclick="openDocumentsLibraryModal()">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="file"></span>
              <span>Documents</span>
            </div>
            <span class="nav-badge" id="badge-documents">0</span>
          </a>
          <a class="nav-link" data-view="playlists" onclick="navigateTo('playlists')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="video"></span>
              <span>Video Playlists</span>
            </div>
            <span class="nav-badge" id="badge-videos">0</span>
          </a>
          <a class="nav-link" data-view="statistics" onclick="navigateTo('statistics')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="bar-chart-3"></span>
              <span>Statistics</span>
            </div>
          </a>
          <a class="nav-link" data-view="settings" onclick="navigateTo('settings')">
            <div class="nav-link-content">
              <span class="icon-slot" data-icon="settings"></span>
              <span>Settings & About us</span>
            </div>
          </a>
        </div>
      </aside>

      <!-- Main Content Area -->
      <main id="main-content">
        <!-- 1. DASHBOARD VIEW -->
        <section id="view-dashboard" class="view-container active">
          <div class="view-header">
            <div class="view-title-group">
              <h1>Welcome Back, <span id="dash-greeting-name">Scholar</span> 👋</h1>
              <p>Here is your comprehensive study and productivity summary for today.</p>
            </div>
            <div class="view-actions">
              <button class="btn btn-secondary btn-sm" onclick="openDashboardCustomizeModal()">
                <span class="icon-slot" data-icon="sliders"></span>
                <span>Customize Dashboard</span>
              </button>
              <button class="btn btn-primary btn-sm" onclick="openQuickAddModal()">
                <span class="icon-slot" data-icon="plus"></span>
                <span>Quick Add</span>
              </button>
            </div>
          </div>

          <!-- Top Quick Stat Summary Pills -->
          <div class="stat-summary-row" id="dashboard-stat-summary">
            <!-- Rendered by JS -->
          </div>

          <!-- Customizable Widgets Container -->
          <div class="dashboard-grid" id="dashboard-widgets-container">
            <!-- Rendered dynamically by JS based on user preferences and order -->
          </div>
        </section>

        <!-- 2. GOALS VIEW -->
        <section id="view-goals" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>Goals Manager</h1>
              <p>Set, track, prioritize, and conquer your academic and personal goals.</p>
            </div>
            <div class="view-actions">
              <button class="btn btn-secondary btn-sm" id="btn-merge-goals" onclick="openMergeGoalsModal()" style="display:none;">
                <span class="icon-slot" data-icon="git-merge"></span>
                <span id="merge-count-label">Merge Selected (0)</span>
              </button>
              <button class="btn btn-primary btn-sm" onclick="openGoalModal()">
                <span class="icon-slot" data-icon="plus"></span>
                <span>Add Goal</span>
              </button>
            </div>
          </div>

          <!-- Filter & Search Toolbar -->
          <div class="card mb-4" style="margin-bottom: 20px;">
            <div class="flex items-center justify-between flex-wrap gap-3">
              <div class="flex items-center gap-2 flex-wrap">
                <button class="btn btn-sm btn-secondary active-filter" data-goal-filter="all" onclick="filterGoals('all')">All</button>
                <button class="btn btn-sm btn-secondary" data-goal-filter="important" onclick="filterGoals('important')">⭐ Important</button>
                <button class="btn btn-sm btn-secondary" data-goal-filter="pending" onclick="filterGoals('pending')">In Progress</button>
                <button class="btn btn-sm btn-secondary" data-goal-filter="completed" onclick="filterGoals('completed')">Completed</button>
                <button class="btn btn-sm btn-secondary" data-goal-filter="today" onclick="filterGoals('today')">Due Today</button>
                <button class="btn btn-sm btn-secondary" data-goal-filter="week" onclick="filterGoals('week')">This Week</button>
              </div>
              <div class="flex items-center gap-2">
                <select class="form-control" style="width: auto; font-size: 12px; padding: 5px 10px;" onchange="sortGoals(this.value)">
                  <option value="deadline">Sort by Deadline</option>
                  <option value="priority">Sort by Priority</option>
                  <option value="progress">Sort by Progress</option>
                  <option value="title">Sort by Title</option>
                  <option value="created">Recently Created</option>
                </select>
                <input type="text" class="form-control" placeholder="Search goals..." style="width: 180px; font-size: 12px; padding: 5px 10px;" oninput="searchGoals(this.value)">
              </div>
            </div>
          </div>

          <div id="goals-list-container" class="dashboard-grid">
            <!-- Rendered by JS -->
          </div>
        </section>

        <!-- 3. TO-DO VIEW -->
        <section id="view-todos" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>To-Do Task Manager</h1>
              <p>Organize daily actionable tasks, checklists, and recurring study duties.</p>
            </div>
            <div class="view-actions">
              <button class="btn btn-primary btn-sm" onclick="openTaskModal()">
                <span class="icon-slot" data-icon="plus"></span>
                <span>Add Task</span>
              </button>
            </div>
          </div>

          <!-- Filter & Category Toolbar -->
          <div class="card mb-4" style="margin-bottom: 20px;">
            <div class="flex items-center justify-between flex-wrap gap-3">
              <div class="flex items-center gap-2 flex-wrap" id="todo-category-pills">
                <!-- Rendered by JS -->
              </div>
              <div class="flex items-center gap-2">
                <select class="form-control" style="width: auto; font-size: 12px; padding: 5px 10px;" onchange="filterTodoStatus(this.value)">
                  <option value="all">All Tasks</option>
                  <option value="pending">Pending</option>
                  <option value="today">Due Today</option>
                  <option value="completed">Completed</option>
                  <option value="high">High & Critical</option>
                </select>
                <input type="text" class="form-control" placeholder="Search tasks..." style="width: 180px; font-size: 12px; padding: 5px 10px;" oninput="searchTasks(this.value)">
              </div>
            </div>
          </div>

          <div class="card">
            <div id="todos-list-container">
              <!-- Rendered by JS -->
            </div>
          </div>
        </section>

        <!-- 4. SUBJECTS VIEW -->
        <section id="view-subjects" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>Subjects & Course Manager</h1>
              <p>Manage curriculum, enrolled courses, syllabus progress, and teacher assignments.</p>
            </div>
            <div class="view-actions">
              <button class="btn btn-primary btn-sm" onclick="openSubjectModal()">
                <span class="icon-slot" data-icon="plus"></span>
                <span>Add Subject</span>
              </button>
            </div>
          </div>

          <div class="dashboard-grid" id="subjects-cards-container">
            <!-- Rendered by JS -->
          </div>
        </section>

        <!-- 5. CHAPTERS VIEW -->
        <section id="view-chapters" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>Chapters & Syllabus Manager</h1>
              <p>Track detailed chapter progress, revision needs, study hours, and resource links.</p>
            </div>
            <div class="view-actions">
              <button class="btn btn-primary btn-sm" onclick="openChapterModal()">
                <span class="icon-slot" data-icon="plus"></span>
                <span>Add Chapter</span>
              </button>
            </div>
          </div>

          <!-- Subject filter bar -->
          <div class="card mb-4" style="margin-bottom: 20px;">
            <div class="flex items-center justify-between flex-wrap gap-3">
              <div class="flex items-center gap-2">
                <label style="margin:0; font-size:13px; font-weight:600;">Filter by Subject:</label>
                <select class="form-control" id="chapter-subject-filter" style="width: auto;" onchange="filterChaptersBySubject(this.value)">
                  <!-- Options populated by JS -->
                </select>
              </div>
              <input type="text" class="form-control" placeholder="Search chapters..." style="width: 200px; font-size: 12px; padding: 5px 10px;" oninput="searchChapters(this.value)">
            </div>
          </div>

          <div class="card" id="chapters-container">
            <!-- Rendered by JS as responsive table or cards -->
          </div>
        </section>

        <!-- 6. TEACHERS VIEW -->
        <section id="view-teachers" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>Teachers & Instructors</h1>
              <p>Directory of professors, advisors, office rooms, and assigned subjects.</p>
            </div>
            <div class="view-actions">
              <button class="btn btn-primary btn-sm" onclick="openTeacherModal()">
                <span class="icon-slot" data-icon="plus"></span>
                <span>Add Teacher</span>
              </button>
            </div>
          </div>

          <div class="dashboard-grid" id="teachers-cards-container">
            <!-- Rendered by JS -->
          </div>
        </section>

        <!-- 7. TIMETABLE VIEW -->
        <section id="view-timetable" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>Weekly Timetable Grid</h1>
              <p>Fully customizable schedule: Columns = Days, Rows = Time Slots, Cells = Classes with Drag & Drop.</p>
            </div>
            <div class="view-actions">
              <button class="btn btn-secondary btn-sm" onclick="openTimetableGridModal()">
                <span class="icon-slot" data-icon="sliders"></span>
                <span>Customize Days & Slots</span>
              </button>
              <button class="btn btn-primary btn-sm" onclick="openTimetableClassModal()">
                <span class="icon-slot" data-icon="plus"></span>
                <span>Add Class</span>
              </button>
            </div>
          </div>

          <div class="timetable-wrapper">
            <div class="timetable-toolbar">
              <div class="flex items-center gap-2">
                <span class="badge badge-indigo">Drag & Drop Supported</span>
                <span class="text-xs text-muted">Click any cell to schedule a class</span>
              </div>
              <div class="flex items-center gap-2">
                <button class="btn btn-secondary btn-sm" onclick="clearTimetableConfirmation()">Clear Grid</button>
              </div>
            </div>
            <div class="timetable-scroll-container" id="timetable-table-container">
              <!-- Rendered by JS: Complete custom grid -->
            </div>
          </div>
        </section>

        <!-- 8. CALENDAR VIEW -->
        <section id="view-calendar" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>Academic Calendar</h1>
              <p>Keep track of exams, assignment deadlines, events, and study milestones.</p>
            </div>
            <div class="view-actions">
              <button class="btn btn-primary btn-sm" onclick="openCalendarEventModal()">
                <span class="icon-slot" data-icon="plus"></span>
                <span>Add Event</span>
              </button>
            </div>
          </div>

          <div class="calendar-wrapper">
            <div class="flex items-center justify-between mb-4 flex-wrap gap-2" style="margin-bottom: 16px;">
              <div class="flex items-center gap-2">
                <button class="btn btn-secondary btn-sm" onclick="changeCalendarMonth(-1)">&larr; Prev</button>
                <button class="btn btn-secondary btn-sm" onclick="resetCalendarToToday()">Today</button>
                <button class="btn btn-secondary btn-sm" onclick="changeCalendarMonth(1)">Next &rarr;</button>
                <h2 id="calendar-month-year" style="font-size: 16px; font-weight: 700; margin-left: 8px;">Month Year</h2>
              </div>
              <div class="flex items-center gap-2">
                <span class="badge badge-rose">Exam</span>
                <span class="badge badge-amber">Assignment</span>
                <span class="badge badge-indigo">Goal Deadline</span>
                <span class="badge badge-emerald">Task</span>
              </div>
            </div>
            <div id="calendar-view-container">
              <!-- Rendered by JS -->
            </div>
          </div>
        </section>

        <!-- 9. PLANNER VIEW (Daily & Weekly) -->
        <section id="view-planner" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>Daily & Weekly Planner</h1>
              <p>Structure each day with connected timetable classes, tasks, habits, and study goals.</p>
            </div>
            <div class="view-actions">
              <div class="flex items-center gap-2">
                <button class="btn btn-secondary btn-sm active-planner-tab" id="btn-planner-daily" onclick="switchPlannerTab('daily')">Daily Planner</button>
                <button class="btn btn-secondary btn-sm" id="btn-planner-weekly" onclick="switchPlannerTab('weekly')">Weekly Planner</button>
              </div>
            </div>
          </div>

          <div id="planner-content-container">
            <!-- Rendered by JS -->
          </div>
        </section>

        <!-- 10. NOTES VIEW -->
        <section id="view-notes" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>General Notes & Study Docs</h1>
              <p>In-depth study notes, topic summaries, lecture takeaways, and formulas.</p>
            </div>
            <div class="view-actions">
              <button class="btn btn-primary btn-sm" onclick="openNoteModal()">
                <span class="icon-slot" data-icon="plus"></span>
                <span>Create Note</span>
              </button>
            </div>
          </div>

          <div class="card mb-4" style="margin-bottom: 20px;">
            <div class="flex items-center justify-between flex-wrap gap-3">
              <div class="flex items-center gap-2">
                <input type="text" class="form-control" placeholder="Search notes..." style="width: 220px; font-size: 12px; padding: 5px 10px;" oninput="searchNotes(this.value)">
                <select class="form-control" id="notes-subject-filter" style="width: auto; font-size: 12px; padding: 5px 10px;" onchange="filterNotesBySubject(this.value)">
                  <!-- Populated by JS -->
                </select>
              </div>
            </div>
          </div>

          <div class="dashboard-grid" id="notes-cards-container">
            <!-- Rendered by JS -->
          </div>
        </section>

        <!-- 12. PLAYLISTS VIEW -->
        <section id="view-playlists" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>Learning Video Playlists</h1>
              <p>Curate lecture series, YouTube tutorials with custom titles, notes, and watch progress.</p>
            </div>
            <div class="view-actions">
              <button class="btn btn-secondary btn-sm" onclick="openPlaylistModal()">
                <span class="icon-slot" data-icon="folder-plus"></span>
                <span>New Playlist</span>
              </button>
              <button class="btn btn-primary btn-sm" onclick="openVideoModal()">
                <span class="icon-slot" data-icon="video"></span>
                <span>Add Video</span>
              </button>
            </div>
          </div>

          <div id="playlists-main-container">
            <!-- Rendered by JS -->
          </div>
        </section>

        <!-- 13. HABITS VIEW -->
        <section id="view-habits" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>Daily Study Habits & Streaks</h1>
              <p>Build consistent study routines, problem-solving habits, and track completion streaks.</p>
            </div>
            <div class="view-actions">
              <button class="btn btn-primary btn-sm" onclick="openHabitModal()">
                <span class="icon-slot" data-icon="plus"></span>
                <span>New Habit</span>
              </button>
            </div>
          </div>

          <div class="card mb-4" style="margin-bottom: 20px;">
            <div class="flex items-center justify-between">
              <div>
                <h3 style="font-size: 15px; font-weight: 600;">Habit Consistency</h3>
                <p class="text-sm text-muted">Tap any circle to toggle today's completion. Maintain your flame streak 🔥!</p>
              </div>
              <div id="habits-overall-stats">
                <!-- Rendered by JS -->
              </div>
            </div>
          </div>

          <div class="dashboard-grid" id="habits-list-container">
            <!-- Rendered by JS -->
          </div>
        </section>

        <!-- 14. TIMER VIEW -->
        <section id="view-timer" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>Study Timer & Pomodoro</h1>
              <p>Focus sessions with audio synthesizer chime, subject tagging, and study logs.</p>
            </div>
            <div class="view-actions">
            </div>
          </div>

          <div class="dashboard-grid">
            <!-- Timer Card -->
            <div class="card col-6" style="text-align: center; padding: 28px;">
              <div class="flex items-center justify-center gap-2 mb-4" style="margin-bottom: 18px;">
                <button class="btn btn-sm btn-secondary active-timer-mode" id="timer-mode-pomodoro" onclick="setTimerMode('pomodoro')">Pomodoro (25m)</button>
                <button class="btn btn-sm btn-secondary" id="timer-mode-shortbreak" onclick="setTimerMode('shortbreak')">Short Break (5m)</button>
                <button class="btn btn-sm btn-secondary" id="timer-mode-longbreak" onclick="setTimerMode('longbreak')">Long Break (15m)</button>
                <button class="btn btn-sm btn-secondary" id="timer-mode-stopwatch" onclick="setTimerMode('stopwatch')">Stopwatch</button>
              </div>

              <div id="study-timer-display" style="font-family: var(--font-mono); font-size: 64px; font-weight: 700; margin: 20px 0; color: var(--text-primary);">
                25:00
              </div>

              <!-- Session Association -->
              <div class="form-row mb-4" style="margin-bottom: 20px; text-align: left;">
                <div class="form-group" style="margin-bottom: 0;">
                  <label>Subject</label>
                  <select class="form-control" id="timer-subject-select" onchange="updateTimerChapters(this.value)">
                    <!-- Populated by JS -->
                  </select>
                </div>
                <div class="form-group" style="margin-bottom: 0;">
                  <label>Chapter</label>
                  <select class="form-control" id="timer-chapter-select">
                    <!-- Populated by JS -->
                  </select>
                </div>
              </div>

              <div class="flex items-center justify-center gap-3">
                <button class="btn btn-primary btn-lg" id="timer-toggle-btn" onclick="toggleStudyTimer()">
                  <span class="icon-slot" data-icon="play"></span>
                  <span id="timer-toggle-label">Start Session</span>
                </button>
                <button class="btn btn-secondary btn-lg" onclick="resetStudyTimer()">
                  <span class="icon-slot" data-icon="rotate-ccw"></span>
                  <span>Reset</span>
                </button>
                <button class="btn btn-secondary btn-lg" onclick="finishAndLogSession()">
                  <span class="icon-slot" data-icon="check-circle"></span>
                  <span>Log Time</span>
                </button>
              </div>
            </div>

            <!-- Study History Log Card -->
            <div class="card col-6">
              <div class="card-header">
                <h3 class="card-title">
                  <span class="icon-slot" data-icon="clock"></span>
                  <span>Recent Study Sessions</span>
                </h3>
                <span class="badge badge-indigo" id="total-study-hours-badge">0 hrs</span>
              </div>
              <div id="study-sessions-history-list" style="max-height: 380px; overflow-y: auto;">
                <!-- Rendered by JS -->
              </div>
            </div>
          </div>
        </section>

        <!-- 15. STATISTICS VIEW -->
        <section id="view-statistics" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>Performance & Study Analytics</h1>
              <p>Real mathematical calculations of your goals, chapters, habits, and study productivity.</p>
            </div>
          </div>

          <div class="dashboard-grid" id="statistics-main-container">
            <!-- Rendered dynamically by JS with SVG charts -->
          </div>
        </section>

        <!-- 16. SETTINGS VIEW -->
        <section id="view-settings" class="view-container">
          <div class="view-header">
            <div class="view-title-group">
              <h1>Settings & Preferences</h1>
              <p>Workspace profiles, dashboard themes, appearance, and complete JSON data management.</p>
            </div>
          </div>

          <div class="dashboard-grid">
            <!-- Profiles Management -->
            <div class="card col-6">
              <div class="card-header">
                <h3 class="card-title">
                  <span class="icon-slot" data-icon="users"></span>
                  <span>Profiles & Workspaces</span>
                </h3>
                <button class="btn btn-primary btn-sm" onclick="openNewProfileModal()">
                  <span class="icon-slot" data-icon="plus"></span>
                  <span>New Profile</span>
                </button>
              </div>
              <p class="text-sm text-muted mb-3" style="margin-bottom: 12px;">Each profile has completely isolated subjects, timetable, notes, goals, and history.</p>
              <div id="settings-profiles-list">
                <!-- Rendered by JS -->
              </div>
            </div>

            <!-- Appearance & Customization -->
            <div class="card col-6">
              <div class="card-header">
                <h3 class="card-title">
                  <span class="icon-slot" data-icon="palette"></span>
                  <span>Theme & Appearance</span>
                </h3>
              </div>
              <div class="form-group">
                <label>Theme Mode</label>
                <div class="flex items-center gap-2">
                  <button class="btn btn-secondary btn-sm" onclick="setAppTheme('light')">Light Mode</button>
                  <button class="btn btn-secondary btn-sm" onclick="setAppTheme('dark')">Dark Mode</button>
                  <button class="btn btn-secondary btn-sm" onclick="setAppTheme('system')">System Default</button>
                </div>
              </div>
              <div class="form-group">
                <label>Accent Color</label>
                <div class="flex items-center gap-2 flex-wrap">
                  <button class="btn btn-sm btn-secondary" style="border-color:#4f46e5; color:#4f46e5;" onclick="setAppAccent('indigo')">Indigo</button>
                  <button class="btn btn-sm btn-secondary" style="border-color:#059669; color:#059669;" onclick="setAppAccent('emerald')">Emerald</button>
                  <button class="btn btn-sm btn-secondary" style="border-color:#7c3aed; color:#7c3aed;" onclick="setAppAccent('violet')">Violet</button>
                  <button class="btn btn-sm btn-secondary" style="border-color:#e11d48; color:#e11d48;" onclick="setAppAccent('rose')">Rose</button>
                  <button class="btn btn-sm btn-secondary" style="border-color:#d97706; color:#d97706;" onclick="setAppAccent('amber')">Amber</button>
                  <button class="btn btn-sm btn-secondary" style="border-color:#0284c7; color:#0284c7;" onclick="setAppAccent('sky')">Sky Blue</button>
                </div>
              </div>
              <div class="form-group">
                <label>Card Style & Density</label>
                <div class="flex items-center gap-2">
                  <select class="form-control" id="settings-card-style" onchange="setAppCardStyle(this.value)">
                    <option value="modern">Modern Rounded</option>
                    <option value="minimal">Minimalist Border</option>
                    <option value="elevated">Elevated Shadow</option>
                  </select>
                  <select class="form-control" id="settings-density" onchange="setAppDensity(this.value)">
                    <option value="comfortable">Comfortable</option>
                    <option value="compact">Compact</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- PWA App Installation & Offline -->
            <div class="card col-12">
              <div class="card-header">
                <h3 class="card-title">
                  <span class="icon-slot" data-icon="download"></span>
                  <span>Install StudyPulse App (PWA)</span>
                </h3>
                <span class="badge badge-emerald" id="pwa-status-badge">App Ready</span>
              </div>
              <p class="text-sm text-muted mb-3" style="margin-bottom: 12px;">Install StudyPulse directly onto your Android phone, iPhone, iPad, Windows, or Mac. Runs in a dedicated distraction-free window with 100% offline access and fast home-screen launch.</p>
              <div class="flex items-center gap-2 flex-wrap">
                <button class="btn btn-primary btn-sm" id="settings-install-app-btn" onclick="triggerPWAInstall()">
                  <span class="icon-slot" data-icon="download"></span>
                  <span>Install App on Device</span>
                </button>
                <button class="btn btn-secondary btn-sm" onclick="showAppInstallationGuideModal()">
                  <span class="icon-slot" data-icon="smartphone"></span>
                  <span>Installation Guide (iOS / Android / PC)</span>
                </button>
              </div>
            </div>
            
            

            <!-- Demo Data Controls -->
            <div class="card col-6">
              <div class="card-header">
                <h3 class="card-title">
                  <span class="icon-slot" data-icon="database"></span>
                  <span>Demo Data Controls</span>
                </h3>
              </div>
              <p class="text-sm text-muted mb-3" style="margin-bottom: 12px;">Restore realistic study examples or wipe demo data to start fresh.</p>
              <div class="flex items-center gap-2">
                <button class="btn btn-secondary btn-sm" onclick="restoreDemoDataAction()">
                  <span class="icon-slot" data-icon="rotate-ccw"></span>
                  <span>Restore Demo Data</span>
                </button>
                <button class="btn btn-danger btn-sm" onclick="removeDemoDataAction()">
                  <span class="icon-slot" data-icon="trash"></span>
                  <span>Remove Demo Data</span>
                </button>
              </div>
            </div>

            <!-- Data Backup: Export & Import -->
            <div class="card col-6">
              <div class="card-header">
                <h3 class="card-title">
                  <span class="icon-slot" data-icon="hard-drive"></span>
                  <span>Data Backup & Restore</span>
                </h3>
              </div>
              <p class="text-sm text-muted mb-3" style="margin-bottom: 12px;">Export all your workspace data to a JSON backup file or restore from a previous file.</p>
              <div class="flex items-center gap-2 flex-wrap">
                <button class="btn btn-secondary btn-sm" onclick="exportDataJSON()">
                  <span class="icon-slot" data-icon="download"></span>
                  <span>Export JSON Backup</span>
                </button>
                <button class="btn btn-secondary btn-sm" onclick="openImportModal()">
                  <span class="icon-slot" data-icon="upload"></span>
                  <span>Import JSON Data</span>
                </button>
              </div>
            </div>

            <!-- Recent Activity Log -->
            <div class="card col-12">
              <div class="card-header">
                <h3 class="card-title">
                  <span class="icon-slot" data-icon="activity"></span>
                  <span>Recent Activity Audit Trail</span>
                </h3>
                <button class="btn btn-secondary btn-sm" onclick="clearActivityLog()">Clear History</button>
              </div>
              <div id="activity-log-container" style="max-height: 250px; overflow-y: auto;">
                <!-- Rendered by JS -->
              </div>
            </div>
        </div>
            
            

          <!-- Developer Profile Card (Nivesh Kumar) -->
          <div class="developer-card" id="developer-card-section">
            <img src="myimage.jpg" alt="Developer Headshot" class="profile-img" onerror="this.onerror=null; this.src='data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'><rect width='120' height='120' rx='60' fill='%234f46e5'/><text x='50%25' y='56%25' font-family='sans-serif' font-size='40' font-weight='bold' fill='%23ffffff' dominant-baseline='middle' text-anchor='middle'>NK</text></svg>';">

            <div class="developer-info">
              <h2>Hi, I'm Nivesh Kumar</h2>
              <p class="title">Full-Stack Web Developer</p>

              <p class="intro">
                I am a Computer Science student at Indian Institute of Information Technology Una HP. I enjoy web development and building new projects. I have built projects like a Music Player and other web applications. I am always excited to learn, build, and improve my skills.
              </p>

              <div class="skills">
                <span>DSA</span>
                <span>Html</span>
                <span>Css</span>
                <span>Java Script</span>
              </div>

              <div class="social-links">
                <!-- GitHub -->
                <a class="github" href="https://github.com/nivesh091" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
                  <svg width="24" height="24" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="12" fill="#24292e" />
                    <path fill="#FFFFFF"
                      d="M12 4C7.58 4 4 7.58 4 12c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.28.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0020 12c0-4.42-3.58-8-8-8z" />
                  </svg>
                </a>

                <!-- LinkedIn -->
                <a class="linkedin" href="https://www.linkedin.com/in/nivesh-kumar-32b476360/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
                  <svg width="24" height="24" viewBox="0 0 24 24">
                    <path fill="#0A66C2"
                      d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
                  </svg>
                </a>

                <!-- Instagram -->
                <a class="insta" href="https://www.instagram.com/nivesh_091" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
                  <svg width="24" height="24" viewBox="0 0 24 24">
                    <defs>
                      <radialGradient id="instaGrad" cx="30%" cy="107%" r="150%">
                        <stop offset="0%" stop-color="#fdf497" />
                        <stop offset="5%" stop-color="#fdf497" />
                        <stop offset="45%" stop-color="#fd5949" />
                        <stop offset="60%" stop-color="#d6249f" />
                        <stop offset="90%" stop-color="#285AEB" />
                      </radialGradient>
                    </defs>
                    <path fill="url(#instaGrad)"
                      d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" />
                  </svg>
                </a>

                <!-- Gmail -->
                <a class="gmail" href="https://mail.google.com/mail/?view=cm&fs=1&to=niveshkumar1230@gmail.com" target="_blank" rel="noopener noreferrer" aria-label="Gmail">
                  <svg width="24" height="24" viewBox="0 0 24 24">
                    <path fill="#4285F4"
                      d="M22.364 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-4.909-3.682v8.678H3.272A1.636 1.636 0 0 1 1.636 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L12 9.49l6.436-6.002c1.618-1.209 3.928-.059 3.928 1.969z" />
                    <path fill="#34A853"
                      d="M1.636 5.457v13.909c0 .904.732 1.636 1.636 1.636h2.182V11.73L1.636 8.847V5.457z" />
                    <path fill="#EA4335"
                      d="M22.364 5.457v3.39l-3.818 2.883v8.906h2.182c.904 0 1.636-.732 1.636-1.636V5.457z" />
                    <path fill="#FBBC04"
                      d="M5.563 3.493L12 9.49l6.436-5.997c-.822-.614-1.898-.781-2.883-.438L12 5.092 8.447 3.055c-.985-.343-2.061-.176-2.884.438z" />
                  </svg>
                </a>
              </div>
            </div>
          </div>
            
            
        </section>
      </main>
    </div>

    <!-- Mobile Bottom Navigation Bar -->
    <nav id="mobile-bottom-nav">
      <div class="mobile-nav-item active" data-view="dashboard" onclick="navigateTo('dashboard')">
        <span class="icon-slot" data-icon="layout-dashboard"></span>
        <span>Home</span>
      </div>
      <div class="mobile-nav-item" data-view="planner" onclick="navigateTo('planner')">
        <span class="icon-slot" data-icon="calendar-days"></span>
        <span>Planner</span>
      </div>
      <div class="mobile-nav-item" data-view="timetable" onclick="navigateTo('timetable')">
        <span class="icon-slot" data-icon="table"></span>
        <span>Timetable</span>
      </div>
      <div class="mobile-nav-item" data-view="todos" onclick="navigateTo('todos')">
        <span class="icon-slot" data-icon="check-square"></span>
        <span>Tasks</span>
      </div>
      <div class="mobile-nav-item" data-view="timer" onclick="navigateTo('timer')">
        <span class="icon-slot" data-icon="timer"></span>
        <span>Timer</span>
      </div>
    </nav>
  </div>

  <!-- Modal Container -->
  <div id="modal-container" class="modal-backdrop" onclick="handleModalBackdropClick(event)">
    <div class="modal-box" id="modal-box" role="dialog" aria-modal="true">
      <!-- Modal Content Injected by JS -->
    </div>
  </div>

  <!-- Toast Notification Container -->
  <div id="toast-container"></div>

  <!-- Offline Status Indicator -->
  <div id="offline-indicator" class="offline-toast" style="display: none;">
    <span class="offline-dot animate-pulse"></span>
    <span>Offline Mode — All data is securely saved locally</span>
  </div>
"""