# College Fee Voucher System (Flask)

A complete, local-first fee voucher / student management system for
**SWAT DEGREE COLLEGE OF TECHNOLOGY** — built with Flask, SQLite, HTML/CSS/JS.

Built by **Rashid Zada — Full Stack Developer**
📱 WhatsApp: **0347-0983567** — message him if you need similar software.

---

## ✨ Features

- 🔐 **Admin-only login** (default `admin` / `admin123`), change password anytime in Settings
- 📊 **Dashboard** — total students, teachers, courses, amount collected, pending dues
- 👩‍🏫 **Teachers** — add / remove teaching staff
- 📘 **Courses** — set tuition fee + one-time fees (ID card, DMC, exam, fund)
- 🎓 **Students** — enroll students, pick a course/teacher, choose 1–4 installments;
  the fee schedule is generated automatically
- 💰 **Dues tracking** — see every unpaid/overdue installment per student, mark as paid
- 🧾 **Real two-copy voucher slip** — Office Copy + Student Copy, matching your original design
- 🖨️ **Print** directly from the browser (both copies laid out for printing)
- ⬇️ **Download PDF** — both copies on one A4 page (generated server-side with ReportLab,
  no external programs needed)
- 💬 **WhatsApp share** — one click opens a chat with the **student's own WhatsApp number**
  with the voucher details pre-filled (see note below on attaching the PDF)
- 📥 **Excel Import / Export** — back up all data (teachers, courses, students, payments)
  to a `.xlsx` file, or bulk-import from Excel
- 100% **local** — runs on your own PC, data stored in a local SQLite file (`college.db`)

---

## 🚀 Setup (Windows / macOS / Linux)

1. Install **Python 3.9+** if you don't already have it: https://python.org
2. Open a terminal in this folder and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python app.py
   ```

4. Open your browser at **http://127.0.0.1:5000**
5. Log in with:
   - Username: `admin`
   - Password: `admin123`
6. Go to **Settings** and change the password immediately.

The database file `college.db` is created automatically on first run in the
same folder — just back it up (or use the Excel export) to keep your records safe.

---

## 📖 How to use it

1. **Teachers** → add your teaching staff first.
2. **Courses** → add each course (e.g. CCTV, 4 Months) with its total fee and
   one-time charges (ID Card / DMC / Exam / Fund fees — these are only added to
   the **first** installment).
3. **Students** → enroll a student, pick their course & teacher, choose how many
   installments (1–4), and the installment schedule + due dates are generated instantly.
4. Open a student's page to see their **installment schedule**. Click **Slip** on any
   installment to open the voucher — from there you can **Print**, **Download PDF**,
   or **Send to Student's WhatsApp**.
5. **Dashboard** always shows the latest pending dues across all students.
6. **Import / Export** → download a full Excel backup any time, or bulk-import
   students/courses/teachers from a spreadsheet (use the exported file as a template).

---

## 💬 About the WhatsApp & SMS features

- The **WhatsApp button** on each voucher opens `wa.me` with the student's number and a
  ready-made message (fee amount, due date, etc.). This uses WhatsApp's free "click to
  chat" link — the **only** thing it cannot do automatically is attach the PDF file,
  because that requires a paid WhatsApp Business API subscription. Simply click
  **Download PDF** first, then attach it in the chat that opens — takes two clicks.
- Real **SMS sending** (e.g. via Twilio) needs a paid SMS gateway account with its own
  API keys. This app doesn't fabricate that connection, but `app.py` is structured so a
  `send_sms()` function can be dropped in easily once you have gateway credentials —
  message the developer above if you'd like this added.

---

## 🗂️ Project Structure

```
college_voucher_system/
├── app.py                  # Flask app: routes, DB, auth, Excel import/export
├── pdf_generator.py         # Builds the two-copy voucher PDF (ReportLab)
├── requirements.txt
├── college.db               # Created automatically (SQLite database)
├── templates/                # All HTML pages (Jinja2)
└── static/
    ├── css/style.css         # App styling
    └── js/script.js
```

---

## 🔒 Security notes for real-world use

- Change `app.secret_key` in `app.py` before deploying anywhere beyond your own PC.
- Change the default admin password immediately after first login.
- This app is designed to run **locally** on one office computer. If you want it
  accessible over the internet or by multiple staff members at once, it should be
  deployed behind a proper WSGI server (e.g. gunicorn) with HTTPS — contact the
  developer above for help setting that up.

---

Need a custom version of this software (multi-branch, SMS/WhatsApp Business API,
online fee payment, etc.)? Contact **Rashid Zada — Full Stack Developer**
📱 **WhatsApp: 0347-0983567**
