from HMS_SYSTEM_PROJECT.database import connect_to_db
from admin_menu import admin_menu

def login():
    # Clear screen for a fresh start on login attempt
    print("\033c", end="")  # ANSI escape sequence to clear screen (works on most terminals)

    # Prompt for username and password
    username = input("👉 Enter your username: ").strip()
    password = input("🔒 Enter your password: ").strip()

    # Connect to the database to verify credentials
    db = connect_to_db()
    cursor = db.cursor()

    query = "SELECT role FROM Users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        role = result[0]
        print(f"\n🎉 Login successful! 🎉\nRole: {role}\n")

        # Redirect based on role
        if role == "Admin":
            print("🔑 Redirecting to Admin Dashboard...")
            admin_menu()
        elif role == "Doctor":
            from HMS_SYSTEM_PROJECT.doctor_menu import doctor_menu
            print("👨‍⚕️ Redirecting to Doctor Dashboard...")
            doctor_menu(username)
        elif role == "Patient":
            from HMS_SYSTEM_PROJECT.patient_menu import patient_menu
            print("👩‍⚕️ Redirecting to Patient Dashboard...")
            patient_menu(username)
        else:
            print("🚨 Unknown role. Please contact the admin.")
    else:
        print("\n❌ Invalid credentials. Please try again. ❌")

    # Close the database connection
    cursor.close()
    db.close()
