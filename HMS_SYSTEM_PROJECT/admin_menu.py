from HMS_SYSTEM_PROJECT.database import connect_to_db


def admin_menu():
    while True:
        print("\n" + "=" * 50)
        print("               👩‍⚕️ ADMIN DASHBOARD 👨‍⚕️")
        print("=" * 50)
        print("1️⃣  Add Doctor")
        print("2️⃣  Add Patient")
        print("3️⃣  View Doctors")
        print("4️⃣  View Patients")
        print("5️⃣  View Appointments")
        print("6️⃣  Appoint Patient to Doctor")
        print("7️⃣  Logout")
        print("=" * 50)
        choice = input("➡️  Enter your choice: ").strip()

        if choice == "1":
            add_doctor()
        elif choice == "2":
            add_patient()
        elif choice == "3":
            view_doctors()
        elif choice == "4":
            view_patients()
        elif choice == "5":
            view_appointments()
        elif choice == "6":
            appoint_patient_to_doctor()
        elif choice == "7":
            print("\n🔒 Logging out... Goodbye, Admin!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


# Add Doctor
def add_doctor():
    db = connect_to_db()
    cursor = db.cursor()

    name = input("Enter doctor's name: ").strip()
    specialization = input("Enter doctor's specialization: ").strip()
    phone = input("Enter doctor's phone: ").strip()
    password = input("Set a password for the doctor: ").strip()

    try:
        query = "INSERT INTO Doctors (name, specialization, phone) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, specialization, phone))
        doctor_id = cursor.lastrowid

        username = name
        user_query = "INSERT INTO Users (username, password, role, user_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(user_query, (username, password, "doctor", doctor_id))

        db.commit()
        print(f"✅ Doctor added successfully. Username: {username}, Role: doctor")
    except Exception as e:
        db.rollback()
        print(f"❌ Error occurred: {e}")
    finally:
        cursor.close()
        db.close()


# Add Patient
def add_patient():
    db = connect_to_db()
    cursor = db.cursor()

    name = input("Enter patient's name: ").strip()
    age = input("Enter patient's age: ").strip()
    disease = input("Enter patient's disease: ").strip()
    password = input("Set a password for the patient: ").strip()

    try:
        query = "INSERT INTO Patients (name, age, disease) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, age, disease))
        patient_id = cursor.lastrowid

        username = name
        user_query = "INSERT INTO Users (username, password, role, user_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(user_query, (username, password, "patient", patient_id))

        db.commit()
        print(f"✅ Patient added successfully. Username: {username}, Role: patient")
    except Exception as e:
        db.rollback()
        print(f"❌ Error occurred: {e}")
    finally:
        cursor.close()
        db.close()


# View Doctors
def view_doctors():
    db = connect_to_db()
    cursor = db.cursor()

    query = "SELECT * FROM Doctors"
    cursor.execute(query)
    doctors = cursor.fetchall()

    if doctors:
        print("\n" + "=" * 50)
        print("              👩‍⚕️ DOCTORS LIST 👨‍⚕️")
        print("=" * 50)
        print(f"{'ID':<5} {'Name':<30} {'Specialization':<20} {'Phone':<15}")
        print("-" * 70)
        for doctor in doctors:
            print(f"{doctor[0]:<5} {doctor[1]:<30} {doctor[2]:<20} {doctor[3]:<15}")
    else:
        print("❌ No doctors found.")

    print("=" * 50)
    cursor.close()
    db.close()


# View Patients
def view_patients():
    db = connect_to_db()
    cursor = db.cursor()

    query = "SELECT * FROM Patients"
    cursor.execute(query)
    patients = cursor.fetchall()

    if patients:
        print("\n" + "=" * 50)
        print("             👩‍⚕️ PATIENTS LIST 👨‍⚕️")
        print("=" * 50)
        print(f"{'ID':<5} {'Name':<30} {'Age':<5} {'Disease':<30}")
        print("-" * 70)
        for patient in patients:
            print(f"{patient[0]:<5} {patient[1]:<30} {patient[2]:<5} {patient[3]:<30}")
    else:
        print("❌ No patients found.")

    print("=" * 50)
    cursor.close()
    db.close()


def view_appointments():
    db = connect_to_db()
    cursor = db.cursor()

    query = """
    SELECT p.name AS Patient, d.name AS Doctor, a.appointment_date 
    FROM Appointments a
    JOIN Patients p ON a.patient_id = p.patient_id
    JOIN Doctors d ON a.doctor_id = d.doctor_id
    """
    cursor.execute(query)
    appointments = cursor.fetchall()

    if appointments:
        print("\n" + "=" * 50)
        print("           📝 APPOINTMENTS LIST 📝")
        print("=" * 50)
        print(f"{'Patient':<30} {'Doctor':<30} {'Appointment Date':<20}")
        print("-" * 90)
        for appointment in appointments:
            # Ensure appointment_date is in correct format
            appointment_date = appointment[2].strftime("%Y-%m-%d") if appointment[2] else "N/A"
            print(f"{appointment[0]:<30} {appointment[1]:<30} {appointment_date:<20}")
    else:
        print("❌ No appointments found.")

    print("=" * 50)
    cursor.close()
    db.close()


# Appoint Patient to Doctor
def appoint_patient_to_doctor():
    db = connect_to_db()
    cursor = db.cursor()

    print("\nAvailable Patients:")
    query = "SELECT patient_id, name FROM Patients"
    cursor.execute(query)
    patients = cursor.fetchall()
    for patient in patients:
        print(f"🆔 ID: {patient[0]}, Name: {patient[1]}")

    patient_id = int(input("➡️ Enter Patient ID: "))

    print("\nAvailable Doctors:")
    query = "SELECT doctor_id, name FROM Doctors"
    cursor.execute(query)
    doctors = cursor.fetchall()
    for doctor in doctors:
        print(f"🆔 ID: {doctor[0]}, Name: {doctor[1]}")

    doctor_id = int(input("➡️ Enter Doctor ID: "))
    appointment_date = input("➡️ Enter appointment date (YYYY-MM-DD): ").strip()

    try:
        query = "INSERT INTO Appointments (patient_id, doctor_id, appointment_date) VALUES (%s, %s, %s)"
        cursor.execute(query, (patient_id, doctor_id, appointment_date))
        db.commit()
        print("✅ Appointment successfully created.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error occurred: {e}")
    finally:
        cursor.close()
        db.close()
