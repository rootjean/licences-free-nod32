import asyncio
from eset import registrar_cuenta, generar_password, generar_usuario
from mailtemp import crear_email_temporal, confirmar_cuenta


def main():
    user = "usua" + generar_usuario()
    email_pass = "Pass123"
    password_eset = generar_password()

    email, token = crear_email_temporal(user, email_pass)

    print(f"Email generado: {email}")
    print(f"Password ESET: {password_eset}")

    registrar_cuenta(email, password_eset)

    asyncio.run(confirmar_cuenta(token))


if __name__ == "__main__":
    main()
