INSERT INTO arac (plaka, tip, km)
SELECT '44 MT ' || lpad(n::text, 3, '0'),
       CASE WHEN n % 4 = 0 THEN 'trambus' ELSE 'otobus' END,
       50000 + n * 1375
FROM generate_series(1, 20) AS n;
 
INSERT INTO parca (ad, stok_adet)
SELECT 'Parca-' || n, 1000 FROM generate_series(1, 10) AS n;