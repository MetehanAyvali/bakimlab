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