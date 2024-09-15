import sys
import streamlit.web.bootstrap as bootstrap

if __name__ == "__main__":
    print("Debug: Starting launch_gui.py")
    bootstrap.run("aider/gui.py", "", sys.argv, flag_options={})
    print("Debug: Exiting launch_gui.py")