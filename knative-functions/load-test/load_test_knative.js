import http from 'k6/http';
import { sleep, check } from 'k6';

// Read image as binary before test starts
const imageData = open(__ENV.IMAGE_PATH, 'b'); // Open file as binary

export let options = {
  stages: [
    { duration: '30s', target: 10 },  // Ramp up to 10 users
    { duration: '1m', target: 50 },   // Increase to 50 users
    { duration: '30s', target: 0 },   // Scale down
  ],
};

export default function () {
  let params = {
    headers: {
      'Host': 'ingest-image.default.4.231.100.102.xip.io',
      'Content-Type': 'image/jpeg',
    },
  };

  let res = http.post('http://4.231.100.102:31750/start-process', imageData, params);

  check(res, {
    'is status 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
