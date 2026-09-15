import os
import sys

from build_styles import css_code
from build_html import html_body
from js_icons import js_icons_code
from js_demo_data import js_demo_data_code
from js_state_and_storage import js_state_storage_code
from js_views_1 import js_views_1_code
from js_views_2 import js_views_2_code
from js_views_3 import js_views_3_code

final_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light" data-accent="indigo" data-card-style="modern" data-density="comfortable">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>StudyPulse - Personal Productivity & Study Management Dashboard</title>
  <meta name="description" content="A complete, professional, modern, responsive Personal Productivity + Study Management Dashboard. Manage subjects, chapters, timetable, tasks, goals, habits, notes, and study timer offline with LocalStorage.">
  <meta property="og:title" content="StudyPulse - Personal Productivity & Study Management Dashboard">
  <meta property="og:description" content="A complete, professional, modern, responsive Personal Productivity + Study Management Dashboard.">
  <meta name="theme-color" content="#4f46e5">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="StudyPulse">
  <link rel="manifest" href="/manifest.webmanifest">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="icon" type="image/svg+xml" href="/icon.svg">
  <link rel="icon" type="image/png" sizes="192x192" href="/pwa-192x192.png">
  <style>
{css_code}
  </style>
</head>
<body>
{html_body}

  <script>
{js_icons_code}
{js_demo_data_code}
{js_state_storage_code}
{js_views_1_code}
{js_views_2_code}
{js_views_3_code}
  </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Generated index.html successfully! File size:", len(final_html), "bytes")
