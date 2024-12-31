from HMS_SYSTEM_PROJECT.database import connect_to_db


# Doctor Menu
def doctor_menu(username):
    db = connect_to_db()
    cursor = db.cursor()

    query = "SELECT doctor_id FROM Doctors WHERE name = %s"
    cursor.execute(query, (username,))
    doctor_data = cursor.fetchone()

    if not doctor_data:
        print("\n🚫 Doctor not found. Please contact the hospital administration.")
        cursor.close()
        db.close()
        return

    doctor_id = doctor_data[0]
    cursor.close()
    db.close()

    while True:
        print("\n" + "=" * 50)
        print("               🩺 DOCTOR DASHBOARD 🩺")
        print("=" * 50)
        print("1️⃣  View Assigned Patients")
        print("2️⃣  Generate Patient Report")
        print("3️⃣  Generate Bill")
        print("4️⃣  Logout")
        print("=" * 50)
        choice = input("➡️  Enter your choice: ").strip()

        if choice == "1":
            view_assigned_patients(doctor_id)
        elif choice == "2":
            generate_report(doctor_id)
        elif choice == "3":
            generate_bill(doctor_id)
        elif choice == "4":
            print("\n🔒 Logging out... Stay safe, Doctor!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


# View Assigned Patients for Doctor
def view_assigned_patients(doctor_id):
    db = connect_to_db()
    cursor = db.cursor()

    query = """
    SELECT p.name, p.age, p.disease, a.appointment_date
    FROM Patients p
    JOIN Appointments a ON p.patient_id = a.patient_id
    WHERE a.doctor_id = %s
    """
    cursor.execute(query, (doctor_id,))
    patients = cursor.fetchall()

    print("\n" + "=" * 50)
    print("              👩‍⚕️ ASSIGNED PATIENTS 👨‍⚕️")
    print("=" * 50)

    if patients:
        for patient in patients:
            print(f"🆔 Patient Name    : {patient[0]}")
            print(f"🎂 Age            : {patient[1]}")
            print(f"🩺 Disease        : {patient[2]}")
            print(f"📅 Appointment    : {patient[3]}")
            print("-" * 50)
    else:
        print("❌ No patients assigned to you at the moment.")

    print("=" * 50)
    cursor.close()
    db.close()


# Generate Patient Report for Doctor
def generate_report(doctor_id):
    db = connect_to_db()
    cursor = db.cursor()

    patient_name = input("Enter patient name to generate report: ").strip()
    query = "SELECT disease FROM Patients WHERE name = %s"
    cursor.execute(query, (patient_name,))
    result = cursor.fetchone()

    print("\n" + "=" * 50)
    print("              📝 PATIENT REPORT 📝")
    print("=" * 50)

    if result:
        print(f"🆔 Patient Name    : {patient_name}")
        print(f"🩺 Disease/Condition: {result[0]}")
    else:
        print("❌ Patient not found.")

    print("=" * 50)
    cursor.close()
    db.close()


def generate_bill(doctor_id):
    db = connect_to_db()
    cursor = db.cursor()

    patient_name = input("Enter patient name to generate bill: ").strip()
    query = "SELECT patient_id FROM Patients WHERE name = %s"
    cursor.execute(query, (patient_name,))
    patient_data = cursor.fetchone()

    print("\n" + "=" * 50)
    print("              💵 BILLING DETAILS 💵")
    print("=" * 50)

    if patient_data:
        patient_id = patient_data[0]
        amount = float(input("💰 Enter bill amount: $"))
        status = "Unpaid"  # Using valid ENUM value for status

        try:
            # Debugging: print the query and data
            print(
                f"Executing query: INSERT INTO Bills (patient_id, amount, status) VALUES ({patient_id}, {amount}, '{status}')")

            bill_query = "INSERT INTO Bills (patient_id, amount, status) VALUES (%s, %s, %s)"
            cursor.execute(bill_query, (patient_id, amount, status))
            db.commit()
            print(f"💳 Bill generated for {patient_name}.")
        except Exception as e:
            db.rollback()  # Rollback if an error occurs
            print(f"❌ Error occurred while generating the bill: {e}")
    else:
        print("❌ Patient not found.")

    print("=" * 50)
    cursor.close()
    db.close()
