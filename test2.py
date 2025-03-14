from binascii import hexlify
import test
from hashlib import sha256
print(test.a_man)

BLBY_THRESHOLD =2

def scitac(x: int,y: int) -> int:
    return x+2*y

def blby_scitac(prvni:int, druhy:int)->int|str:
    if prvni > BLBY_THRESHOLD:
        return prvni + druhy
    else:
        return f"PRvni je mensi než {BLBY_THRESHOLD}"

vysledek = blby_scitac(3,8)
if not isinstance(vysledek, str): # vysledek neni typu int
    print("VYSLEDEKz fnkce:", vysledek)
    print("VYsledek je upkne k nicemu")
    

def tiskac(cislo: int) ->None:
    print(cislo)

prvni = scitac(1,2)
tiskac(prvni)

sha_context = sha256()
sha_context.update("Jan".encode("utf-8"))
vysledny_hash:bytes = sha_context.digest()
vysledny_hash_hex:str = hexlify(vysledny_hash).decode()
print(vysledny_hash_hex)
