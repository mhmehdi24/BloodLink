// ------------------------------------------------------------
// BloodLink API helper
// Wraps fetch() so every screen can call the API consistently.
// ------------------------------------------------------------

const API_BASE = "http://127.0.0.1:5000";

async function request(method, path, body) {
    const options = {
        method: method,
        headers: { "Content-Type": "application/json" },
    };
    if (body !== undefined) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(API_BASE + path, options);
    const text = await response.text();
    const data = text ? JSON.parse(text) : null;

    if (!response.ok) {
        const err = new Error((data && data.error) || `HTTP ${response.status}`);
        err.status = response.status;
        err.data = data;
        throw err;
    }
    return data;
}

const api = {
    get:   (path)        => request("GET", path),
    post:  (path, body)  => request("POST", path, body),
    patch: (path, body)  => request("PATCH", path, body),
};