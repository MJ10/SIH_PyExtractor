### Setting up the Database
```mysql
- CREATE DATABASE PyExtractor CHARACTER SET UTF8;
- CREATE USER sih@localhost IDENTIFIED BY 'ISRO@PyE18';
- GRANT ALL PRIVILEGES ON PyExtractor.* TO sih@localhost;
- FLUSH PRIVILEGES;
```

## Setup virtual environment
```
- virtualenv -p python3 pyExtractor
- cd pyExtractor/
- source bin/activate
- git clone https://github.com/MJ10/SIH_PyExtractor.git
- cd SIH_PyExtractor/
- pip install -r requirements.txt 
```

### External Dependencies

- Tesseract-OCR
- Open-CV