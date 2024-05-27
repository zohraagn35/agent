from cx_Freeze import setup, Executable

# List of additional files to include
include_files = ['gui.py', 'tasks.py', 'main.py', 'agent2.png']

# Define the executables
executables = [Executable("main.py", base="Win32GUI")]

setup(
    name="agent DOT1x",
    version="1.0",
    description="801.1x agent",
    options={"build_exe": {"include_files": include_files}},
    executables=executables
)
