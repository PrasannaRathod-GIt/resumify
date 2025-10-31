import os, json, sqlite3
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask import g, jsonify, redirect, url_for

# --- Persistence config ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join("static", "uploads")
DB_PATH = os.path.join(BASE_DIR, "submissions.db")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_db(_e):
    db = getattr(g, "_db", None)
    if db is not None:
        db.close()

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              template TEXT NOT NULL,
              data TEXT NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_submission(template_key: str, data: dict) -> int:
    db = get_db()
    cur = db.execute("INSERT INTO submissions (template, data) VALUES (?, ?)",
                     (template_key, json.dumps(data)))
    db.commit()
    return cur.lastrowid

def load_submission(submission_id: int):
    db = get_db()
    row = db.execute("SELECT template, data FROM submissions WHERE id=?", (submission_id,)).fetchone()
    if not row:
        return None, None
    return row["template"], json.loads(row["data"])

def parse_multiline_field(value):
    """
    Parse a textarea where user may enter one item per line.
    Returns a list of stripped, non-empty items.
    Falls back to comma-splitting if no newline items found (backwards compatibility).
    """
    if not value:
        return []
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    if lines:
        return lines
    return [item.strip() for item in value.split(',') if item.strip()]

# ---------------- Template 1 ----------------
@app.route('/form/template1')
def form_template1():
    return render_template('template1/form.html')

