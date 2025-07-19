/* global Instascan */
window.startScanner = function (cb) {
  const scanner = new Instascan.Scanner({ video: document.getElementById("preview") });
  scanner.addListener("scan", cb);
  Instascan.Camera.getCameras().then(cameras => {
    if (cameras.length) scanner.start(cameras[0]);
  });
};