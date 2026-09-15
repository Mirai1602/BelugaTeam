#Aqui van todas las funciones que ayudan a validar entradas y transformar datos
#Modelado de matrices y operaciones
class MatrizModel:
    @staticmethod
    def sumar(matrices):
        f_base, c_base = len(matrices[0]), len(matrices[0][0])
        res = [fila[:] for fila in matrices[0]]
        for m in matrices[1:]:
            for i in range(f_base):
                for j in range(c_base):
                    res[i][j] += m[i][j]
        return res
#Restar
    @staticmethod
    def restar(matrices):
        f_base, c_base = len(matrices[0]), len(matrices[0][0])
        res = [fila[:] for fila in matrices[0]]
        for m in matrices[1:]:
            for i in range(f_base):
                for j in range(c_base):
                    res[i][j] -= m[i][j]
        return res
#Multiplicar
    @staticmethod
    def multiplicar(matrices):
        res = matrices[0]
        for m in matrices[1:]:
            f_A, c_A = len(res), len(res[0])
            f_B, c_B = len(m), len(m[0])
            sub_res = []
            for i in range(f_A):
                fila = []
                for j in range(c_B):
                    suma = 0
                    for k in range(c_A):
                        suma += res[i][k] * m[k][j]
                    fila.append(suma)
                sub_res.append(fila)
            res = sub_res
        return res


#Formaro de salida 
    @staticmethod
    def formato_matriz_str(matriz, titulo=""):
        texto = f"--- {titulo} ---\n" if titulo else ""
        for fila in matriz:
            coefs = "  ".join([f"{val:8.2f}" for val in fila[:-1]])
            b_val = f"{fila[-1]:8.2f}"
            texto += f"[ {coefs}  | {b_val} ]\n"
        return texto + "\n"

#convertir de Binario a Decimal
    @staticmethod
    def binario_a_decimal():
        numEnBinario = []
        print("ingrese el nuemero binario que desea convertir a decimal")
        binario = input()
        for bit in binario:  #Convierte de string a int y lo guarda en la lista 
            numEnBinario.append(int(bit))
        decimal = 0
        for i, bit in enumerate(reversed(numEnBinario)):
            decimal += bit * (2 ** i)
        return decimal