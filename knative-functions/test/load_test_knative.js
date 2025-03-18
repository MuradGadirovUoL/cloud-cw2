import http from 'k6/http';
import { sleep, check } from 'k6';
import { Trend, Counter, Rate } from 'k6/metrics';

const coldStartDuration = new Trend('cold_start_duration');
const warmStartDuration = new Trend('warm_start_duration');
const coldStarts = new Counter('cold_start_count');
const successRate = new Rate('success_rate');

const imageData = open(__ENV.IMAGE_PATH, 'b');
const headers = {
  'Host': 'ingest-image.default.4.231.100.102.xip.io',
  'Content-Type': 'image/jpeg'
};

const COLD_START_THRESHOLD = 3000; // ms
const WARM_START_THRESHOLD = 500; // ms

export let options = {
  scenarios: {
    cold_start: {
      executor: 'per-vu-iterations',
      vus: 1,
      iterations: 1,
      exec: 'coldStart',
      startTime: '0s'
    },
    warm_load: {
      executor: 'ramping-arrival-rate',
      startRate: 10,
      timeUnit: '1s',
      preAllocatedVUs: 50,
      stages: [
        { target: 50, duration: '30s' }, // Ramp-up
        { target: 50, duration: '1m' },  // Sustain
        { target: 0, duration: '30s' }   // Cool-down
      ],
      exec: 'warmLoad',
      startTime: '15s' // Allow time for cold start
    }
  }
};

export function coldStart() {
  const res = http.post(
    'http://4.231.100.102:31750/start-process',
    imageData,
    { headers }
  );

  // Record cold start metrics
  coldStartDuration.add(res.timings.duration);
  coldStarts.add(1);
  successRate.add(res.status === 200);

  check(res, {
    'Cold start succeeded': (r) => r.status === 200,
    'Cold start duration < 5s': (r) => r.timings.duration < 5000
  });
}

export function warmLoad() {
  const res = http.post(
    'http://4.231.100.102:31750/start-process',
    imageData,
    { headers }
  );

  // Classify as cold/warm based on duration
  if (res.timings.duration > COLD_START_THRESHOLD) {
    coldStarts.add(1);
    coldStartDuration.add(res.timings.duration);
  } else {
    warmStartDuration.add(res.timings.duration);
  }

  successRate.add(res.status === 200);

  check(res, {
    'Warm start succeeded': (r) => r.status === 200,
    'Warm start duration < 500ms': (r) => r.timings.duration < WARM_START_THRESHOLD
  });

  sleep(0.5); // Control request rate
}