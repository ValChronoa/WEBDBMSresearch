document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  if (!form) return;
  form.addEventListener("submit", e => {
    const exp = document.querySelector("[name='expiration_date']")?.value;
    const cal = document.querySelector("[name='calibration_due']")?.value;
    if (exp && new Date(exp) < new Date()) {
      alert("Expiration date cannot be in the past."); e.preventDefault();
    }
    if (cal && new Date(cal) < new Date()) {
      alert("Calibration due date cannot be in the past."); e.preventDefault();
    }
  });
});