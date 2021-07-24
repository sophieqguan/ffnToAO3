# **FFnet to AO3** 

This programs transfers any story from Fanfiction.net to AO3. Please use this only for stories that you have claims to.


# Usage

### Install (run in command line):
  `pip install ffnToAO3`
*make sure you have python installed. If not, head over to [python installation](https://www.python.org/downloads/)

### Dependencies:
  `pip install MechanicalSoup` 
  [(mechanical soup)](https://github.com/MechanicalSoup/MechanicalSoup)
  
  `pip install cloudscraper`
  [(cloudscraper)](https://github.com/VeNoMouS/cloudscraper)
  
  `easy_install BeautifulSoup4` or `pip install bs4`

### Example

```
from ffnToAO3.ffnToAO3 import uploadAO3

uploadAO3.upload()
```

### Example Program Display

```
>>> from ffnToAO3.ffnToAO3 import uploadAO3
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

If error occurs (e.g. did not locate all chapters), please rerun the program. 

# Credits

metadata scraping for ffn is based on https://github.com/smilli/fanfiction scraping method.
