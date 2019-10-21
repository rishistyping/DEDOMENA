import requests
import shutil
import os   

def download_MODIS_image(num_images, year, month, day, max_day, max_month, end_date):
    
    # input params
    # param 1: number of images to download (for this URL, don't go over 80)
    # param 2: date of image; e.g. date = '2012-07-09'
    
    if month < 10 and day < 10:
        date = str(year) + '-0' + str(month) + '-0' + str(day)
    elif month < 10 and day >= 10:
        date = str(year) + '-0' + str(month) + '-' + str(day)
    elif month >= 10 and day < 10:
        date = str(year) + '-' + str(month) + '-0' + str(day)
    else:
        date = str(year) + '-' + str(month) + '-' + str(day)
        
    
    #max_day = 30   # not going to take the data from 31st day of any month (future imoprovement)
    #max_month = 12
    
    image_num = 0
    
    for m in range(month, max_month+1):
        for d in range(day, max_day+1):            
            for i in range(num_images):
                
                if date == end_date:
                    print 'end date ', end_date, ' reached'
                    break            
                image_id = i
                #image_num = str(img_counter)
                url = 'https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/' + date + '/250m/6/13/' + str(image_id) + '.jpg'
                
                #Save file in local hard drive
                filepath = 'D:\SpaceApps2019\Chasers_of_lost_data\downloads\images_modis_nasa\\'
                filename = 'nasa_modis_image_' + date + '_' + str(image_num) + '.jpg'
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
                    print 'image #', image_num, 'downloaded'
                else:
                    print 'image #', image_num, 'is a zero sized file --> invalid image'
                    
                image_num += 1
            

#### MAIN ####

# Loop over dates in a month to download in larger batches
#num_images = 80
#day = 1
#month = 7
#year = 2019
#max_day = 30
#max_month = 9
#end_date = '2019-09-15'

#download_MODIS_image(num_images, year, month, day, max_day, max_month, end_date)