@app.route('/preview/template1', methods=['POST'])
def preview_template1():
    name = request.form['name']
    title = request.form['title']
    about = request.form['about']
    skills = request.form['skills'].split(',')
    certs = [c.strip() for c in request.form.getlist('certs[]') if c.strip()]
    experience = request.form['experience']
    education = [e.strip() for e in request.form.getlist('education[]') if e.strip()]
    phone = request.form['phone']
    email = request.form['email']
    location = request.form['location']

    # Handle uploaded photo
    photo_file = request.files['photo']
    photo_filename = None
    if photo_file and photo_file.filename != '':
        photo_filename = secure_filename(photo_file.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo_file.save(photo_path)

    return render_template('template1/preview.html',
                           name=name, title=title, about=about,
                           skills=[s.strip() for s in skills],
                           certs=[c.strip() for c in certs],
                           experience=experience,
                           education=education,
                           phone=phone, email=email, location=location,
                           profile_photo=photo_filename)

# ---------------- Template 2 ----------------
@app.route('/form/template2')
def form_template2():
    return render_template('template2/form.html')

@app.route('/preview/template2', methods=['POST'])
def preview_template2():
    name = request.form['name']
    title = request.form['title']
    phone = request.form['phone']
    email = request.form['email']
    website = request.form['website']
    address = request.form['address']
    about = request.form['about']

    education_raw = request.form.get("education", "")
    education = [e.strip() for e in education_raw.split("||") if e.strip()]


    expertise = [e.strip() for e in request.form['expertise'].split(',')]
    languages = [l.strip() for l in request.form['languages'].split(',')]

    no_experience = 'no_experience' in request.form

    job1_duration = request.form.get('job1_duration', '')
    job1_company = request.form.get('job1_company', '')
    job1_position = request.form.get('job1_position', '')
    job1_desc = request.form.get('job1_desc', '')

    job2_duration = request.form.get('job2_duration', '')
    job2_company = request.form.get('job2_company', '')
    job2_position = request.form.get('job2_position', '')
    job2_desc = request.form.get('job2_desc', '')

    job3_duration = request.form.get('job3_duration', '')
    job3_company = request.form.get('job3_company', '')
    job3_position = request.form.get('job3_position', '')
    job3_desc = request.form.get('job3_desc', '')

    internships = request.form['internships']

    # Handle uploaded photo
    photo_file = request.files['photo']
    photo_filename = None
    if photo_file and photo_file.filename != '':
        photo_filename = secure_filename(photo_file.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo_file.save(photo_path)

    return render_template('template2/preview.html',
        name=name, title=title, phone=phone, email=email, website=website, address=address,
        about=about, education=education,
        expertise=expertise, languages=languages,
        no_experience=no_experience,
        job1_duration=job1_duration, job1_company=job1_company,
        job1_position=job1_position, job1_desc=job1_desc,
        job2_duration=job2_duration, job2_company=job2_company,
        job2_position=job2_position, job2_desc=job2_desc,
        job3_duration=job3_duration, job3_company=job3_company,
        job3_position=job3_position, job3_desc=job3_desc,
        internships=internships, profile_photo=photo_filename)

# ---------------- Home Page ----------------
@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/select_template')
def select_template():
    return render_template('select_template.html')


# ---------------- Template 3 ----------------
@app.route("/form/template3")
def template3_form():
    return render_template("template3/form.html")


@app.route("/preview/template3", methods=["POST"])
def template3_preview():
    # Profile image
    image_file = request.files.get("profile_image")
    profile_image = None
    if image_file and image_file.filename:
        filename = secure_filename(image_file.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image_file.save(save_path)
        profile_image = filename

    # Basic info
    name = request.form.get("name", "")
    title = request.form.get("title", "")
    profile = request.form.get("profile", "")

    # Contact
    location = request.form.get("location", "")
    email = request.form.get("email", "")
    phone = request.form.get("phone", "")
    linkedin = request.form.get("linkedin", "")

    # Education
    edu_institution = request.form.get("edu_institution", "")
    edu_degree = request.form.get("edu_degree", "")
    edu_year = request.form.get("edu_year", "")

    # Skills
    skills = request.form.getlist("skills[]") or []
    skills = [s.strip() for s in skills if s.strip()]

    # Work experience (up to 3)
    experiences = []
    for i in range(1, 4):
        company = request.form.get(f"exp{i}_company", "").strip()
        role = request.form.get(f"exp{i}_role", "").strip()
        start = request.form.get(f"exp{i}_start", "").strip()
        end = request.form.get(f"exp{i}_end", "").strip()
        desc = request.form.getlist(f"exp{i}_desc[]") or []
        desc = [d.strip() for d in desc if d.strip()]

        if company or role or start or end or desc:
            experiences.append({
                "company": company,
                "role": role,
                "start": start,
                "end": end,
                "desc": desc
            })

    # Bundle data
    data = dict(
        name=name,
        title=title,
        profile=profile,
        location=location,
        email=email,
        phone=phone,
        linkedin=linkedin,
        edu_institution=edu_institution,
        edu_degree=edu_degree,
        edu_year=edu_year,
        skills=skills,
        experiences=experiences,
        profile_image=profile_image
    )

    submission_id = save_submission("template3", data)
    return render_template("template3/preview.html", **data, submission_id=submission_id)



# ---------------- Template 4 ----------------
# ---------------- Template 4 ----------------
# ---------------- Template 4 ----------------
@app.route("/form/template4", methods=["GET", "POST"])
def template4_form():
    if request.method == "POST":
        # Profile image
        profile_file = request.files.get("profile_image")
        profile_image = None
        if profile_file and profile_file.filename:
            filename = secure_filename(profile_file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            profile_file.save(save_path)
            profile_image = filename  # just filename, not full path

        # Basic info
        name = request.form.get("name")
        title = request.form.get("title")
        about = request.form.get("about")
        email = request.form.get("email")
        phone = request.form.get("phone")
        location = request.form.get("location")
        website = request.form.get("website")

        # Skills
        hard_skills = [s for s in request.form.getlist("hard_skills[]") if s.strip()]
        soft_skills_raw = request.form.get("soft_skills")
        soft_skills = json.loads(soft_skills_raw) if soft_skills_raw else []

        # Education
        education = [e for e in request.form.getlist("education[]") if e.strip()]

        # Experiences (fixed so responsibilities are unique per experience)
        experiences = []
        companies = request.form.getlist("company[]")
        job_titles = request.form.getlist("job_title[]")
        start_dates = request.form.getlist("start_date[]")
        end_dates = request.form.getlist("end_date[]")

        for i in range(len(companies)):
            resp_key = f"responsibilities[{i}][]"
            resp_list = request.form.getlist(resp_key)
            if companies[i].strip() or job_titles[i].strip():
                experiences.append({
                    "company": companies[i],
                    "job_title": job_titles[i],
                    "start_date": start_dates[i],
                    "end_date": end_dates[i],
                    "responsibilities": [r.strip() for r in resp_list if r.strip()]
                })

        # Achievements
        achievements = []
        achievement_dates = request.form.getlist("achievement_date[]")
        achievement_descs = request.form.getlist("achievement_desc[]")
        for d, desc in zip(achievement_dates, achievement_descs):
            if d.strip() or desc.strip():
                achievements.append({"date": d, "desc": desc})

        # Bundle data
        data = dict(
            name=name, title=title, about=about,
            email=email, phone=phone, location=location, website=website,
            hard_skills=hard_skills, soft_skills=soft_skills,
            education=education, profile_image=profile_image,
            experiences=experiences, achievements=achievements
        )

        submission_id = save_submission("template4", data)
        return render_template("template4/preview.html", **data, submission_id=submission_id)

    # GET request
    return render_template("template4/form.html")

# ---------------- Template 5 ----------------
@app.route('/form/template5')
def form_template5():
    return render_template('template5/form.html')

@app.route('/preview/template5', methods=['POST'])
def preview_template5():
    # Basic fields
    name = request.form.get('name', '').strip()
    title = request.form.get('title', '').strip()
    about = request.form.get('about', '').strip()

    # Contact
    phone = request.form.get('phone', '').strip()
    email = request.form.get('email', '').strip()
    linkedin = request.form.get('linkedin', '').strip()
    address = request.form.get('address', '').strip()

    # Education (stored client-side as "||"-joined values)
    education_raw = request.form.get('education', '')
    education = [e.strip() for e in education_raw.split('||') if e.strip()]

    # Skills & languages (comma-separated hidden inputs)
    skills = [s.strip() for s in request.form.get('skills', '').split(',') if s.strip()]
    languages = [l.strip() for l in request.form.get('languages', '').split(',') if l.strip()]

    # Certificates (dynamic fields name="cert_name[]" and name="cert_provider[]")
    cert_names = request.form.getlist('cert_name[]')
    cert_providers = request.form.getlist('cert_provider[]')
    certificates = []
    for n, p in zip(cert_names, cert_providers):
        if n.strip() or p.strip():
            certificates.append({'name': n.strip(), 'provider': p.strip()})

    # Photo upload (input name="photo")
    photo_file = request.files.get('photo')
    photo_filename = None
    if photo_file and photo_file.filename:
        photo_filename = secure_filename(photo_file.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo_file.save(photo_path)

    # Bundle
    data = dict(
        name=name, title=title, about=about,
        phone=phone, email=email, linkedin=linkedin, address=address,
        education=education, skills=skills, languages=languages,
        certificates=certificates, profile_photo=photo_filename
    )

    # Save (keeps consistent with template3/4 behaviour)
    submission_id = save_submission("template5", data)
    return render_template('template5/preview.html', **data, submission_id=submission_id)







# ---------------- API + Resume View ----------------
@app.route("/api/submissions")
def api_list_submissions():
    db = get_db()
    rows = db.execute("SELECT id, template, created_at FROM submissions ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])

TEMPLATE_MAP = {
    "template1": "template1/preview.html",
    "template2": "template2/preview.html",
    "template3": "template3/preview.html",
    "template4": "template4/preview.html",
   
}

@app.route("/resume/<int:submission_id>")
def resume_view(submission_id):
    template_key, data = load_submission(submission_id)
    if not template_key:
        return "Not found", 404
    tpl = TEMPLATE_MAP.get(template_key)
    if not tpl:
        return f"Template not registered: {template_key}", 500
    return render_template(tpl, **data, submission_id=submission_id)


# ✅ Run the app
if __name__ == '__main__':
    init_db()  # make sure DB table exists
    app.run(debug=True)
