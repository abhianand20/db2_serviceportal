const API_BASE = "http://localhost:8000/api/v1";



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

