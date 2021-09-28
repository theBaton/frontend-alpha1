from flask_jwt_extended import JWTManager

jwt = JWTManager()

from .UserView import user_api
from .ProfileView import profile_api
#from .BlogpostView import blogpost_api
#from .EditorialView import editorial_api
#from .PodcastView import podcast_api
