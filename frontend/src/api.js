const API_BASE_URL = "https://food-packaging-ai-omega.vercel.app/api/v1";

const TOKEN_STORAGE_KEY = "foodPackagingAccessToken";

function getAccessToken() {
  return localStorage.getItem(TOKEN_STORAGE_KEY);
}

function saveAccessToken(token) {
  if (token) {
    localStorage.setItem(TOKEN_STORAGE_KEY, token);
  }
}

export function clearAccessToken() {
  localStorage.removeItem(TOKEN_STORAGE_KEY);
}

async function request(endpoint, options = {}) {
  const token = getAccessToken();
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  // Add a bearer token to requests when the user has logged in.
  if (token && !headers.Authorization && !headers.authorization) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const detail = data?.detail;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail.map((item) => item.msg || JSON.stringify(item)).join(", ")
          : `Request failed with status ${response.status}`;

    throw new Error(message);
  }

  return data;
}

export function getCommodities() {
  return request("/commodities/");
}

export function getPackagingMaterials() {
  // Keep this path aligned with the backend admin router.
  return request("/admin/packaging");
}

export function getRecommendations(payload) {
  return request("/recommendations/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function comparePackaging(payload) {
  return request("/compare/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getHistory() {
  return request("/history/");
}

export async function registerUser(payload) {
  return request("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function loginUser(payload) {
  const data = await request("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });

  saveAccessToken(data.access_token);
  return data;
}
