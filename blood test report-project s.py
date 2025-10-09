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
            status = "Low"
            abnormal_tests[test] = "Low"
        elif value > high:
            status = "High"
            abnormal_tests[test] = "High"
        else:
            status = "Normal"
        patient_data[test] = (value, status)

    # ---------------- Disease suggestion rules ----------------
    possible_diseases = []

    # Malaria: Low Hemoglobin + Low Platelet
    if abnormal_tests.get("Hemoglobin") == "Low" and abnormal_tests.get("Platelet Count") == "Low":
        possible_diseases.append("Malaria: Take antimalarial drugs and rest")

    # Dengue: Low Platelet + Normal/High WBC
    if abnormal_tests.get("Platelet Count") == "Low" and abnormal_tests.get("WBC Count") in ["High", None]:
        possible_diseases.append("Dengue: Monitor platelet count and stay hydrated")

    # Diabetes: High Blood Sugar
    if abnormal_tests.get("Blood Sugar (Fasting)") == "High":
        possible_diseases.append("Diabetes: Reduce sugar intake, exercise regularly")

    # Anemia
    if abnormal_tests.get("Hemoglobin") == "Low" and abnormal_tests.get("RBC Count") == "Low":
        possible_diseases.append("Anemia: Iron supplements and diet rich in iron")

    # High Cholesterol
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

    # ---------------- Display quick summary ----------------
    print("\n=== Test Summary ===")
    for test, (value, status) in patient_data.items():
        print(f"{test:<25}: {value:<10} → {status}")

    # ---------------- Prepare report content ----------------
    report_lines = []
    report_lines.append("BLOOD TEST ANALYSIS REPORT")
    report_lines.append("-----------------------------------")
    report_lines.append(f"Patient Name: {name}")
    report_lines.append(f"Age: {age}")
    report_lines.append(f"Gender: {gender}\n")

    report_lines.append("Test Results:")
    for test, (value, status) in patient_data.items():
        report_lines.append(f"{test}: {value} → {status}")

    report_lines.append("\nPossible Diseases & Doctor Advice:")
    for disease in possible_diseases:
        report_lines.append(f"{disease}: {doctor_advice[disease]}")

    # ---------------- Save individual report ----------------
    filename = f"{name.lower().replace(' ', '_')}_blood_report.txt"
    with open(filename, "w", encoding="utf-8") as file:
        for line in report_lines:
            file.write(line + "\n")

    print(f"\n✅ Report for {name} saved successfully as '{filename}'")

    # Return summary data for master report
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

    all_patients_summary = []

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

        summary = analyze_patient(name, age, gender, normal_ranges)
        all_patients_summary.append(summary)

    # ---------------- Master report ----------------
    if all_patients_summary:
        master_lines = []
        master_lines.append("MASTER BLOOD TEST SUMMARY REPORT")
        master_lines.append("--------------------------------")
        for patient in all_patients_summary:
            master_lines.append(f"\nPatient Name: {patient['Name']}, Age: {patient['Age']}, Gender: {patient['Gender']}")
            master_lines.append("Abnormal Tests:")
            if patient["Abnormal Tests"]:
                for test, status in patient["Abnormal Tests"].items():
                    master_lines.append(f"  - {test}: {status}")
            else:
                master_lines.append("  - None")

            master_lines.append("Diseases & Doctor Advice:")
            for disease in patient["Diseases"]:
                advice = patient["Doctor Advice"][disease]
                master_lines.append(f"  - {disease}: {advice}")
            master_lines.append("-" * 50)

        with open("master_blood_report.txt", "w", encoding="utf-8") as file:
            for line in master_lines:
                file.write(line + "\n")

        print("\n✅ Master Summary Report saved as 'master_blood_report.txt'")
    else:
        print("\nNo patient data entered. Master summary not created.")


# ---------------- Program Entry ----------------
if __name__ == "__main__":
    main()
