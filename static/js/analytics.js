/* static/js/analytics.js */
/* Thin wrapper around the analytics endpoints */

async function fetchChart(lab, endpoint) {
  const res = await fetch(`/api/analytics/${lab}/${endpoint}`);
  if (!res.ok) throw new Error(res.statusText);
  return res.json();
}