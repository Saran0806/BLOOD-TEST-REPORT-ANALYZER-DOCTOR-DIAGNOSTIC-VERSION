import mysql.connector

# ---------------- Database Setup ----------------
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="saransk"
)
cursor = connection.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS blood_analyzer_db")
cursor.execute("USE blood_analyzer_db")

# Create table for patient reports
cursor.execute("""
CREATE TABLE IF NOT EXISTS patient_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    abnormal_tests TEXT,
    diseases TEXT,
    doctor_advice TEXT
)
""")

print("✅ Database and table created successfully!")

cursor.close()
connection.close()


# ---------------- Analysis Function ----------------
def analyze_patient(name, age, gender, normal_ranges):
    patient_data = {}
    print(f"\nEnter blood test values for {name}:")
    for test in normal_ranges.keys():
        while True:
            try:
                value = float(input(f"{test}: "))
                break
            except ValueError:
                print("❌ Invalid input. Please enter a numeric value.")
        patient_data[test] = value

    # Identify abnormal test results
    abnormal_tests = {}
    for test, (low, high) in normal_ranges.items():
        value = patient_data[test]
        if value < low:
            abnormal_tests[test] = "Low"
        elif value > high:
            abnormal_tests[test] = "High"
        else:
            abnormal_tests[test] = "Normal"

    # ---------------- Disease suggestion rules ----------------
    possible_diseases = []

    if abnormal_tests.get("Hemoglobin") == "Low" and abnormal_tests.get("Platelet Count") == "Low":
        possible_diseases.append("Malaria: Take antimalarial drugs and rest")

    if abnormal_tests.get("Platelet Count") == "Low" and abnormal_tests.get("WBC Count") in ["High", None]:
        possible_diseases.append("Dengue: Monitor platelet count and stay hydrated")

    if abnormal_tests.get("Blood Sugar (Fasting)") == "High":
        possible_diseases.append("Diabetes: Reduce sugar intake, exercise regularly")

    if abnormal_tests.get("Hemoglobin") == "Low" and abnormal_tests.get("RBC Count") == "Low":
        possible_diseases.append("Anemia: Iron supplements and diet rich in iron")

    if abnormal_tests.get("Cholesterol") == "High":
        possible_diseases.append("High Cholesterol: Avoid fatty foods and exercise regularly")

    if not possible_diseases:
        possible_diseases.append("No major disease detected")

    print("-" * 50)

    # ---------------- Doctor input for advice ----------------
    doctor_advice = {}
    print("\n=== Doctor: Provide treatment/advice for abnormal tests or diseases ===")
    for disease in possible_diseases:
        advice = input(f"Advice for {disease}: ")
        doctor_advice[disease] = advice

    print("💬 Take care of your health. Small daily changes make a big difference!")
    print("-" * 50)

    # ---------------- Save Report to File ----------------
    filename = f"{name.lower().replace(' ', '_')}_blood_report.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write("BLOOD TEST ANALYSIS REPORT\n")
        file.write("-----------------------------------\n")
        file.write(f"Patient Name: {name}\n")
        file.write(f"Age: {age}\n")
        file.write(f"Gender: {gender}\n\n")

        file.write("Test Results:\n")
        for test, status in abnormal_tests.items():
            file.write(f"{test}: {status}\n")

        file.write("\nPossible Diseases & Doctor Advice:\n")
        for disease in possible_diseases:
            file.write(f"{disease}: {doctor_advice[disease]}\n")

    print(f"\n✅ Report for {name} saved successfully as '{filename}'")

    # ---------------- Save Report to Database ----------------
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="saransk",
            database="blood_analyzer_db"
        )
        cursor = connection.cursor()

        abnormal_str = ", ".join([f"{t}={s}" for t, s in abnormal_tests.items()])
        disease_str = ", ".join(possible_diseases)
        advice_str = "; ".join([f"{d}: {a}" for d, a in doctor_advice.items()])

        query = """
        INSERT INTO patient_reports (name, age, gender, abnormal_tests, diseases, doctor_advice)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (name, age, gender, abnormal_str, disease_str, advice_str)
        cursor.execute(query, values)
        connection.commit()

        print("✅ Data successfully saved into MySQL database.")

    except mysql.connector.Error as e:
        print(f"❌ Error saving to database: {e}")

    finally:
        if cursor and connection.is_connected():
            cursor.close()
            connection.close()

    return {
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Abnormal Tests": abnormal_tests,
        "Diseases": possible_diseases,
        "Doctor Advice": doctor_advice
    }


# ---------------- Main Function ----------------
def main():
    print("\n🩺 BLOOD TEST REPORT ANALYZER - DOCTOR DIAGNOSTIC VERSION 🩺")
    print("-----------------------------------------------------------")

    normal_ranges = {
        "Hemoglobin": (13.0, 17.0),
        "RBC Count": (4.5, 5.9),
        "WBC Count": (4000, 11000),
        "Platelet Count": (150000, 450000),
        "Blood Sugar (Fasting)": (70, 110),
        "Cholesterol": (125, 200)
    }

    while True:
        name = input("\nEnter patient name (or type 'exit' to finish): ")
        if name.lower() == "exit":
            break
        try:
            age = int(input("Enter age: "))
        except ValueError:
            print("❌ Invalid input for age. Please enter a number.")
            continue
        gender = input("Enter gender (Male/Female): ")

        analyze_patient(name, age, gender, normal_ranges)


# ---------------- Program Entry ----------------
if __name__ == "__main__":
    main()
