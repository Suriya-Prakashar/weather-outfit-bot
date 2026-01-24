import os

# Get current folder
cwd = os.getcwd()
print(f"🕵️ Scanning: {cwd}")

# 1. CHECK FOR COMMON NAMING ERRORS
# Windows often names it ".gitignore.txt" by mistake
wrong_name = os.path.join(cwd, ".gitignore.txt")
right_name = os.path.join(cwd, ".gitignore")

if os.path.exists(wrong_name):
    print("⚠️ FOUND ERROR: File is named '.gitignore.txt'")
    try:
        os.rename(wrong_name, right_name)
        print("✅ FIXED: Renamed to '.gitignore'")
    except Exception as e:
        print(f"❌ ERROR: Could not rename file. {e}")

# 2. CREATE IT IF IT DOESN'T EXIST
elif not os.path.exists(right_name):
    print("⚠️ MISSING: '.gitignore' file not found.")
    try:
        with open(right_name, "w") as f:
            f.write(".env\n__pycache__/\n*.log\n")
        print("✅ FIXED: Created a fresh '.gitignore' file.")
    except Exception as e:
        print(f"❌ ERROR: Could not create file. {e}")

# 3. VERIFY CONTENT
else:
    print("ℹ️ File '.gitignore' exists. Checking content...")
    with open(right_name, "r") as f:
        content = f.read()
    
    if ".env" not in content:
        print("⚠️ PROBLEM: '.env' is missing from the file.")
        with open(right_name, "a") as f:
            f.write("\n.env")
        print("✅ FIXED: Added '.env' to the ignore list.")
    else:
        print("✅ PERFECT: '.gitignore' is correctly named and includes '.env'.")

print("\n🎉 DONE. Now run 'git status' in your terminal again.")