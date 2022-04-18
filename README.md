# **FFnet to AO3** 

This programs transfers any story from Fanfiction.net to AO3. Please use this only for stories that you have claims to.

# Web Version

Instead of using this as a library, you may use this directly as a web application at [ffn-to-ao3.herokuapp.com](https://ffn-to-ao3.herokuapp.com)

(Currently down for maintenance)

# Usage

### Install:
  `pip install ffnToAO3`
  
### Dependencies:
  `pip install MechanicalSoup` 
  (https://github.com/MechanicalSoup/MechanicalSoup)
  
  `pip install cloudscraper`
  (https://github.com/VeNoMouS/cloudscraper)
  
  `easy_install BeautifulSoup4` or `pip install bs4`

### Example (in command line)

```
python

>>> from ffnToAO3 import uploadAO3

>>> uploadAO3.upload()
```

### Example Program Display

```
>>> from ffnToAO3 import uploadAO3
>>> uploadAO3.upload()
Heading to AO3...
Enter your AO3 username: Clostone
Enter your AO3 password: 12345678
Logged in successfully...
Heading to ffnet...
Your ffnet username (case sensitive): CCS
Getting list of works...
	 if chapters are not displaying, restart the app.
1. Rabbit Dreams
2. Hawks
3. Jane's Day Off
4. Ferris Wheel Accident
5. 1982: Summer, a river


Select work from 1 to 5 to move to AO3:

2
Story to be transfered -----
story title: Hawks
story link: http://fanfiction.net/s/1727272238/1/Hawks
----------------------------
Getting metadata...
getting a total of 4 chapters...
Getting metadata...
transferring metadata and story content...
Chapter 1 posted.
New work url: https://archiveofourown.org/works/6461772348
Chapter 2 posted.
Chapter 3 posted.
Chapter 4 posted.
Done.

```


# Notes

The program will require you to log into AO3 (but not fanfiction.net)
While uploading, it will also download a copy of your story to your local drive.

This is a console-based program, which means there's no display and all input/logging will occur in console.


# Troubleshooting

- "select work from 1 to 0": please restart to app

- "cannot find relative path": this may happen if you're running the code yourself. If this occurs, go into uploadAO3.py and remove 'from .' from the import statement 'from . import get_ffn'


# Credits

metadata scraping for ffn is based on https://github.com/smilli/fanfiction's scraping method.
