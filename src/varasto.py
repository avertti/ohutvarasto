class Varasto:
    def __init__(self, tilavuus, alku_saldo = 0):
        # Alustetaan attribuutit
        self.tilavuus = 0.0
        self.saldo = 0.0
        # Asetetaan arvot validoinnin kautta
        self._alusta_tilavuus(tilavuus)
        self._alusta_saldo(alku_saldo)

    def _alusta_tilavuus(self, tilavuus):
        if tilavuus > 0.0:
            self.tilavuus = tilavuus

    def _alusta_saldo(self, alku_saldo):
        if alku_saldo < 0.0:
            return  # saldo on jo alustettu nollaksi
        if alku_saldo <= self.tilavuus:
            # mahtuu
            self.saldo = alku_saldo
        else:
            # täyteen ja ylimäärä hukkaan!
            self.saldo = self.tilavuus

    # huom: ominaisuus voidaan myös laskea
    # Ei tarvita erillistä kenttää viela_tilaa tms.
    def paljonko_mahtuu(self):
        return self.tilavuus - self.saldo

    def lisaa_varastoon(self, maara):
        if maara < 0:
            return
        if maara <= self.paljonko_mahtuu():
            self.saldo = self.saldo + maara
        else:
            self.saldo = self.tilavuus

    def ota_varastosta(self, maara):
        if maara < 0:
            return 0.0
        if maara > self.saldo:
            kaikki_mita_voidaan = self.saldo
            self.saldo = 0.0

            return kaikki_mita_voidaan

        self.saldo = self.saldo - maara

        return maara

    def __str__(self):
        return f"saldo = {self.saldo}, vielä tilaa {self.paljonko_mahtuu()}"
