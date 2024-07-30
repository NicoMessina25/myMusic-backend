from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.users.models import User
from app.profiles.models import EProfile
from typing import List

def authenticate_user(profiles_required: List[EProfile] = None):
    verify_jwt_in_request()
    user = User.get_user_by_username(get_jwt_identity())
    
    # Si no se requieren perfiles específicos, simplemente devuelve el usuario autenticado
    if not profiles_required:
        return user
    
    # Verifica si el profileId del usuario está en la lista de perfiles permitidos
    if user.profileId in [profile.value for profile in profiles_required]:
        return user
    
    # Si el perfil del usuario no está en la lista permitida, lanza un error de permiso
    raise PermissionError(f"El usuario con el perfil {user.profileId} no tiene permiso para usar esta función")