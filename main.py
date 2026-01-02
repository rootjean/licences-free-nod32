import asyncio
from eset import registrar_cuenta, generar_password, generar_usuario
from mailtemp import crear_email_temporal, confirmar_cuenta


async def main():
    user = "usua" + generar_usuario()
    email_pass = "Pass123"
    password_eset = generar_password()

    email, token = crear_email_temporal(user, email_pass)

    print(f"Email generado: {email}")
    print(f"Password ESET: {password_eset}")

    await asyncio.gather(
        registrar_cuenta(email, password_eset),
        confirmar_cuenta(token)
    )


if __name__ == "__main__":
    asyncio.run(main())