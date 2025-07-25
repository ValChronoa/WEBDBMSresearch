/* static/js/qr.js */
/* QR generator + live camera scanner helpers */

/* ---------- GENERATE ---------- */
function makeQR(lab, itemId) {
  const img = document.getElementById('qr-img');
  if (!img) return;
  img.src = `/api/qr/generate/${lab}/${itemId}`;
  img.style.display = 'block';
}

/* ---------- SCAN ---------- */
async function startScanner(onResult) {
  const video = document.getElementById('qr-video');
  if (!video) return;

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ 
      video: { facingMode: 'environment' } 
    });
    video.srcObject = stream;
    video.style.display = 'block';
    await video.play();

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    let frameCount = 0;
    let scanning = true;

    const tick = () => {
      if (!scanning) return;
      
      frameCount++;
      // Only process every 3rd frame
      if (frameCount % 3 !== 0) {
        requestAnimationFrame(tick);
        return;
      }

      if (video.readyState >= video.HAVE_ENOUGH_DATA) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0);

        canvas.toBlob(blob => {
          const fd = new FormData();
          fd.append('image', blob);
          fetch('/api/qr/decode', { method: 'POST', body: fd })
            .then(r => r.json())
            .then(({ data }) => {
              if (data) {
                onResult(data);
                scanning = false;
                stream.getTracks().forEach(t => t.stop());
              }
            });
        });
      }
      requestAnimationFrame(tick);
    };
    tick();
  } catch (err) {
    console.error("Camera error:", err);
    // Fallback to file upload
    document.getElementById('file-upload').style.display = 'block';
  }
}

// To stop the scanner
function stopScanner() {
  scanning = false;
}