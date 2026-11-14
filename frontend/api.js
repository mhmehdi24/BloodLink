// ------------------------------------------------------------
// BloodLink API helper
// Wraps fetch() so every screen can call the API consistently.
// ------------------------------------------------------------

function getApiBase() {
    // 1. Check for manual override in localStorage
    const savedBase = localStorage.getItem("BLOODLINK_API_BASE");
    if (savedBase) return savedBase.replace(/\/+$/, "");

    // 2. Check if running in a local environment (localhost, 127.0.0.1)
    const hostname = window.location.hostname;
    const isLocal = hostname === "localhost" || hostname === "127.0.0.1";

    if (isLocal) {
        return "http://127.0.0.1:5000";
    }

    // 3. If running in browser over HTTP/HTTPS (e.g. Vercel), use current origin
    if (window.location.origin && window.location.origin.startsWith("http")) {
        return window.location.origin;
    }

    // 4. Fallback for file:// or offline preview
    return "http://127.0.0.1:5000";
}

const API_BASE = getApiBase();

async function request(method, path, body) {
    const options = {
        method: method,
        headers: { "Content-Type": "application/json" },
    };
    if (body !== undefined) {
        options.body = JSON.stringify(body);
    }

    const cleanPath = path.startsWith("/") ? path : `/${path}`;
    const targetUrl = API_BASE + cleanPath;

    let response;
    try {
        response = await fetch(targetUrl, options);
    } catch (networkErr) {
        console.error(`API Network Error [${method} ${targetUrl}]:`, networkErr);
        const err = new Error(`Cannot connect to backend server at ${API_BASE}. Make sure the Flask API server is running on http://127.0.0.1:5000.`);
        err.isNetworkError = true;
        throw err;
    }

    const text = await response.text();
    let data = null;
    try {
        data = text ? JSON.parse(text) : null;
    } catch {
        data = { raw: text };
    }

    if (!response.ok) {
        const message = (data && (data.error || data.reason || data.message)) || `HTTP ${response.status}`;
        const err = new Error(message);
        err.status = response.status;
        err.data = data;
        throw err;
    }
    return data;
}

const api = {
    getBaseUrl: () => API_BASE,
    get:    (path)        => request("GET", path),
    post:   (path, body)  => request("POST", path, body),
    patch:  (path, body)  => request("PATCH", path, body),
    delete: (path, body)  => request("DELETE", path, body),
};