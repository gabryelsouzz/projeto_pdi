# 1.Make this directory use a specific Python version

`pyenv local 3.12.13`

# 2.Use pyenv to create a venv in .venv

`pyenv exec python -m venv .venv`

# 3.Activate venv

## A.Linux/macOS

`source .venv/bin/activate`

## B.Windows PowerShell (if applicable)

`.venv\Scripts\Activate.ps1`

---

# 4.Install requirements

`pip install -r requirements.txt`

---

# 5.Register this local python version as a Jupyter kernel

`python -m ipykernel install --user --name projeto_pdi --display-name "Projeto PDI"`

---

# 6.Run the desktop UI

`python run.py`

> The UI uses Tkinter/CustomTkinter, so the Python interpreter must be built with
> Tk support. If `python run.py` fails with `ModuleNotFoundError: No module named '_tkinter'`,
> install the Tk system dependency for your interpreter, e.g. on macOS with Homebrew:
> `brew install python-tk@3.12`
