class Clovek():
    jmeno:str
    vek:int
    def __init__(self, jno:str, vek:int) -> None:
        self.jmeno = jno
        self.vek = vek

    def ma_narozeniny(self)->None:
        self.vek += 1
        print(f"Vsechno nejlepši, {self.jmeno} má {self.vek} let!")

class ClovekMajiciPohlavi(Clovek):
    pohlavi:str
    def __init__(self, jmeno:str, vek:int, pohlavi:str="Neuvedeno"):
        self.pohlavi = pohlavi
        super().__init__(jmeno, vek)

    def ma_narozeniny(self)->None:
        self.vek += 100
        print(f"Vsechno nejlepši, super kámoš {self.jmeno} má {self.vek} let!")

def popis_cloveka(clovek:Clovek):
    print(clovek.jmeno,"je starý přesně", clovek.vek, "let")
    
josef = ClovekMajiciPohlavi("Josef", 25)
josef.ma_narozeniny()
print(josef.pohlavi)

karel_clovek = Clovek("Karel", 77)

popis_cloveka(karel_clovek)

karel_clovek.ma_narozeniny()
karel_clovek.ma_narozeniny()


popis_cloveka(karel_clovek)
popis_cloveka(josef)
