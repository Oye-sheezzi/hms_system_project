from HMS_SYSTEM_PROJECT.database import connect_to_db

# Patient Menu
def patient_menu(username):
    db = connect_to_db()
    cursor = db.cursor()

    query = "SELECT patient_id FROM Patients WHERE name = %s"
    cursor.execute(query, (username,))
    patient_data = cursor.fetchone()

    if not patient_data:
        print("\n🚫 Patient not found. Please contact the hospital administration.")
        cursor.close()
        db.close()
        return

    patient_id = patient_data[0]

    cursor.close()
    db.close()

    while True:
        print("\n" + "=" * 50)
        print("               🏥 PATIENT DASHBOARD 🏥")
        print("=" * 50)
        print("1️⃣  View Medical Report")
        print("2️⃣  View Billing Details")
        print("3️⃣  Logout")
        print("=" * 50)
        choice = input("➡️  Enter your choice: ").strip()

        if choice == "1":
            view_patient_report(patient_id)
        elif choice == "2":
            view_patient_bill(patient_id)
        elif choice == "3":
            print("\n🔒 Logging out... Have a great day!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

# View Patient Report
def view_patient_report(patient_id):
    db = connect_to_db()
    cursor = db.cursor()

    query = "SELECT disease FROM Patients WHERE patient_id = %s"
    cursor.execute(query, (patient_id,))
    result = cursor.fetchone()

    print("\n" + "=" * 50)
    print("               📋 MEDICAL REPORT 📋")
    print("=" * 50)
    if result:
        print(f"🆔 Patient ID       : {patient_id}")
        print(f"💊 Disease/Condition: {result[0]}")
    else:
        print("❌ No medical report found for the patient.")
    print("=" * 50)

    cursor.close()
    db.close()

# View Patient Bill
def view_patient_bill(patient_id):
    db = connect_to_db()
    cursor = db.cursor()

    query = "SELECT amount, status FROM Bills WHERE patient_id = %s"
    cursor.execute(query, (patient_id,))
    bill = cursor.fetchone()

    print("\n" + "=" * 50)
    print("               💵 BILLING DETAILS 💵")
    print("=" * 50)
    if bill:
        amount, status = bill
        print(f"🆔 Patient ID : {patient_id}")
        print(f"💰 Bill Amount: ${amount:.2f}")
        print(f"📄 Bill Status: {status}")
        if status.lower() == "unpaid":
            print("⚠️  Note: Please clear your dues at the earliest convenience.")
    else:
        print("❌ No billing details found for the patient.")
    print("=" * 50)

    cursor.close()
    db.close()
