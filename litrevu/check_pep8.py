import os

# From Python3.7 you can add
# keyword argument capture_output
error = False
print("Running pep8 tools...")
print("isort .")
error |= bool(os.system("isort ."))
print("black .")
error |= bool(os.system("black ."))
print("flake8 .")
error |= bool(os.system("flake8 ."))
if error:
    print("There are pep8 errors in your code. Please fix them.")
else:
    print("all done!")
