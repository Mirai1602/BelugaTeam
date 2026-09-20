class Conversiones:

    @staticmethod
    def decimal_a_binario(numero):
        numero = int(numero)

        if numero == 0:
            return "0"

        signo = ""
        if numero < 0:
            signo = "-"
            numero = abs(numero)

        binario = []

        while numero > 0:
            residuo = numero % 2
            binario.append(str(residuo))
            numero //= 2

        return signo + "".join(reversed(binario))

    @staticmethod
    def binario_a_decimal(binario):
        binario = str(binario).strip()

        if not binario:
            raise ValueError("El número binario no puede estar vacío.")

        signo = 1

        if binario.startswith("-"):
            signo = -1
            binario = binario[1:]

        if not binario or any(bit not in "01" for bit in binario):
            raise ValueError("Ingrese solamente 0 y 1.")

        decimal = 0

        for i, bit in enumerate(reversed(binario)):
            decimal += int(bit) * (2 ** i)

        return signo * decimal

    @staticmethod
    def decimal_a_hexadecimal(numero):
        numero = int(numero)

        if numero == 0:
            return "0"

        signo = ""

        if numero < 0:
            signo = "-"
            numero = abs(numero)

        digitos = "0123456789ABCDEF"
        hexadecimal = []

        while numero > 0:
            residuo = numero % 16
            hexadecimal.append(digitos[residuo])
            numero //= 16

        return signo + "".join(reversed(hexadecimal))

    @staticmethod
    def hexadecimal_a_decimal(hexadecimal):
        hexadecimal = str(hexadecimal).strip().upper()

        if not hexadecimal:
            raise ValueError("El número hexadecimal no puede estar vacío.")

        signo = 1

        if hexadecimal.startswith("-"):
            signo = -1
            hexadecimal = hexadecimal[1:]

        digitos = "0123456789ABCDEF"

        if not hexadecimal or any(digito not in digitos for digito in hexadecimal):
            raise ValueError("Ingrese un número hexadecimal válido.")

        decimal = 0

        for i, digito in enumerate(reversed(hexadecimal)):
            valor = digitos.index(digito)
            decimal += valor * (16 ** i)

        return signo * decimal
