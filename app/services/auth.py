from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user import UserService
from app.core.security import verify_password,loginTokens

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
        self.user_service = UserService(db)
    
    async def login_by_email_or_username_and_password(self,email_or_username: str, password: str):
        
        if "@" in email_or_username:
            user_in_db = await self.user_service.get_user_by_email(email_or_username)
        else:
            user_in_db = await self.user_service.get_user_by_username(email_or_username)
        
        if not user_in_db:
            return {"message" : "email or username in invalid!"}
        
        if not verify_password(password, user_in_db.password):
            return {"message" : "password is invalid!"}
            
        login_token = loginTokens(user_in_db.id)
            
        return{
            "id": user_in_db.id,
            "email": user_in_db.email,
            "username": user_in_db.user_name,
            "fullname": user_in_db.full_name,
            "phone_no": user_in_db.phone_no,
            "gender": user_in_db.gender,
            "created_at": user_in_db.created_at,
            "updated_at": user_in_db.update_ar
        } 