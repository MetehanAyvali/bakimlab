import http from 'k6/http';
import { check } from 'k6';

const BASE = __ENV.BASE_URL || 'http://localhost';
const JSON_BASLIK = { headers: { 'Content-Type': 'application/json' } };

export const options = {
  scenarios: {
    sabit_yuk: {
      executor: 'constant-arrival-rate',
      rate: Number(__ENV.HIZ || 20),      // saniyede istek
      timeUnit: '1s',
      duration: __ENV.SURE || '5m',
      preAllocatedVUs: 20,
      maxVUs: 200,
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.001'],      // hata orani %0,1'in altinda
    http_req_duration: ['p(95)<500'],     // 95. yuzdelik 500 ms'nin altinda
  },
};

export default function () {
  const zar = Math.random();
  let yanit;
  if (zar < 0.50) {
    yanit = http.get(`${BASE}/araclar`);
  } else if (zar < 0.80) {
    const govde = JSON.stringify({
      arac_id: 1 + Math.floor(Math.random() * 20),
      aciklama: 'yuk testi is emri',
    });
    yanit = http.post(`${BASE}/is-emri`, govde, JSON_BASLIK);
  } else if (zar < 0.95) {
    const govde = JSON.stringify({
      parca_id: 1 + Math.floor(Math.random() * 10),
      adet: -1,
    });
    yanit = http.post(`${BASE}/stok/hareket`, govde, JSON_BASLIK);
  } else {
    yanit = http.get(`${BASE}/rapor/ozet`);
  }
  check(yanit, { 'durum 2xx': (r) => r.status >= 200 && r.status < 300 });
}