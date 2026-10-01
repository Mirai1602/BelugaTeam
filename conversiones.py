class Conversiones:
    """Conversiones realizadas con Python estándar y procedimientos explicativos."""

    # Digitos utilizables para el procedimiento y para q cuente en hexadecimal tmb
    DIGITOS = "0123456789ABCDEF"

    @staticmethod
    def _validar_entero(numero):
        texto = str(numero).strip()
        if not texto:
            raise ValueError("El número no puede estar vacío.")
        try:
            return int(texto)
        except ValueError:
            raise ValueError("Ingrese un número entero válido.")

    @staticmethod
    def _decimal_a_base(numero, base):
        numero = Conversiones._validar_entero(numero)
        if numero == 0:
            return "0", "0 / {} = 0, residuo 0".format(base)

        signo = ""
        if numero < 0:
            signo = "-"
            numero = abs(numero)

        digitos = []
        pasos = []
        original = numero

        while numero > 0:
            cociente = numero // base
            residuo = numero % base
            digitos.append(Conversiones.DIGITOS[residuo])
            pasos.append(f"{numero} / {base} = {cociente}, residuo {Conversiones.DIGITOS[residuo]}")
            numero = cociente

        resultado = signo + "".join(reversed(digitos))
        procedimiento = (
            f"Conversión de {('-' if signo else '')}{original} a base {base}\n\n"
            "Se divide sucesivamente entre la base y se leen los residuos "
            "desde el último hasta el primero.\n\n"
            + "\n".join(pasos)
            + "\n\nResultado: " + resultado
        )
        return resultado, procedimiento

    @staticmethod
    def _base_a_decimal(numero, base):
        texto = str(numero).strip().upper()
        if not texto:
            raise ValueError("El número no puede estar vacío.")

        signo = 1
        if texto.startswith("-"):
            signo = -1
            texto = texto[1:]

        if not texto:
            raise ValueError("Ingrese un número válido.")

        valores = []
        for digito in texto:
            if digito not in Conversiones.DIGITOS[:base]:
                raise ValueError(f"El número {numero} no es válido en base {base}.")
            valores.append(Conversiones.DIGITOS.index(digito))

        terminos = []
        total = 0
        longitud = len(valores)
        for posicion, valor in enumerate(valores):
            exponente = longitud - posicion - 1
            termino = valor * (base ** exponente)
            total += termino
            terminos.append(f"{valor} × {base}^{exponente} = {termino}")

        total *= signo
        procedimiento = (
            f"Conversión de {('-' if signo < 0 else '')}{texto} de base {base} a decimal\n\n"
            "Se utiliza la combinación lineal de cada dígito por la base elevada "
            "a su posición, comenzando desde el exponente 0 a la derecha.\n\n"
            + "\n".join(terminos)
            + f"\n\nSuma de términos = {total}"
        )
        return str(total), procedimiento

    @staticmethod
    def decimal_a_binario(numero):
        return Conversiones._decimal_a_base(numero, 2)[0]

    @staticmethod
    def binario_a_decimal(binario):
        return int(Conversiones._base_a_decimal(binario, 2)[0])

    @staticmethod
    def decimal_a_octal(numero):
        return Conversiones._decimal_a_base(numero, 8)[0]

    @staticmethod
    def octal_a_decimal(octal):
        return int(Conversiones._base_a_decimal(octal, 8)[0])

    @staticmethod
    def decimal_a_hexadecimal(numero):
        return Conversiones._decimal_a_base(numero, 16)[0]

    @staticmethod
    def hexadecimal_a_decimal(hexadecimal):
        return int(Conversiones._base_a_decimal(hexadecimal, 16)[0])

    @staticmethod
    def decimal_a_binario_con_procedimiento(numero):
        return Conversiones._decimal_a_base(numero, 2)

    @staticmethod
    def binario_a_decimal_con_procedimiento(numero):
        return Conversiones._base_a_decimal(numero, 2)

    @staticmethod
    def decimal_a_octal_con_procedimiento(numero):
        return Conversiones._decimal_a_base(numero, 8)

    @staticmethod
    def octal_a_decimal_con_procedimiento(numero):
        return Conversiones._base_a_decimal(numero, 8)

    @staticmethod
    def decimal_a_hexadecimal_con_procedimiento(numero):
        return Conversiones._decimal_a_base(numero, 16)

    @staticmethod
    def hexadecimal_a_decimal_con_procedimiento(numero):
        return Conversiones._base_a_decimal(numero, 16)
    @staticmethod
    def arabigo_a_romano(numero):
        """Convierte un entero arábigo de 1 a 3999 a numeración romana."""
        n = Conversiones._validar_entero(numero)
        if not 1 <= n <= 3999:
            raise ValueError("Para la conversión tradicional, el número arábigo debe estar entre 1 y 3999.")

        valores = [
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
        ]

        restante = n
        partes = []
        pasos = [f"Conversión de {n} (arábigo) a romano", "",
                 "Se utilizan los valores romanos de mayor a menor.", ""]

        for valor, simbolo in valores:
            cantidad = restante // valor
            if cantidad:
                for _ in range(cantidad):
                    partes.append(simbolo)
                    restante -= valor
                    pasos.append(f"{valor} → {simbolo}; restante = {restante}")

        resultado = "".join(partes)
        pasos.append(f"\nResultado: {resultado}")
        return resultado, "\n".join(pasos)

    @staticmethod
    def romano_a_arabigo(romano):
        """Convierte una numeración romana canónica de 1 a 3999 a entero arábigo."""
        texto = str(romano).strip().upper()
        if not texto:
            raise ValueError("El número romano no puede estar vacío.")

        valores = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        if any(c not in valores for c in texto):
            raise ValueError("El número romano contiene símbolos no válidos.")

        total = 0
        pasos = [f"Conversión de {texto} (romano) a arábigo", "",
                 "Se recorren los símbolos de izquierda a derecha.",
                 "Si un símbolo menor aparece antes de uno mayor, se resta; de lo contrario, se suma.", ""]

        i = 0
        while i < len(texto):
            actual = valores[texto[i]]
            if i + 1 < len(texto) and actual < valores[texto[i + 1]]:
                siguiente = valores[texto[i + 1]]
                total += siguiente - actual
                pasos.append(f"{texto[i]}({actual}) antes de {texto[i+1]}({siguiente}) → {siguiente} - {actual} = {siguiente - actual}; acumulado = {total}")
                i += 2
            else:
                total += actual
                pasos.append(f"{texto[i]}({actual}) → +{actual}; acumulado = {total}")
                i += 1

        # Validación canónica: evita aceptar formas como IIII, IC o VX.
        canonico, _ = Conversiones.arabigo_a_romano(total)
        if canonico != texto:
            raise ValueError(f"Número romano no válido en notación tradicional: {texto}.")

        pasos.append(f"\nResultado: {total}")
        return str(total), "\n".join(pasos)

