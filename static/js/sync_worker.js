import Dexie from "./dexie.min.js";
const db = new Dexie("LIMSOffline");
db.version(1).stores({ pending: "++id, lab, payload" });
window.queueSync = (lab, payload) => db.pending.add({ lab, payload });
navigator.serviceWorker.ready.then(reg => reg.sync.register("sync-updates"));