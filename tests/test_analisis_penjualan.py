import sys
import unittest
from pathlib import Path
import tempfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analisis_penjualan import load_data, analyze

class TestAnalisisPenjualan(unittest.TestCase):
    def test_dataset_valid_dan_kolom_hasil_ada(self):
        data = load_data(ROOT / "data" / "penjualan.csv")
        self.assertGreater(len(data), 0)
        for col in ["omzet", "total_biaya", "keuntungan", "bulan"]:
            self.assertIn(col, data.columns)

    def test_omzet_menggunakan_diskon(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "contoh.csv"
            pd.DataFrame([{
                "tanggal":"2026-01-01", "produk":"A", "kategori":"X",
                "jumlah_terjual":2, "harga_satuan":100, "biaya_satuan":40,
                "diskon":0.1, "kanal":"Toko"
            }]).to_csv(p, index=False)
            data = load_data(p)
            self.assertAlmostEqual(data.loc[0, "omzet"], 180)
            self.assertAlmostEqual(data.loc[0, "keuntungan"], 100)

    def test_diskon_di_luar_rentang_ditolak(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "buruk.csv"
            pd.DataFrame([{
                "tanggal":"2026-01-01", "produk":"A", "kategori":"X",
                "jumlah_terjual":2, "harga_satuan":100, "biaya_satuan":40,
                "diskon":1.2, "kanal":"Toko"
            }]).to_csv(p, index=False)
            with self.assertRaises(ValueError):
                load_data(p)

    def test_analisis_menghasilkan_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = load_data(ROOT / "data" / "penjualan.csv")
            analyze(data, tmp)
            self.assertTrue((Path(tmp) / "ringkasan_umum.csv").exists())
            self.assertTrue((Path(tmp) / "temuan.md").exists())
            self.assertTrue((Path(tmp) / "charts" / "omzet_bulanan.png").exists())

if __name__ == "__main__":
    unittest.main()
