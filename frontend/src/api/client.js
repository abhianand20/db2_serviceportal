// const API_BASE = "http://localhost:8000/api/v1";

// src/client.js or wherever you define API_BASE
export const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000/api/v1";

console.log("API_BASE:", API_BASE);
// // client.js or api.js
// const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000/api/v1";

// console.log("API_BASE:", API_BASE);
// const API_BASE = "http://192.168.56.21:30008/api/v1"; 
// --This is for kubernetes deployment, for local development use "http://localhost:8000/api/v1"

// export async function apiGet(server, instance, dbName, endpoint) {
//   // Make sure endpoint starts with "/"
//   const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;

//   // Build URL
//   const url = `${API_BASE}/databases/${dbName}${path}`;

//   try {
//     const res = await fetch(url);
//     if (!res.ok) {
//       throw new Error(`HTTP error! status: ${res.status}`);
//     }
//     return await res.json();
//   } catch (err) {
//     console.error("API fetch error:", err);
//     return null;
//   }
// }

export async function apiGet(server, instance, dbName, endpoint = "") {
  if (!endpoint) {
    throw new Error("apiGet: endpoint is required");
  }

  const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  const url = `${API_BASE}/databases/${dbName}${path}`;

  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }
  return res.json();
}

