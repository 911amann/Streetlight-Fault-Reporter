from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

FILE_NAME = "data/streetlights.txt"


# Read all streetlight records from the file
def read_records():
    records = []

    try:
        file = open(FILE_NAME, "r")

        for line in file:
            line = line.strip()

            if line != "":
                data = line.split("|")

                record = {
                    "id": data[0],
                    "pole": data[1],
                    "area": data[2],
                    "problem": data[3],
                    "severity": data[4],
                    "priority": data[5],
                    "status": data[6],
                    "reported_by": data[7]
                }

                records.append(record)

        file.close()

    except FileNotFoundError:
        print("Data file not found.")

    return records


# Save a new streetlight record
def save_record(record):
    try:
        file = open(FILE_NAME, "a")

        line = (
            record["id"] + "|" +
            record["pole"] + "|" +
            record["area"] + "|" +
            record["problem"] + "|" +
            record["severity"] + "|" +
            record["priority"] + "|" +
            record["status"] + "|" +
            record["reported_by"] + "\n"
        )

        file.write(line)
        file.close()

    except Exception as error:
        print("Error while saving:", error)


# Generate the next report ID
def get_next_id(records):
    if len(records) == 0:
        return "SL001"

    numbers = []

    for record in records:
        number = int(record["id"][2:])
        numbers.append(number)

    next_number = max(numbers) + 1

    return "SL" + str(next_number).zfill(3)


# Assign priority according to severity
def assign_priority(severity):

    if severity == "Critical":
        return "High"

    elif severity == "Major":
        return "Medium"

    else:
        return "Low"


# Validate mobile number using regular expression
def validate_phone(phone):

    pattern = r"^[0-9]{10}$"

    if re.match(pattern, phone):
        return True

    return False


# Home page
@app.route("/")
def index():

    records = read_records()

    total = len(records)

    pending = 0
    repaired = 0
    high_priority = 0

    for record in records:

        if record["status"] != "Repaired":
            pending += 1

        if record["status"] == "Repaired":
            repaired += 1

        if record["priority"] == "High" and record["status"] != "Repaired":
            high_priority += 1

    areas = set()

    for record in records:
        areas.add(record["area"])

    return render_template(
        "index.html",
        total=total,
        pending=pending,
        repaired=repaired,
        high_priority=high_priority,
        areas=len(areas)
    )


# Report a new fault
@app.route("/report", methods=["GET", "POST"])
def report():

    if request.method == "POST":

        pole = request.form["pole"].strip()
        area = request.form["area"].strip()
        problem = request.form["problem"].strip()
        severity = request.form["severity"]
        reported_by = request.form["reported_by"].strip()
        phone = request.form["phone"].strip()

        if pole == "" or area == "" or problem == "" or reported_by == "":
            return render_template(
                "report.html",
                message="Please fill all required fields."
            )

        if not validate_phone(phone):
            return render_template(
                "report.html",
                message="Please enter a valid 10 digit mobile number."
            )

        records = read_records()

        new_id = get_next_id(records)

        priority = assign_priority(severity)

        record = {
            "id": new_id,
            "pole": pole,
            "area": area,
            "problem": problem,
            "severity": severity,
            "priority": priority,
            "status": "Pending",
            "reported_by": reported_by + " (" + phone + ")"
        }

        save_record(record)

        return redirect(url_for("poles"))

    return render_template("report.html")


# Pole tracking
@app.route("/poles")
def poles():

    records = read_records()

    return render_template(
        "poles.html",
        records=records
    )


# Update repair status
@app.route("/repair/<report_id>")
def repair(report_id):

    records = read_records()

    for record in records:

        if record["id"] == report_id:
            record["status"] = "Repaired"

    try:
        file = open(FILE_NAME, "w")

        for record in records:

            line = (
                record["id"] + "|" +
                record["pole"] + "|" +
                record["area"] + "|" +
                record["problem"] + "|" +
                record["severity"] + "|" +
                record["priority"] + "|" +
                record["status"] + "|" +
                record["reported_by"] + "\n"
            )

            file.write(line)

        file.close()

    except Exception as error:
        print("Error while updating:", error)

    return redirect(url_for("poles"))


# Maintenance queue
@app.route("/queue")
def queue():

    records = read_records()

    pending_records = []

    for record in records:

        if record["status"] != "Repaired":
            pending_records.append(record)

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    pending_records.sort(
        key=lambda record: priority_order[record["priority"]]
    )

    return render_template(
        "queue.html",
        records=pending_records
    )


# Area-wise reports
@app.route("/areas")
def areas():

    records = read_records()

    area_names = set()

    for record in records:
        area_names.add(record["area"])

    area_reports = []

    for area in area_names:

        area_records = [
            record for record in records
            if record["area"] == area
        ]

        total = len(area_records)

        pending = 0
        repaired = 0

        for record in area_records:

            if record["status"] == "Repaired":
                repaired += 1
            else:
                pending += 1

        area_reports.append({
            "area": area,
            "total": total,
            "pending": pending,
            "repaired": repaired
        })

    return render_template(
        "areas.html",
        reports=area_reports
    )


if __name__ == "__main__":
    app.run(debug=True)