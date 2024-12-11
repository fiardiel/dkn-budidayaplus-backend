from ninja import Schema, Field
from pydantic import UUID4, field_validator
from typing import Optional

class ProfileInputSchema(Schema):
    image_name: Optional[str] = ''

class UserSchema(Schema):
    id: int
    phone_number: str = Field(alias='username')
    first_name: str
    last_name: str

class ProfileSchema(Schema):
    id: UUID4
    user: UserSchema
    image_name: Optional[str] = ''
    role: str

class UpdateProfileSchema(Schema):
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
    image_name: Optional[str] = ''

class WorkerSchema(Schema):
    id: UUID4
    first_name: Optional[str]= ''
    last_name: Optional[str]= ''
    phone_number: str

class CreateWorkerSchema(Schema):
    phone_number: str
    first_name: str
    last_name: str
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError('Password harus minimal 8 karakter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password harus mengandung angka')
        if not any(c.isalpha() for c in v):
            raise ValueError('Password harus mengandung huruf')
        return v

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v: str):
        if not v.isdigit():
            raise ValueError('Nomor telefon harus berupa angka')
        if not v.startswith('08'):
            raise ValueError('Nomor telefon harus dimulai dengan 08')
        if len(v) < 10:
            raise ValueError('Nomor telefon harus minimal 10 digit')
        if len(v) > 13:
            raise ValueError('Nomor telefon anda maksimal 13 digit')
        return v
