import mysql.connector

# ------------------------- DB CONNECTION -------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="HardhikSP@26"
)
cur = conn.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS hr_system")
cur.execute("USE hr_system")


# ------------------------- TABLES -------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    candidate_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    experience INT,
    skills TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(100),
    required_skills TEXT
)
""")

conn.commit()


# ------------------------- MATCH FUNCTION -------------------------
def calculate_match(candidate_skills, required_skills):
    candidate_set = set([x.strip() for x in candidate_skills.lower().split(",")])
    required_set = set([x.strip() for x in required_skills.lower().split(",")])

    matched = candidate_set & required_set
    score = (len(matched) / len(required_set)) * 100 if len(required_set) > 0 else 0

    return round(score, 2), matched


# ------------------------- ADD CANDIDATE -------------------------
def add_candidate():
    print("\n--- Add New Candidate ---")
    name = input("Name: ")
    exp = input("Experience (years): ")
    skills = input("Skills (comma-separated): ")

    cur.execute("INSERT INTO candidates (name, experience, skills) VALUES (%s, %s, %s)",
                (name, exp, skills))
    conn.commit()
    print("Candidate added successfully!\n")


# ------------------------- ADD JOB -------------------------
def add_job():
    print("\n--- Add New Job ---")
    title = input("Job Title: ")
    skills = input("Required Skills (comma-separated): ")

    cur.execute("INSERT INTO jobs (job_title, required_skills) VALUES (%s, %s)",
                (title, skills))
    conn.commit()
    print("Job added successfully!\n")


# ------------------------- SEARCH CANDIDATE BY SKILL -------------------------
def search_candidate_by_skill():
    skill = input("\nEnter skill to search: ").lower()

    print("\nCandidates with skill:", skill)
    cur.execute("SELECT name, skills FROM candidates")

    found = False
    for row in cur.fetchall():
        name, skills = row
        if skill in skills.lower():
            print(f"✔ {name}  —  Skills: {skills}")
            found = True

    if not found:
        print("No candidates found with this skill.\n")


# ------------------------- UPDATE CANDIDATE SKILLS -------------------------
def update_candidate_skills():
    cid = int(input("\nEnter candidate ID to update: "))
    new_skills = input("Enter new skills (comma-separated): ")

    cur.execute("UPDATE candidates SET skills=%s WHERE candidate_id=%s",
                (new_skills, cid))
    conn.commit()
    print("Skills updated successfully!\n")


# ------------------------- DELETE CANDIDATE -------------------------
def delete_candidate():
    cid = int(input("\nEnter candidate ID to delete: "))

    cur.execute("DELETE FROM candidates WHERE candidate_id=%s", (cid,))
    conn.commit()
    print("Candidate deleted successfully!\n")


# ------------------------- TOP CANDIDATE MATCHING -------------------------
def top_candidates_for_job():
    job_id = int(input("\nEnter job ID: "))

    cur.execute("SELECT job_title, required_skills FROM jobs WHERE job_id=%s", (job_id,))
    job = cur.fetchone()

    if not job:
        print("Invalid Job ID!\n")
        return

    title, req_skills = job
    print(f"\n🔍 Job: {title}")
    print("Required Skills:", req_skills)

    cur.execute("SELECT name, skills FROM candidates")
    results = []

    for cand in cur.fetchall():
        name, skills = cand
        score, matched = calculate_match(skills, req_skills)
        results.append((name, score, matched))

    results.sort(key=lambda x: x[1], reverse=True)

    print("\n⭐ Top 3 Candidates:")
    for r in results[:3]:
        print(f"{r[0]} → {r[1]}% match | Skills matched: {', '.join(r[2]) or 'None'}")


# ------------------------- MENU -------------------------
def menu():
    while True:
        print("""
-------------------------------------
     HR Hiring System – Main Menu
-------------------------------------
1. Add Candidate
2. Add Job
3. Search Candidate by Skill
4. Update Candidate Skills
5. Delete Candidate
6. Top Candidates for a Job
7. Exit
""")

        choice = input("Enter choice: ")

        if choice == "1":
            add_candidate()
        elif choice == "2":
            add_job()
        elif choice == "3":
            search_candidate_by_skill()
        elif choice == "4":
            update_candidate_skills()
        elif choice == "5":
            delete_candidate()
        elif choice == "6":
            top_candidates_for_job()
        elif choice == "7":
            print("Exiting system…")
            break
        else:
            print("Invalid choice! Try again.\n")


# ------------------------- START PROGRAM -------------------------
menu()
