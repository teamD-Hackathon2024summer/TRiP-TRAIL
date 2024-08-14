from typing import Optional
from pydantic import BaseModel, validator
import re
from datetime import date as dt_date
import datetime

# ユーザー登録のバリテーション
class UserCreate(BaseModel):
    user_name: str 
    email: str 
    password1: str 
    password2: str 
    user_address: str 

    # ユーザー名が空でないことを確認
    @validator('user_name')
    def name_not_empty(cls, v):
        if not v:
            raise ValueError('Name must be filled')
        return v

    # メールアドレスが空でないことを確認
    @validator('email')
    def email_not_empty(cls, v):
        if not v:
            raise ValueError('Email must be filled')
        return v
    
    #メールアドレスの形式の確認
    @validator('email')
    def validate_email_format(cls, v):
        pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v

    # パスワード1が空でないことを確認
    @validator('password1')
    def password1_not_empty(cls, v):
        if not v:
            raise ValueError('Password1 must be filled')
        return v
    
    # パスワード2が空でないことを確認
    @validator('password2')
    def password1_not_empty(cls, v):
        if not v:
            raise ValueError('Password2 must be filled')
        return v
    
    # 現住所が空でないことを確認
    @validator('user_address')
    def address_not_empty(cls, v):
        if not v:
            raise ValueError('Address must be filled')
        return v
    
    # パスワードが一致するかを確認
    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('Passwords do not match')
        return v

# ログインのバリテーション
class LoginForm(BaseModel):
    email: str
    password: str
    
    # # メールアドレスが空でないことを確認
    # @validator('email')
    # def email_not_empty(cls, v):
    #     if not v:
    #         raise ValueError('Email must be filled')
    #     return v
    
    # #メールアドレスの形式の確認
    # @validator('email')
    # def validate_email_format(cls, v):
    #     pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    #     if not re.match(pattern, v):
    #         raise ValueError('Invalid email format')
    
    # # パスワードが空でないことを確認
    # @validator('password')
    # def password_not_empty(cls, v):
    #     if not v:
    #         raise ValueError('Password must be filled')
    
#ユーザー情報変更のバリテーション
class UserEdit(BaseModel):
    user_name: Optional[str] = None
    email: Optional[str] = None
    password1: Optional[str] = None
    password2: Optional[str] = None
    user_address: Optional[str] = None  

    # メールアドレスがNoneでない場合の形式の確認
    @validator('email', pre=True, always=True)
    def validate_email_format(cls, v):
        if v is None:
            return v
        pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v

    # パスワードがNoneでない場合に一致するかを確認
    @validator('password2', pre=True, always=True)
    def passwords_match(cls, v, values, **kwargs):
        if v is None:
            return v
        if 'password1' in values and v != values['password1']:
            raise ValueError('Passwords do not match')
        return v

# スケジュール追加のバリテーション
class ScheduleCreate(BaseModel):
    date: dt_date
    destination: str
    destination_address: str

# 過去の日付でないことを確認
    @validator('date')
    def validate_date(cls, v):
        if v and v < dt_date.today():
            raise ValueError('The date cannot be in the past.')
        return v

    # 日付が空でないことを確認
    @validator('date')
    def name_not_empty(cls, v):
        if not v:
            raise ValueError('Date must be filled')
        return v

    # 目的地名称が空でないことを確認
    @validator('destination')
    def email_not_empty(cls, v):
        if not v:
            raise ValueError('Destination must be filled')
        return v

    # 目的地住所が空でないことを確認
    @validator('destination_address')
    def password1_not_empty(cls, v):
        if not v:
            raise ValueError('Destination_address must be filled')
        return v

# スケジュール変更のバリテーション
class ScheduleEdit(BaseModel):
    date: Optional[dt_date] = None
    destination: Optional[str] = None
    destination_address: Optional[str] = None

    # 過去の日付でないことを確認
    @validator('date')
    def validate_date(cls, v):
        if v and v < dt_date.today():
            raise ValueError('The date cannot be in the past.')
        return v
