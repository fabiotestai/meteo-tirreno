import unittest

from meteo.fattibilita import omirl_series

# Ritaglio di un grafico "Vento" di OMIRL (charts/GEPOA/Vento), due serie
XML = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><dataChart>
<dataSeries><axisId>0</axisId>
<data><item>1791717000000</item><item>12.6</item></data>
<data><item>1791717600000</item><item>10.8</item></data>
<name>Velocit\xc3\xa0 del Vento</name><type>line</type></dataSeries>
<dataSeries><axisId>0</axisId>
<data><item>1791720000000</item><item>225.0</item></data>
<data><item>1791723600000</item><item></item></data>
<name>Wind Direction</name></dataSeries>
</dataChart>"""


class TestOmirl(unittest.TestCase):
    def test_series(self):
        s = omirl_series(XML)
        self.assertEqual(s["Velocità del Vento"], [(1791717000, 12.6), (1791717600, 10.8)])
        self.assertEqual(s["Wind Direction"], [(1791720000, 225.0)])  # i valori vuoti si scartano


if __name__ == "__main__":
    unittest.main()
