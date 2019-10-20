import requests
import shutil
import os   

def download_MODIS_image(num_images, date):
    
    # input params
    # param 1: number of images to download (for this URL, don't go over 80)
    # param 2: date of image; e.g. date = '2012-07-09'
    for i in range(num_images):
        
        img_counter = i
        image_num = str(img_counter)
        Date = date
        url = 'https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/' + Date + '/250m/6/13/' + image_num + '.jpg'
        
        #Save file in local hard drive
        filepath = 'D:\SpaceApps2019\Chasers_of_lost_data\downloads\images_modis_nasa\\'
        filename = 'nasa_modis_image_' + Date + '_' + image_num + '.jpg'
        full_filepath = filepath + filename
        
        # Open the url image, set stream to True, this will return the stream content.
        response = requests.get(url, stream=True)
            
        # Open a local file with wb ( write binary ) permission.
        local_file = open(full_filepath, 'wb')
        
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        response.raw.decode_content = True
        
        # Copy the response stream raw data to local image file.
        shutil.copyfileobj(response.raw, local_file)
        
        # Remove the image url response object.
        local_file.close()
        del response
        
        filesize = os.path.getsize(full_filepath)
        if filesize > 428:
            print 'image #', img_counter, 'downloaded'
        else:
            print 'image #', img_counter, 'is a zero sized file --> invalid image'
            

