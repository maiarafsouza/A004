# Princípio da responsabilidade única
# Princípio aberto/fechado -> classe deve ser aberta para extensão, fechada para modificação

import datetime
import math
from typing import List

class Pessoa:
    def __init__(self, 
                 nome: str, 
                 sobrenome: str, 
                 data_de_nascimento: datetime.date):
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_de_nascimento = data_de_nascimento
    
    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)
    
    def __str__(self) -> str:
        return f'{self.nome} {self.sobrenome} tem {self.idade} anos'
    
class Curriculo(Pessoa):
    def __init__(self, 
                 pessoa: Pessoa, 
                 experiencias: List[str]):
        self.experiencias = experiencias
        self.pessoa = pessoa

    @property
    def quantidade_de_experiencias(self) -> int:
        return len(self.experiencias)
    
    @property
    def empresa_atual(self) -> str:
        return self.experiencias[-1]
    
    def adiciona_experiência(self, experiencia: str) -> None:
        self.experiencias.append(experiencia)
    
    def __str__(self):
        return f'''
        {self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos
        trabalhou em {self.quantidade_de_experiencias} empresas
        atualmente trabalha na empresa {self.empresa_atual}'''

p1 = Pessoa('José', 'Cuervo', datetime.date(1947, 4, 17))

c1 = Curriculo(p1, ['Nubank', 'Boticario', 'Santander'])

print(p1)
print(c1)