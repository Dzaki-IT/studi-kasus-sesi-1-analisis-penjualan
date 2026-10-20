from pathlib import Path
import argparse
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "penjualan.csv"
DEFAULT_OUTPUT = ROOT / "outputs"

REQUIRED_COLUMNS = {
    "tanggal", "produk", "kategori", "jumlah_terjual",
    "harga_satuan", "biaya_satuan", "diskon", "kanal"
}

def load_data(path=DEFAULT_DATA):
    """Membaca dan memvalidasi data transaksi."""
    data = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Kolom wajib tidak ditemukan: {', '.join(sorted(missing))}")

    data["tanggal"] = pd.to_datetime(data["tanggal"], errors="coerce")
    numeric_cols = ["jumlah_terjual", "harga_satuan", "biaya_satuan", "diskon"]
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    if data[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("Data memiliki nilai kosong atau format yang tidak valid.")
    if (data["jumlah_terjual"] <= 0).any():
        raise ValueError("jumlah_terjual harus lebih besar dari 0.")
    if (data["harga_satuan"] < 0).any() or (data["biaya_satuan"] < 0).any():
        raise ValueError("Harga dan biaya tidak boleh negatif.")
    if not data["diskon"].between(0, 1).all():
        raise ValueError("diskon harus berada di antara 0 dan 1.")

    # Menghitung nilai transaksi setelah diskon, biaya, dan keuntungan.
    data["omzet"] = data["jumlah_terjual"] * data["harga_satuan"] * (1 - data["diskon"])
    data["total_biaya"] = data["jumlah_terjual"] * data["biaya_satuan"]
    data["keuntungan"] = data["omzet"] - data["total_biaya"]
    data["bulan"] = data["tanggal"].dt.to_period("M").astype(str)
    return data

def analyze(data, output_dir=DEFAULT_OUTPUT):
    """Membuat tabel ringkasan, grafik, dan catatan temuan."""
    output_dir = Path(output_dir)
    chart_dir = output_dir / "charts"
    chart_dir.mkdir(parents=True, exist_ok=True)

    ringkasan = pd.DataFrame([{
        "jumlah_transaksi": int(len(data)),
        "total_unit_terjual": int(data["jumlah_terjual"].sum()),
        "total_omzet": round(data["omzet"].sum(), 2),
        "total_biaya": round(data["total_biaya"].sum(), 2),
        "total_keuntungan": round(data["keuntungan"].sum(), 2),
        "margin_keuntungan_persen": round(data["keuntungan"].sum() / data["omzet"].sum() * 100, 2)
    }])
    ringkasan.to_csv(output_dir / "ringkasan_umum.csv", index=False)

    per_bulan = data.groupby("bulan", as_index=False).agg(
        omzet=("omzet", "sum"),
        keuntungan=("keuntungan", "sum"),
        unit_terjual=("jumlah_terjual", "sum")
    )
    per_bulan.to_csv(output_dir / "ringkasan_bulanan.csv", index=False)

    per_produk = data.groupby("produk", as_index=False).agg(
        unit_terjual=("jumlah_terjual", "sum"),
        omzet=("omzet", "sum"),
        keuntungan=("keuntungan", "sum"),
        rata_diskon=("diskon", "mean")
    ).sort_values("keuntungan", ascending=False)
    per_produk["rata_diskon_persen"] = (per_produk.pop("rata_diskon") * 100).round(2)
    per_produk.to_csv(output_dir / "ringkasan_produk.csv", index=False)

    # Grafik 1: omzet per bulan
    plt.figure(figsize=(8, 5))
    plt.plot(per_bulan["bulan"], per_bulan["omzet"], marker="o")
    plt.title("Omzet per Bulan")
    plt.xlabel("Bulan")
    plt.ylabel("Omzet (rupiah)")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(chart_dir / "omzet_bulanan.png", dpi=150)
    plt.close()

    # Grafik 2: keuntungan per produk
    plot_data = per_produk.sort_values("keuntungan")
    plt.figure(figsize=(8, 5))
    plt.barh(plot_data["produk"], plot_data["keuntungan"])
    plt.title("Keuntungan per Produk")
    plt.xlabel("Keuntungan (rupiah)")
    plt.ylabel("Produk")
    plt.tight_layout()
    plt.savefig(chart_dir / "keuntungan_produk.png", dpi=150)
    plt.close()

    # Grafik 3: rata-rata diskon dan keuntungan per produk untuk membantu eksplorasi.
    plt.figure(figsize=(8, 5))
    plt.scatter(per_produk["rata_diskon_persen"], per_produk["keuntungan"])
    for _, row in per_produk.iterrows():
        plt.annotate(row["produk"], (row["rata_diskon_persen"], row["keuntungan"]),
                     xytext=(4, 4), textcoords="offset points", fontsize=8)
    plt.title("Rata-rata Diskon vs Keuntungan Produk")
    plt.xlabel("Rata-rata diskon (%)")
    plt.ylabel("Total keuntungan (rupiah)")
    plt.tight_layout()
    plt.savefig(chart_dir / "diskon_vs_keuntungan.png", dpi=150)
    plt.close()

    best = per_produk.iloc[0]
    lowest = per_produk.iloc[-1]
    peak = per_bulan.loc[per_bulan["omzet"].idxmax()]
    low = per_bulan.loc[per_bulan["omzet"].idxmin()]
    report = f"""# Catatan Hasil Analisis

> Dataset ini adalah **data sintetis untuk pembelajaran**, bukan catatan transaksi toko sungguhan.

- Jumlah transaksi: **{int(ringkasan.loc[0, 'jumlah_transaksi'])}**
- Total unit terjual: **{int(ringkasan.loc[0, 'total_unit_terjual'])}**
- Total omzet setelah diskon: **Rp{ringkasan.loc[0, 'total_omzet']:,.0f}**
- Total keuntungan perkiraan: **Rp{ringkasan.loc[0, 'total_keuntungan']:,.0f}**
- Margin keuntungan keseluruhan: **{ringkasan.loc[0, 'margin_keuntungan_persen']:.2f}%**

## Temuan deskriptif
- Bulan dengan omzet tertinggi pada data: **{peak['bulan']}** (Rp{peak['omzet']:,.0f}).
- Bulan dengan omzet terendah pada data: **{low['bulan']}** (Rp{low['omzet']:,.0f}).
- Produk dengan total keuntungan tertinggi: **{best['produk']}** (Rp{best['keuntungan']:,.0f}).
- Produk dengan total keuntungan terendah: **{lowest['produk']}** (Rp{lowest['keuntungan']:,.0f}).

## Pertanyaan diagnostik untuk ditindaklanjuti
1. Apakah diskon yang lebih besar berkaitan dengan keuntungan yang lebih rendah pada produk yang sama?
2. Apakah perbedaan kanal penjualan (Toko/Online) berhubungan dengan jumlah unit yang terjual?
3. Apakah produk dengan keuntungan terendah perlu ditinjau dari harga, biaya, atau strategi promosi?

## Batasan
Analisis ini mendeskripsikan pola dalam dataset contoh. Pola tersebut **tidak membuktikan sebab-akibat**. Sebelum keputusan bisnis nyata dibuat, data harus diverifikasi dan faktor lain seperti biaya operasional, retur, stok, serta biaya pengiriman perlu diperhitungkan.
"""
    (output_dir / "temuan.md").write_text(report, encoding="utf-8")
    return ringkasan, per_bulan, per_produk

def main():
    parser = argparse.ArgumentParser(description="Analisis data penjualan toko fiktif.")
    parser.add_argument("--data", default=str(DEFAULT_DATA), help="Lokasi file CSV transaksi.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Folder untuk menyimpan hasil.")
    args = parser.parse_args()
    data = load_data(args.data)
    ringkasan, _, per_produk = analyze(data, args.output)
    print("Analisis selesai.")
    print(ringkasan.to_string(index=False))
    print("\nPeringkat keuntungan per produk:")
    print(per_produk[["produk", "unit_terjual", "omzet", "keuntungan"]].to_string(index=False))
    print(f"\nHasil tersimpan di: {Path(args.output).resolve()}")

if __name__ == "__main__":
    main()
