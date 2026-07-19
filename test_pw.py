from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
print(pwd_context.verify('admin123', '$2b$12$WLTQfdoW9zrF3gt4cVEuoe25w71XMkncKpXXTCRiwwEbbHzVpjRUm'))
