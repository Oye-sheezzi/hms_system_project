from login import login

def main():
    # Clear screen to provide a fresh interface each time
    print("\033c", end="")  # ANSI escape sequence to clear the screen (works on most terminals)

    # Using emojis for a more appealing layout
    print("=" * 60)
    print(f"{'💖 Welcome to Hospital Management System 💖':^60}")
    print("=" * 60)
    print("\n👩‍⚕️👨‍⚕️ Please log in to continue. 🔑\n")

    # Call the login function to authenticate the user
    login()

if __name__ == "__main__":
    main()
