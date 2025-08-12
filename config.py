import cloudinary



class config:
    SECRET_KEY = 'secretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    
cloudinary.config( 
    cloud_name = "dsxlk12bs", 
    api_key = "534613577116544", 
    api_secret = "poDHs5c_IrodeHgifY1grJ3HwUw"
)