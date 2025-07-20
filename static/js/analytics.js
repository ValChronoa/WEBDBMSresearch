/* static/js/analytics.js - simple fetch wrappers */

async function fetchChart(lab, endpoint) {
  const res = await fetch(`/api/analytics/${lab}/${endpoint}`);
  return res.json();
}

// Example usage (Chart.js later):
// fetchChart('chemistry', 'aging').then(console.log);