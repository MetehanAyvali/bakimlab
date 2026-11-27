CREATE TABLE arac (
    id    serial PRIMARY KEY,
    plaka text UNIQUE NOT NULL,
    tip   text NOT NULL,
    km    integer NOT NULL DEFAULT 0
);
CREATE TABLE parca (
    id        serial PRIMARY KEY,
    ad        text NOT NULL,
    stok_adet integer NOT NULL DEFAULT 0
);
CREATE TABLE is_emri (
    id         serial PRIMARY KEY,
    arac_id    integer NOT NULL REFERENCES arac(id),
    aciklama   text NOT NULL,
    durum      text NOT NULL DEFAULT 'acik',
    olusturma  timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE stok_hareket (
    id       serial PRIMARY KEY,
    parca_id integer NOT NULL REFERENCES parca(id),
    adet     integer NOT NULL,
    tarih    timestamptz NOT NULL DEFAULT now()
);