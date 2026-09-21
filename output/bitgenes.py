import os
from sys import getsizeof

class CompressedGene:
    def __init__(self, gene, gened):
        if gene:
            self.compress(gene)
        else:
            self.bit_string = int.from_bytes(gened, byteorder='big')

    def compress(self, gene):
        self.bit_string = 0b01
        for nucleotide in gene:
            self.bit_string <<= 2
            if nucleotide == "A": 
                self.bit_string |= 0b00
            elif nucleotide == "C": 
                self.bit_string |= 0b01
            elif nucleotide == "G": 
                self.bit_string |= 0b10
            elif nucleotide == "T": 
                self.bit_string |= 0b11
            else: raise ValueError("Invalid Nucleotide")

    def decompress(self):
        gene = ""
        for i in range(0, self.bit_string.bit_length() - 1, 2):
            bits = self.bit_string >> i & 0b11
            if bits == 0b00: 
                gene += "A"
            elif bits == 0b01: 
                gene += "C"
            elif bits == 0b10: 
                gene += "G"
            elif bits == 0b11: 
                gene += "T"
        return gene[::-1]

    def save_to_file(self, filename, is_binary):
        if is_binary:
            num_bytes = (self.bit_string.bit_length() + 7) // 8
            bytes_data = self.bit_string.to_bytes(num_bytes, byteorder='big')
            with open(filename, "wb") as arquivo:
                arquivo.write(bytes_data)
        else:
            with open(filename, "w") as arquivo:
                arquivo.write(self.decompress())

os.makedirs("output", exist_ok=True)

with open("output/genes.txt", "r") as arquivo:
    original = arquivo.read()

compressed = CompressedGene(original, None)
compressed.save_to_file("output/genes_comprimidos.bin", is_binary=True)

with open("output/genes_comprimidos.bin", "rb") as arquivo:
    genes_comprimidos = arquivo.read()

descompressed = CompressedGene(None, genes_comprimidos)
descompressed.save_to_file("output/genes_descomprimidos.txt", is_binary=False)

with open("output/genes_descomprimidos.txt", "r") as arquivo:
    modificado = arquivo.read()

print("Arquivo de texto 'output/genes_descomprimidos.txt' gerado para comparacao manual!\n")
print(f"Original: {os.path.getsize('output/genes.txt')} bytes no disco, {getsizeof(original)} bytes na RAM")
print(f"Comprimido (bits): {os.path.getsize('output/genes_comprimidos.bin')} bytes no disco, {getsizeof(compressed.bit_string)} bytes na RAM")
print(f"Descomprimido: {os.path.getsize('output/genes_descomprimidos.txt')} bytes no disco, {getsizeof(modificado)} bytes na RAM")

x = os.path.getsize('output/genes.txt')
y = os.path.getsize('output/genes_comprimidos.bin')
z = os.path.getsize('output/genes_descomprimidos.txt')

print(f"Porcentagem de compressão: {100 - (y / x * 100):.2f}%")
