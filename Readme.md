# emex2md

A simple script to convert all your evernote notebooks to markdown files. Useful if you're moving from evernote to obsidian after the recent [evernote free tier limitations update](https://help.evernote.com/hc/en-us/articles/23565231682323-Note-and-notebook-limits-in-Evernote-Free-December-2023).

# Features

- Converts each note inside your notebook into a separate markdown file with another file named `timeline.md` storing all the timestamps and tags associated with each note, all linked together via the [obsidian internal links](https://help.obsidian.md/Linking+notes+and+files/Internal+links).

# Usage

1. Install necessary python dependencies

```
pip install -r requirements.txt
```

2. Export all your evernote notebooks into the `input` folder

3. Run the following command to trigger the conversion.

```
python emex2md.py
```
