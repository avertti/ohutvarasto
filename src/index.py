from varasto import Varasto


def luo_varastot():
    mehua = Varasto(100.0)
    olutta = Varasto(100.0, 20.2)
    return mehua, olutta


def testaa_getterit(olut_varasto):
    print("Olut getterit:")
    print(f"saldo = {olut_varasto.saldo}")
    print(f"tilavuus = {olut_varasto.tilavuus}")
    print(f"paljonko_mahtuu = {olut_varasto.paljonko_mahtuu()}")


def testaa_setterit(mehu_varasto):
    print("Mehu setterit:")
    print("Lisätään 50.7")
    mehu_varasto.lisaa_varastoon(50.7)
    print(f"Mehuvarasto: {mehu_varasto}")
    print("Otetaan 3.14")
    mehu_varasto.ota_varastosta(3.14)
    print(f"Mehuvarasto: {mehu_varasto}")


def testaa_virhetilanteita():
    print("Virhetilanteita:")
    print("Varasto(-100.0);")
    huono = Varasto(-100.0)
    print(huono)

    print("Varasto(100.0, -50.7)")
    huono = Varasto(100.0, -50.7)
    print(huono)


def testaa_ylitaytto(olut_varasto):
    print(f"Olutvarasto: {olut_varasto}")
    print("olutta.lisaa_varastoon(1000.0)")
    olut_varasto.lisaa_varastoon(1000.0)
    print(f"Olutvarasto: {olut_varasto}")

def testaa_negatiivinen_lisays(mehu_varasto):
    print(f"Mehuvarasto: {mehu_varasto}")
    print("mehua.lisaa_varastoon(-666.0)")
    mehu_varasto.lisaa_varastoon(-666.0)
    print(f"Mehuvarasto: {mehu_varasto}")

def testaa_yliotto_olut(olut_varasto):
    print(f"Olutvarasto: {olut_varasto}")
    print("olutta.ota_varastosta(1000.0)")
    saatiin = olut_varasto.ota_varastosta(1000.0)
    print(f"saatiin {saatiin}")
    print(f"Olutvarasto: {olut_varasto}")

def testaa_negatiivinen_otto(mehu_varasto):
    print(f"Mehuvarasto: {mehu_varasto}")
    print("mehua.otaVarastosta(-32.9)")
    saatiin = mehu_varasto.ota_varastosta(-32.9)
    print(f"saatiin {saatiin}")
    print(f"Mehuvarasto: {mehu_varasto}")

def tulosta_alkutilanne(mehu, olut):
    print("Luonnin jälkeen:")
    print(f"Mehuvarasto: {mehu}")
    print(f"Olutvarasto: {olut}")

def main():
    mehu, olut = luo_varastot()
    tulosta_alkutilanne(mehu, olut)#fffffffffffffffffffffffffffffffffffffffffffffffffffffff
    testaa_getterit(olut)
    testaa_setterit(mehu)
    testaa_virhetilanteita()
    testaa_ylitaytto(olut)
    testaa_negatiivinen_lisays(mehu)
    testaa_yliotto_olut(olut)
    testaa_negatiivinen_otto(mehu)

if __name__ == "__main__":
    main()
