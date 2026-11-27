"""BakimTakip - bilerek "eski usul" yazilmis tek parca (monolit) uygulama."""
import os

import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request

# ESKI ALISKANLIK: parola kodun icinde duruyor. Ortam degiskeni verilirse
# o kullanilir; yeni ortamda parolayi koddan bu sayede cikaracagiz.
DB = dict(
    host=os.environ.get("DB_HOST", "localhost"),
    port=int(os.environ.get("DB_PORT", "5432")),
    dbname=os.environ.get("DB_NAME", "bakim"),
    user=os.environ.get("DB_USER", "bakim_app"),
    password=os.environ.get("DB_PASSWORD", "Bakim123"),
)
SURUM = os.environ.get("SURUM", "eski")

app = Flask(__name__)


def sorgu(sql, args=()):
    """Her istekte yeni baglanti acar (eski usul; PgBouncer ile uyumlu)."""
    conn = psycopg2.connect(connect_timeout=5, **DB)
    try:
        with conn, conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        ) as cur:
            cur.execute(sql, args)
            return cur.fetchall() if cur.description else []
    finally:
        conn.close()


@app.after_request
def surum_basligi(yanit):
    yanit.headers["X-Surum"] = SURUM
    return yanit


@app.get("/saglik")
def saglik():
    sorgu("SELECT 1")
    return jsonify(durum="ok", surum=SURUM)


@app.get("/araclar")
def araclar():
    return jsonify(sorgu("SELECT id, plaka, tip, km FROM arac ORDER BY id"))


@app.post("/is-emri")
def is_emri_ac():
    veri = request.get_json(force=True)
    satir = sorgu(
        "INSERT INTO is_emri (arac_id, aciklama) VALUES (%s, %s) "
        "RETURNING id, arac_id, aciklama, durum, olusturma",
        (veri["arac_id"], veri["aciklama"]),
    )
    return jsonify(satir[0]), 201


@app.get("/is-emri/<int:kimlik>")
def is_emri_getir(kimlik):
    satir = sorgu("SELECT * FROM is_emri WHERE id = %s", (kimlik,))
    if not satir:
        return jsonify(hata="bulunamadi"), 404
    return jsonify(satir[0])


@app.post("/stok/hareket")
def stok_hareket():
    veri = request.get_json(force=True)
    satir = sorgu(
        "WITH h AS (INSERT INTO stok_hareket (parca_id, adet) "
        "           VALUES (%s, %s) RETURNING id, parca_id, adet) "
        "UPDATE parca p SET stok_adet = p.stok_adet + h.adet "
        "FROM h WHERE p.id = h.parca_id "
        "RETURNING h.id AS hareket_id, p.id AS parca_id, p.stok_adet",
        (veri["parca_id"], veri["adet"]),
    )
    return jsonify(satir[0]), 201


@app.get("/rapor/ozet")
def rapor_ozet():
    return jsonify(
        sorgu(
            "SELECT a.tip, count(i.id) AS is_emri_sayisi, "
            "       count(i.id) FILTER (WHERE i.durum = 'acik') AS acik "
            "FROM arac a LEFT JOIN is_emri i ON i.arac_id = a.id "
            "GROUP BY a.tip ORDER BY a.tip"
        )
    )


if __name__ == "__main__":
    # ESKI ALISKANLIK: gelistirme sunucusuyla canli ortamda calismak.
    app.run(host="0.0.0.0", port=5000)