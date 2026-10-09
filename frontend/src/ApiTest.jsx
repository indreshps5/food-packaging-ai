import { useEffect, useState } from "react";
import { getCommodities } from "./api";

export default function ApiTest() {
  const [commodities, setCommodities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getCommodities()
      .then((data) => {
        const items = Array.isArray(data)
          ? data
          : data.commodities ?? data.items ?? [];

        setCommodities(items);
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: "30px", fontFamily: "Arial, sans-serif" }}>
      <h1>Food Packaging AI — API Test</h1>

      {loading && <p>Loading commodities from the backend...</p>}

      {error && (
        <p style={{ color: "red" }}>
          API connection failed: {error}
        </p>
      )}

      {!loading && !error && (
        <>
          <p style={{ color: "green" }}>
            Backend connection successful!
          </p>

          {commodities.length === 0 ? (
            <p>The API responded, but no commodity list was found.</p>
          ) : (
            <ul>
              {commodities.map((item, index) => (
                <li key={item.id ?? index}>
                  {item.name ?? JSON.stringify(item)}
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </div>
  );
}