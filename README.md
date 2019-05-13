# olea-v2

This project is the next version of `olea` and runs on a full featured server, instead of GAE, (actually, I rewrite almost all the codes).

## Environment

This project is developing and testing with `Python 3.7.3 X86-64` under `Windows 10 17763.437` – with many automatic scripts and VS Code. (NOTE: I will switch to the newest stable release as soon as possible in the future)

If you are working on Windows as well, DO NOT tick `download debug symbols` checkbook when installing Python, or you cannot create a virtual environment via `venv` (I have no idea about how it affect `venv`).

To set up the environment for DEV (and for PROD), just simply run the `setup_env.ps1` in `tools` folder. See `README.md` file under the same folder for more details.
