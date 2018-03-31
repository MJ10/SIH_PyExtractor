
### Install Dependencies



#### MySQL
* `sudo apt-get install mysql-server-5.7`
* `sudo apt-get install libmysqlclient-dev`


### Setting up the Database

`mysql -u <username> -p`

```mysql
CREATE DATABASE PyExtractor CHARACTER SET UTF8;
CREATE USER sih@localhost IDENTIFIED BY 'ISRO@PyE18';
GRANT ALL PRIVILEGES ON PyExtractor.* TO sih@localhost;
FLUSH PRIVILEGES;
```

## Setup virtual environment
```bash
virtualenv -p python3 pyExtractor
cd pyExtractor/
source bin/activate
git clone https://github.com/MJ10/SIH_PyExtractor.git
cd SIH_PyExtractor/
pip install -r requirements.txt 
```

### External Dependencies

- Tesseract-OCR
- Open-CV

### Offline Map using OpenStreetMap and LeafletJS
* Download the vectorised map file of the required area.
* Run the server on port 8080
`tileserver-gl-light 2017-07-03_asia_india.mbtiles `
