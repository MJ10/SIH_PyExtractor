import exifread as ef
from PIL import Image
# import os

# barrowed from 
# https://gist.github.com/snakeye/fdc372dbf11370fe29eb 
def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


def getData(filepath):
    '''
    returns gps data if present other wise returns empty dictionary
    '''
    # print(filepath)
    # dateTaken = Image.open(filepath)._getexif()[36867]
    with open(filepath, 'rb') as f:
        tags = ef.process_file(f)
        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')
        dateTaken = tags.get("Image DateTime")
        print(dateTaken)
        if latitude:
            lat_value = _convert_to_degress(latitude)
            if latitude_ref.values != 'N':
                lat_value = -lat_value
        else:
            return {'latitude': None, 'longitude': None, 'dateTaken': dateTaken}
        if longitude:
            lon_value = _convert_to_degress(longitude)
            if longitude_ref.values != 'E':
                lon_value = -lon_value
        else:
            return {'latitude': None, 'longitude': None, 'dateTaken': dateTaken}
        return {'latitude': lat_value, 'longitude': lon_value, 'dateTaken': dateTaken}
    return {'latitude': None, 'longitude': None, 'dateTaken': dateTaken}


# Testing Module

# for file in os.listdir(os.getcwd()):
# 	if(file.find('.jpg')):		
# 		file_path = file   
# 		gps = getGPS(file_path)
# 		print(gps)