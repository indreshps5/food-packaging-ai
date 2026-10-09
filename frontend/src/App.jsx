import { useEffect, useMemo, useState } from "react";
import {
  clearAccessToken,
  getCommodities,
  getHistory,
  getPackagingMaterials,
  getRecommendations,
  loginUser,
  registerUser,
  comparePackaging,
} from "./api";

const navigation = ["Dashboard", "Recommendations", "Compare Packaging", "History", "Admin"];

const inputClass =
  "w-full rounded-xl border border-slate-200 bg-white px-4 py-3 outline-none focus:border-emerald-500";

const defaultStorage = {
  temperature: "25",
  humidity: "60",
  duration: "30",
  transportation: "Road",
};

/* ---------- helpers for reading backend results safely ---------- */

function fmt(value) {
  const n = Number(value);
  if (value === null || value === undefined || value === "" || !Number.isFinite(n)) return "—";
  return String(Math.round(n * 100) / 100);
}

function normalizeEntry(entry) {
  const e = entry || {};
  const pkg = e.packaging || {};
  const scores = e.scores || e;
  const id = pkg.id ?? e.packaging_id ?? e.material_id ?? e.id;
  return {
    id,
    name: pkg.name ?? e.name ?? e.packaging_name ?? e.material_name ?? (id !== undefined ? `Material #${id}` : "Unknown material"),
    type: pkg.material_type ?? e.material_type ?? "",
    structure: pkg.structure ?? e.structure ?? "",
    thickness: pkg.thickness ?? e.thickness,
    overall: scores.overall_score,
    quality: scores.quality_score,
    cost: scores.cost_score,
    sustainability: scores.sustainability_score,
    shelfDays: e.shelf_life?.estimated_days ?? e.estimated_shelf_life_days ?? e.estimated_days,
  };
}

function normalizeRecommendation(data) {
  const rec = data?.recommendation ?? data ?? {};
  const top = normalizeEntry(rec.packaging ? rec : { ...rec, packaging: undefined });
  if (!rec.packaging && data?.recommended_material_id !== undefined) {
    top.name = `Material #${data.recommended_material_id}`;
  }
  return {
    top,
    shelf: rec.shelf_life ?? data?.shelf_life ?? null,
    explanation: rec.explanation ?? data?.explanation ?? "",
    alternatives: data?.alternatives ?? rec.alternatives ?? [],
  };
}

function findList(result) {
  if (Array.isArray(result)) return result;
  if (!result || typeof result !== "object") return null;
  const keys = ["comparison", "comparisons", "results", "packaging", "materials", "options", "rankings", "ranked", "alternatives", "items"];
  for (const key of keys) {
    if (Array.isArray(result[key])) return result[key];
  }
  for (const value of Object.values(result)) {
    if (Array.isArray(value) && value.length && typeof value[0] === "object") return value;
  }
  return null;
}

function App() {
  const [commodities, setCommodities] = useState([]);
  const [commoditiesLoading, setCommoditiesLoading] = useState(true);
  const [commoditiesError, setCommoditiesError] = useState("");
  const [activePage, setActivePage] = useState("Dashboard");
  const [selectedCommodityId, setSelectedCommodityId] = useState("");
  const [search, setSearch] = useState("");
  const [showAll, setShowAll] = useState(false);
  const [storage, setStorage] = useState(defaultStorage);
  const [authMode, setAuthMode] = useState("login");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(
    Boolean(localStorage.getItem("foodPackagingAccessToken"))
  );
  const [authMessage, setAuthMessage] = useState("");
  const [authError, setAuthError] = useState("");
  const [busy, setBusy] = useState(false);
  const [recommendation, setRecommendation] = useState(null);
  const [recommendationError, setRecommendationError] = useState("");
  const [history, setHistory] = useState([]);
  const [historyError, setHistoryError] = useState("");
  const [compareResult, setCompareResult] = useState(null);
  const [compareError, setCompareError] = useState("");
  const [materials, setMaterials] = useState([]);
  const [materialsError, setMaterialsError] = useState("");
  const [materialsLoaded, setMaterialsLoaded] = useState(false);

  useEffect(() => {
    let cancelled = false;
    getCommodities()
      .then((data) => {
        if (cancelled) return;
        const items = Array.isArray(data)
          ? data
          : data?.commodities ?? data?.items ?? [];
        setCommodities(items);
        if (items.length) setSelectedCommodityId(String(items[0].id));
      })
      .catch((error) => {
        if (!cancelled) setCommoditiesError(error.message || "Failed to load commodities.");
      })
      .finally(() => {
        if (!cancelled) setCommoditiesLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  // Automatically load history when the History page is opened
  useEffect(() => {
    if (activePage === "History" && isAuthenticated) {
      loadHistory();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activePage, isAuthenticated]);

  const selectedCommodity = useMemo(
    () => commodities.find((item) => String(item.id) === String(selectedCommodityId)),
    [commodities, selectedCommodityId]
  );

  const filteredCommodities = useMemo(
    () => commodities.filter((item) => String(item.name || "").toLowerCase().includes(search.toLowerCase())),
    [commodities, search]
  );

  function commodityNameById(id) {
    const found = commodities.find((item) => String(item.id) === String(id));
    return found ? found.name : "";
  }

  function updateStorage(field, value) {
    setStorage((previous) => ({ ...previous, [field]: value }));
  }

  async function handleAuthSubmit(event) {
    event.preventDefault();
    setBusy(true);
    setAuthError("");
    setAuthMessage("");
    try {
      if (authMode === "register") {
        await registerUser({ username: username.trim(), email: email.trim(), password });
        setAuthMessage("Account created. Please sign in with your username and password.");
        setAuthMode("login");
        setPassword("");
      } else {
        await loginUser({ username: username.trim(), password });
        setIsAuthenticated(true);
        setAuthMessage("Signed in successfully.");
        setPassword("");
      }
    } catch (error) {
      setAuthError(error.message || "Authentication failed.");
    } finally {
      setBusy(false);
    }
  }

  function handleLogout() {
    clearAccessToken();
    setIsAuthenticated(false);
    setRecommendation(null);
    setHistory([]);
    setAuthMessage("You have signed out.");
    setActivePage("Dashboard");
  }

  function buildPayload() {
    const food = selectedCommodity.food_properties || {};
    return {
      commodity_id: selectedCommodity.id,
      food_properties: {
        moisture_content: Number(food.moisture_content ?? 0),
        oil_fat_content: Number(food.oil_fat_content ?? 0),
        pH: Number(food.pH ?? 7),
        respiration_rate: Number(food.respiration_rate ?? 0),
      },
      storage_conditions: {
        temperature: Number(storage.temperature),
        humidity: Number(storage.humidity),
        storage_duration: Number(storage.duration),
        transportation_type: storage.transportation,
      },
    };
  }

  async function handleRecommendation() {
    if (!selectedCommodity) {
      setRecommendationError("Please select a food commodity.");
      return;
    }
    if (!isAuthenticated) {
      setRecommendationError("Please sign in before generating a recommendation.");
      return;
    }

    setBusy(true);
    setRecommendationError("");
    setRecommendation(null);
    try {
      const result = await getRecommendations(buildPayload());
      setRecommendation(result);
    } catch (error) {
      setRecommendationError(error.message || "Could not generate recommendation.");
    } finally {
      setBusy(false);
    }
  }

  async function loadHistory() {
    if (!isAuthenticated) {
      setHistoryError("Please sign in to view your recommendation history.");
      setHistory([]);
      return;
    }
    setBusy(true);
    setHistoryError("");
    try {
      const result = await getHistory();
      const items = Array.isArray(result) ? result : result?.history ?? [];
      setHistory([...items].sort((a, b) => (b.recommendation_id ?? 0) - (a.recommendation_id ?? 0)));
    } catch (error) {
      setHistoryError(error.message || "Could not load history.");
    } finally {
      setBusy(false);
    }
  }

  async function handleCompare() {
    if (!selectedCommodity) {
      setCompareError("Please select a food commodity.");
      return;
    }
    setBusy(true);
    setCompareError("");
    setCompareResult(null);
    try {
      const result = await comparePackaging(buildPayload());
      setCompareResult(result);
    } catch (error) {
      setCompareError(error.message || "Could not compare packaging.");
    } finally {
      setBusy(false);
    }
  }

  async function loadMaterials() {
    setBusy(true);
    setMaterialsError("");
    try {
      const result = await getPackagingMaterials();
      const items = Array.isArray(result) ? result : findList(result) ?? [];
      setMaterials(items);
      setMaterialsLoaded(true);
    } catch (error) {
      setMaterialsError(error.message || "Could not load packaging materials.");
    } finally {
      setBusy(false);
    }
  }

  function pageContent() {
    if (activePage === "Recommendations") {
      return (
        <div className="space-y-6">
          <Panel title="Generate a packaging recommendation" subtitle="Select a food and enter its storage conditions.">
            {commoditiesLoading ? <p>Loading commodities…</p> : null}
            {commoditiesError ? <ErrorText>{commoditiesError}</ErrorText> : null}
            <div className="grid gap-5 sm:grid-cols-2">
              <Field label="Food commodity">
                <select className={inputClass} value={selectedCommodityId} onChange={(e) => setSelectedCommodityId(e.target.value)}>
                  {commodities.map((item) => <option key={item.id} value={String(item.id)}>{item.name}</option>)}
                </select>
              </Field>
              <Field label="Storage temperature (°C)">
                <input className={inputClass} type="number" value={storage.temperature} onChange={(e) => updateStorage("temperature", e.target.value)} />
              </Field>
              <Field label="Relative humidity (%)">
                <input className={inputClass} type="number" min="0" max="100" value={storage.humidity} onChange={(e) => updateStorage("humidity", e.target.value)} />
              </Field>
              <Field label="Storage duration (days)">
                <input className={inputClass} type="number" min="1" value={storage.duration} onChange={(e) => updateStorage("duration", e.target.value)} />
              </Field>
              <Field label="Transportation">
                <select className={inputClass} value={storage.transportation} onChange={(e) => updateStorage("transportation", e.target.value)}>
                  <option>Road</option><option>Rail</option><option>Air</option><option>Sea</option>
                </select>
              </Field>
            </div>
            {!isAuthenticated ? <p className="mt-4 text-sm text-amber-700">Sign in is required to generate a recommendation. Use the account panel in the header.</p> : null}
            {recommendationError ? <ErrorText>{recommendationError}</ErrorText> : null}
            <button disabled={busy || commoditiesLoading || !commodities.length} onClick={handleRecommendation} className="mt-6 rounded-xl bg-emerald-600 px-6 py-3 font-semibold text-white hover:bg-emerald-700 disabled:opacity-50">
              {busy ? "Please wait…" : "✧ Generate recommendation"}
            </button>
          </Panel>
          {recommendation ? (
            <RecommendationCard
              data={recommendation}
              heading={`Recommended packaging for ${selectedCommodity?.name ?? "your food"}`}
            />
          ) : null}
        </div>
      );
    }

    if (activePage === "Compare Packaging") {
      return (
        <div className="space-y-6">
          <Panel title="Compare packaging materials" subtitle="Compare packaging options using the selected commodity and storage conditions.">
            <div className="grid gap-4 sm:grid-cols-2">
              <Field label="Food commodity">
                <select className={inputClass} value={selectedCommodityId} onChange={(e) => setSelectedCommodityId(e.target.value)}>
                  {commodities.map((item) => <option key={item.id} value={String(item.id)}>{item.name}</option>)}
                </select>
              </Field>
              <Field label="Storage temperature (°C)">
                <input className={inputClass} type="number" value={storage.temperature} onChange={(e) => updateStorage("temperature", e.target.value)} />
              </Field>
              <Field label="Relative humidity (%)">
                <input className={inputClass} type="number" value={storage.humidity} onChange={(e) => updateStorage("humidity", e.target.value)} />
              </Field>
              <Field label="Storage duration (days)">
                <input className={inputClass} type="number" value={storage.duration} onChange={(e) => updateStorage("duration", e.target.value)} />
              </Field>
              <Field label="Transportation">
                <select className={inputClass} value={storage.transportation} onChange={(e) => updateStorage("transportation", e.target.value)}>
                  <option>Road</option><option>Rail</option><option>Air</option><option>Sea</option>
                </select>
              </Field>
            </div>
            {compareError ? <ErrorText>{compareError}</ErrorText> : null}
            <button disabled={busy || !selectedCommodity} onClick={handleCompare} className="mt-5 rounded-xl bg-emerald-600 px-5 py-3 font-semibold text-white disabled:opacity-50">{busy ? "Please wait…" : "Compare packaging"}</button>
          </Panel>
          {compareResult ? <CompareResults result={compareResult} commodityName={selectedCommodity?.name} /> : null}
        </div>
      );
    }

    if (activePage === "History") {
      return (
        <Panel title="Recommendation history" subtitle="View recommendations saved to your account. Newest first.">
          <button disabled={busy} onClick={loadHistory} className="rounded-xl bg-emerald-600 px-5 py-3 font-semibold text-white disabled:opacity-50">{busy ? "Loading…" : "Refresh history"}</button>
          {!isAuthenticated ? <p className="mt-4 text-sm text-amber-700">Please sign in to view your saved recommendations.</p> : null}
          {historyError ? <ErrorText>{historyError}</ErrorText> : null}
          {isAuthenticated && !historyError && !busy && history.length === 0 ? <p className="mt-4 text-sm text-slate-500">No saved recommendations yet. Generate one from the Recommendations page.</p> : null}
          <div className="mt-5 space-y-3">
            {history.map((item, index) => (
              <HistoryItem key={item.recommendation_id ?? index} item={item} index={index} commodityName={commodityNameById(item.commodity_id)} />
            ))}
          </div>
        </Panel>
      );
    }

    if (activePage === "Admin") {
      return (
        <div className="space-y-6">
          <Panel title="Administration" subtitle="Review the commodity and packaging data used by the recommendation engine.">
            <div className="flex flex-wrap items-center gap-3">
              <button disabled={busy} onClick={loadMaterials} className="rounded-xl bg-emerald-600 px-5 py-3 font-semibold text-white disabled:opacity-50">{busy ? "Loading…" : "Load packaging materials"}</button>
              <span className="text-sm text-slate-500">Admin routes may require an admin account on the backend.</span>
            </div>
            {materialsError ? <ErrorText>{materialsError}</ErrorText> : null}
            {materialsLoaded && materials.length === 0 && !materialsError ? <p className="mt-4 text-sm text-slate-500">No packaging materials were returned.</p> : null}
            {materials.length > 0 ? (
              <div className="mt-5 overflow-x-auto rounded-xl border border-slate-200">
                <table className="min-w-full text-left text-sm">
                  <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                    <tr>
                      <th className="px-4 py-3">ID</th>
                      <th className="px-4 py-3">Name</th>
                      <th className="px-4 py-3">Type</th>
                      <th className="px-4 py-3">Structure</th>
                      <th className="px-4 py-3">Thickness</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {materials.map((m, i) => (
                      <tr key={m.id ?? i}>
                        <td className="px-4 py-3 text-slate-500">{m.id ?? "—"}</td>
                        <td className="px-4 py-3 font-semibold">{m.name ?? "—"}</td>
                        <td className="px-4 py-3">{m.material_type ?? "—"}</td>
                        <td className="px-4 py-3 text-slate-600">{m.structure ?? "—"}</td>
                        <td className="px-4 py-3">{m.thickness ?? "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : null}
          </Panel>
          <Panel title="Food commodities" subtitle={`${commodities.length} commodities in the catalogue.`}>
            <div className="overflow-x-auto rounded-xl border border-slate-200">
              <table className="min-w-full text-left text-sm">
                <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                  <tr>
                    <th className="px-4 py-3">ID</th>
                    <th className="px-4 py-3">Name</th>
                    <th className="px-4 py-3">Category</th>
                    <th className="px-4 py-3">Moisture %</th>
                    <th className="px-4 py-3">Oil/fat %</th>
                    <th className="px-4 py-3">pH</th>
                    <th className="px-4 py-3">Respiration</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {commodities.map((c) => (
                    <tr key={c.id}>
                      <td className="px-4 py-3 text-slate-500">{c.id}</td>
                      <td className="px-4 py-3 font-semibold">{c.name}</td>
                      <td className="px-4 py-3">{c.category ?? "—"}</td>
                      <td className="px-4 py-3">{fmt(c.food_properties?.moisture_content)}</td>
                      <td className="px-4 py-3">{fmt(c.food_properties?.oil_fat_content)}</td>
                      <td className="px-4 py-3">{fmt(c.food_properties?.pH)}</td>
                      <td className="px-4 py-3">{fmt(c.food_properties?.respiration_rate)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Panel>
        </div>
      );
    }

    return (
      <div className="space-y-6">
        <section className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-emerald-700 to-teal-600 p-7 text-white sm:p-9">
          <div className="relative z-10 max-w-xl">
            <span className="inline-flex rounded-full bg-white/15 px-3 py-1.5 text-xs font-medium">Intelligent packaging platform</span>
            <h2 className="mt-5 text-3xl font-bold leading-tight sm:text-4xl">Smarter packaging.<br />Fresher food.</h2>
            <p className="mt-4 max-w-lg text-sm leading-6 text-emerald-50 sm:text-base">Discover suitable packaging materials using food characteristics, storage conditions, barrier properties and sustainability considerations.</p>
            <button onClick={() => setActivePage("Recommendations")} className="mt-6 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-emerald-800 hover:bg-emerald-50">Get a recommendation →</button>
          </div>
          <div className="pointer-events-none absolute -right-12 -top-12 hidden h-72 w-72 rounded-full border border-white/15 sm:block" />
          <div className="pointer-events-none absolute -right-2 top-12 hidden h-48 w-48 rounded-full border border-white/15 sm:block" />
        </section>

        <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Food commodities" value={String(commodities.length)} note="Loaded from backend" icon="🌾" />
          <StatCard label="Packaging materials" value="Backend" note="Available routes vary" icon="▤" />
          <StatCard label="Recommendation engine" value="Connected" note="Uses backend API" icon="✧" />
          <StatCard label="Sustainability" value="Included" note="Depends on backend result" icon="♧" />
        </section>

        <section className="grid gap-6 xl:grid-cols-5">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 sm:p-6 xl:col-span-3">
            <div className="flex flex-wrap items-center justify-between gap-3"><div><h2 className="text-lg font-bold">Food commodities</h2><p className="mt-1 text-sm text-slate-500">Available foods in your catalogue</p></div><button onClick={() => setShowAll(!showAll)} className="rounded-lg border border-slate-200 px-3 py-2 text-sm hover:bg-slate-50">{showAll ? "Show less" : "View all"} →</button></div>
            {showAll ? <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search commodities..." className={`${inputClass} mt-4`} /> : null}
            {commoditiesLoading ? <p className="mt-4 text-sm text-slate-500">Loading commodities…</p> : null}
            {commoditiesError ? <ErrorText>{commoditiesError}</ErrorText> : null}
            <div className="mt-5 divide-y divide-slate-100">
              {(showAll ? filteredCommodities : commodities.slice(0, 4)).map((item) => <button key={item.id} onClick={() => { setSelectedCommodityId(String(item.id)); setActivePage("Recommendations"); }} className="flex w-full items-center gap-3 py-3.5 text-left hover:bg-slate-50"><div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-50 text-xl">{({ Rice: "🌾", Wheat: "🌿", Potato: "🥔", Peanuts: "🥜", Apple: "🍎" })[item.name] ?? "📦"}</div><div className="min-w-0 flex-1"><p className="font-semibold">{item.name}</p><p className="mt-1 text-xs text-slate-500">{item.category}</p></div><span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-medium text-emerald-700">Available</span></button>)}
            </div>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-5 sm:p-6 xl:col-span-2"><h2 className="text-lg font-bold">How it works</h2><p className="mt-1 text-sm text-slate-500">From food properties to material selection</p><div className="mt-6 space-y-5"><ProcessStep number="01" title="Select a commodity" description="Choose the food you want to package." /><ProcessStep number="02" title="Define storage conditions" description="Provide temperature, humidity and duration." /><ProcessStep number="03" title="Evaluate packaging" description="Assess suitability and relevant criteria." /><ProcessStep number="04" title="Review recommendations" description="Explore ranked options and explanations." /></div></div>
        </section>
        <p className="text-center text-xs leading-5 text-slate-400">Food Packaging AI · SIH 2026 Prototype<br />Scores and shelf-life estimates require scientific validation before real-world use.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-64 flex-col border-r border-slate-200 bg-white lg:flex">
        <div className="flex h-20 items-center gap-3 border-b border-slate-100 px-6"><div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-600 text-2xl text-white">♧</div><div><h1 className="text-base font-bold tracking-tight">Food Packaging AI</h1><p className="mt-0.5 text-xs text-slate-500">Intelligent systems</p></div></div>
        <div className="px-4 pt-7"><p className="mb-3 px-3 text-xs font-semibold uppercase tracking-widest text-slate-400">Workspace</p><nav className="space-y-1">{navigation.slice(0, 4).map((page) => <button key={page} onClick={() => { setActivePage(page); if (page === "History") { setHistoryError(""); } }} className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-medium ${activePage === page ? "bg-emerald-50 text-emerald-800" : "text-slate-600 hover:bg-slate-50"}`}><span className="w-5 text-center text-lg">{page === "Dashboard" ? "▦" : page === "Recommendations" ? "✧" : page === "History" ? "◷" : "⇄"}</span>{page}</button>)}</nav></div>
        <div className="mt-7 px-4"><p className="mb-3 px-3 text-xs font-semibold uppercase tracking-widest text-slate-400">Management</p><button onClick={() => setActivePage("Admin")} className={`flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-medium ${activePage === "Admin" ? "bg-emerald-50 text-emerald-800" : "text-slate-600 hover:bg-slate-50"}`}>⚙ Admin panel</button></div>
        <div className="mt-auto p-4"><div className="rounded-2xl bg-slate-50 p-4"><p className="text-xs font-semibold">● Prototype workspace</p><p className="mt-2 text-xs leading-5 text-slate-500">Intelligent packaging recommendations for food commodities.</p></div><p className="mt-4 px-2 text-xs text-slate-400">SIH 2026 · Project prototype</p></div>
      </aside>

      <div className="lg:pl-64">
        <header className="sticky top-0 z-10 flex min-h-20 flex-wrap items-center justify-between gap-4 border-b border-slate-200 bg-white/95 px-4 py-3 backdrop-blur sm:px-8">
          <div><p className="text-xs font-medium text-slate-400">Workspace / {activePage}</p><h2 className="mt-1 text-xl font-bold">{activePage}</h2></div>
          <div className="flex flex-wrap items-center gap-3">
            <span className="hidden rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-medium text-emerald-700 sm:inline-flex">Prototype</span>
            {isAuthenticated ? <><span className="text-sm text-emerald-800">Signed in</span><button onClick={handleLogout} className="rounded-lg border border-slate-200 px-3 py-2 text-sm hover:bg-slate-50">Sign out</button></> : <button onClick={() => { setAuthError(""); setAuthMessage(""); setAuthMode("login"); document.getElementById("auth-panel")?.scrollIntoView({ behavior: "smooth", block: "center" }); }} className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-700">Sign in / Register</button>}
          </div>
        </header>

        <main className="mx-auto max-w-[1500px] p-4 sm:p-8">
          {!isAuthenticated ? <section id="auth-panel" className="mb-6 rounded-2xl border border-emerald-100 bg-white p-5 sm:p-6"><h2 className="text-lg font-bold">{authMode === "login" ? "Sign in to your account" : "Create an account"}</h2><p className="mt-1 text-sm text-slate-500">{authMode === "login" ? "Sign in to generate recommendations and view saved history." : "Register with a username, email address and password."}</p><form onSubmit={handleAuthSubmit} className="mt-5 grid gap-4 sm:grid-cols-2"><Field label="Username"><input required autoComplete="username" className={inputClass} value={username} onChange={(e) => setUsername(e.target.value)} /></Field>{authMode === "register" ? <Field label="Email"><input required type="email" autoComplete="email" className={inputClass} value={email} onChange={(e) => setEmail(e.target.value)} /></Field> : null}<Field label="Password"><input required type="password" autoComplete={authMode === "login" ? "current-password" : "new-password"} className={inputClass} value={password} onChange={(e) => setPassword(e.target.value)} /></Field><div className="flex items-end gap-3"><button disabled={busy} type="submit" className="rounded-xl bg-emerald-600 px-5 py-3 font-semibold text-white disabled:opacity-50">{busy ? "Please wait…" : authMode === "login" ? "Sign in" : "Register"}</button><button type="button" onClick={() => { setAuthMode(authMode === "login" ? "register" : "login"); setAuthError(""); setAuthMessage(""); }} className="rounded-xl border border-slate-200 px-4 py-3 text-sm font-medium">{authMode === "login" ? "Create account" : "Back to sign in"}</button></div></form>{authError ? <ErrorText>{authError}</ErrorText> : null}{authMessage ? <p className="mt-3 text-sm text-emerald-700">{authMessage}</p> : null}</section> : authMessage ? <p className="mb-5 rounded-xl bg-emerald-50 p-3 text-sm text-emerald-800">{authMessage}</p> : null}
          <div className="mb-6 flex gap-2 overflow-x-auto pb-1 lg:hidden">{navigation.map((page) => <button key={page} onClick={() => setActivePage(page)} className={`shrink-0 rounded-xl px-3 py-2 text-sm font-medium ${activePage === page ? "bg-emerald-600 text-white" : "border border-slate-200 bg-white text-slate-600"}`}>{page}</button>)}</div>
          {pageContent()}
        </main>
      </div>
    </div>
  );
}

/* ---------- small shared components ---------- */

function Field({ label, children }) {
  return <div><label className="mb-2 block text-sm font-medium text-slate-700">{label}</label>{children}</div>;
}

function Panel({ title, subtitle, children }) {
  return <section className="rounded-2xl border border-slate-200 bg-white p-6"><h2 className="text-lg font-bold">{title}</h2>{subtitle ? <p className="mt-2 text-sm text-slate-500">{subtitle}</p> : null}<div className="mt-6">{children}</div></section>;
}

function StatCard({ label, value, note, icon }) {
  return <div className="rounded-2xl border border-slate-200 bg-white p-5"><div className="flex items-center justify-between"><p className="text-sm font-medium text-slate-500">{label}</p><span className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-xl">{icon}</span></div><p className="mt-4 text-2xl font-bold">{value}</p><p className="mt-1 text-xs text-slate-500">{note}</p></div>;
}

function ProcessStep({ number, title, description }) {
  return <div className="flex gap-4"><div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-sm font-bold text-emerald-700">{number}</div><div><h3 className="font-semibold">{title}</h3><p className="mt-1 text-sm leading-5 text-slate-500">{description}</p></div></div>;
}

function ErrorText({ children }) {
  return <p role="alert" className="mt-4 rounded-xl bg-red-50 p-3 text-sm text-red-700">{children}</p>;
}

function RawData({ data, force = false, label = "Show raw data" }) {
  if (!force) return null;
  return (
    <details className="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-3">
      <summary className="cursor-pointer text-sm font-medium text-slate-600">{label}</summary>
      <pre className="mt-3 overflow-x-auto whitespace-pre-wrap break-words text-xs text-slate-700">{JSON.stringify(data, null, 2)}</pre>
    </details>
  );
}

function ScoreBar({ label, value, color }) {
  const n = Number(value);
  const width = Number.isFinite(n) ? Math.max(0, Math.min(100, n * 10)) : 0;
  return (
    <div>
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium text-slate-600">{label}</span>
        <span className="font-bold">{fmt(value)}<span className="font-normal text-slate-400"> / 10</span></span>
      </div>
      <div className="mt-1.5 h-2.5 overflow-hidden rounded-full bg-slate-100">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${width}%` }} />
      </div>
    </div>
  );
}

function ScoreGrid({ entry }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <ScoreBar label="Overall" value={entry.overall} color="bg-emerald-600" />
      <ScoreBar label="Quality" value={entry.quality} color="bg-sky-500" />
      <ScoreBar label="Cost" value={entry.cost} color="bg-amber-500" />
      <ScoreBar label="Sustainability" value={entry.sustainability} color="bg-teal-500" />
    </div>
  );
}

function ShelfLife({ shelf }) {
  if (!shelf) return null;
  const est = Number(shelf.estimated_days);
  const base = Number(shelf.baseline_days);
  const diff = Number.isFinite(est) && Number.isFinite(base) ? est - base : null;
  return (
    <div className="rounded-xl border border-slate-200 p-4">
      <h4 className="text-sm font-semibold text-slate-700">Estimated shelf life</h4>
      <div className="mt-3 flex flex-wrap items-end gap-x-8 gap-y-3">
        <div>
          <p className="text-3xl font-bold text-emerald-700">{fmt(shelf.estimated_days)}<span className="ml-1 text-base font-medium text-slate-500">days</span></p>
          <p className="text-xs text-slate-500">With this packaging</p>
        </div>
        <div>
          <p className="text-xl font-semibold text-slate-700">{fmt(shelf.baseline_days)}<span className="ml-1 text-sm font-medium text-slate-500">days</span></p>
          <p className="text-xs text-slate-500">Baseline estimate</p>
        </div>
        {diff !== null ? (
          <span className={`rounded-full px-3 py-1 text-xs font-semibold ${diff >= 0 ? "bg-emerald-50 text-emerald-700" : "bg-red-50 text-red-700"}`}>
            {diff >= 0 ? "+" : ""}{fmt(diff)} days vs baseline
          </span>
        ) : null}
      </div>
      <p className="mt-3 text-xs leading-5 text-amber-700">Model estimate only. It is not a validated food-safety guarantee and needs scientific validation before real-world use.</p>
    </div>
  );
}

function AlternativesList({ alternatives }) {
  if (!Array.isArray(alternatives) || alternatives.length === 0) return null;
  const rows = alternatives.map(normalizeEntry);
  return (
    <div>
      <h4 className="text-sm font-semibold text-slate-700">Other options (ranked)</h4>
      <div className="mt-3 space-y-2">
        {rows.map((alt, index) => (
          <div key={alt.id ?? index} className="flex flex-wrap items-center gap-3 rounded-xl border border-slate-200 p-3">
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-sm font-bold text-slate-600">{index + 2}</span>
            <div className="min-w-0 flex-1">
              <p className="font-semibold">{alt.name}</p>
              <p className="text-xs text-slate-500">{[alt.type, alt.structure].filter(Boolean).join(" · ")}</p>
            </div>
            <div className="flex gap-4 text-center text-xs text-slate-500">
              <div><p className="text-sm font-bold text-slate-800">{fmt(alt.quality)}</p>Quality</div>
              <div><p className="text-sm font-bold text-slate-800">{fmt(alt.cost)}</p>Cost</div>
              <div><p className="text-sm font-bold text-slate-800">{fmt(alt.sustainability)}</p>Sustain.</div>
              <div><p className="text-sm font-bold text-emerald-700">{fmt(alt.overall)}</p>Overall</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function RecommendationCard({ data, heading, compact = false }) {
  const hasContent = data && (data.recommendation || data.scores);
  if (!hasContent) {
    return (
      <section className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
        <h3 className="font-semibold text-amber-900">No recommendation available</h3>
        <p className="mt-1 text-sm text-amber-800">{data?.message || data?.detail || "The backend did not return a suitable packaging material for these conditions."}</p>
        <RawData data={data} force />
      </section>
    );
  }
  const { top, shelf, explanation, alternatives } = normalizeRecommendation(data);
  return (
    <section className={compact ? "space-y-5" : "space-y-5 rounded-2xl border border-slate-200 bg-white p-6"}>
      {heading ? <p className="text-xs font-semibold uppercase tracking-widest text-slate-400">{heading}</p> : null}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl bg-gradient-to-r from-emerald-700 to-teal-600 p-5 text-white">
        <div>
          <span className="inline-flex rounded-full bg-white/20 px-3 py-1 text-xs font-semibold">★ Best match</span>
          <h3 className="mt-3 text-2xl font-bold">{top.name}</h3>
          <p className="mt-1 text-sm text-emerald-50">
            {[top.type, top.structure, top.thickness ? `${top.thickness} µm` : ""].filter(Boolean).join(" · ")}
          </p>
        </div>
        <div className="text-right">
          <p className="text-4xl font-bold">{fmt(top.overall)}</p>
          <p className="text-xs text-emerald-50">Overall score / 10</p>
        </div>
      </div>
      <ScoreGrid entry={top} />
      <ShelfLife shelf={shelf} />
      {explanation ? (
        <div className="rounded-xl bg-slate-50 p-4">
          <h4 className="text-sm font-semibold text-slate-700">Why this material?</h4>
          <p className="mt-2 text-sm leading-6 text-slate-600">{explanation}</p>
        </div>
      ) : null}
      <AlternativesList alternatives={alternatives} />
      <RawData data={data} />
    </section>
  );
}

function HistoryItem({ item, index, commodityName }) {
  const [open, setOpen] = useState(false);
  const { top, shelf } = normalizeRecommendation(item);
  return (
    <div className="rounded-xl border border-slate-200 p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="font-semibold">Recommendation #{item.recommendation_id ?? index + 1}</p>
          <p className="mt-1 text-sm text-slate-600">
            {commodityName ? `${commodityName} · ` : ""}Commodity ID: {item.commodity_id ?? "—"} · Material ID: {item.recommended_material_id ?? "—"}
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right">
            <p className="text-xl font-bold text-emerald-700">{fmt(top.overall)}</p>
            <p className="text-xs text-slate-500">Overall</p>
          </div>
          {shelf ? (
            <div className="text-right">
              <p className="text-xl font-bold text-slate-700">{fmt(shelf.estimated_days)}</p>
              <p className="text-xs text-slate-500">Shelf-life days</p>
            </div>
          ) : null}
          <button onClick={() => setOpen(!open)} className="rounded-lg border border-slate-200 px-3 py-2 text-sm hover:bg-slate-50">{open ? "Hide details" : "View details"}</button>
        </div>
      </div>
      {open ? <div className="mt-5 border-t border-slate-100 pt-5"><RecommendationCard data={item} compact /></div> : null}
    </div>
  );
}

function CompareResults({ result, commodityName }) {
  const list = findList(result);
  if (!list || list.length === 0 || typeof list[0] !== "object") {
    return (
      <section className="rounded-2xl border border-slate-200 bg-white p-6">
        <h3 className="text-lg font-bold">Comparison result</h3>
        <p className="mt-2 text-sm text-slate-500">The result format was not recognised, so the raw data is shown below.</p>
        <RawData data={result} force label="Raw comparison data" />
      </section>
    );
  }
  const rows = list.map(normalizeEntry);
  const sorted = rows.some((r) => Number.isFinite(Number(r.overall)))
    ? [...rows].sort((a, b) => Number(b.overall ?? -1) - Number(a.overall ?? -1))
    : rows;
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6">
      <h3 className="text-lg font-bold">Comparison result{commodityName ? ` for ${commodityName}` : ""}</h3>
      <p className="mt-1 text-sm text-slate-500">{sorted.length} packaging materials, ranked by overall score.</p>
      <div className="mt-5 overflow-x-auto rounded-xl border border-slate-200">
        <table className="min-w-full text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-3">Rank</th>
              <th className="px-4 py-3">Material</th>
              <th className="px-4 py-3">Quality</th>
              <th className="px-4 py-3">Cost</th>
              <th className="px-4 py-3">Sustainability</th>
              <th className="px-4 py-3">Overall</th>
              <th className="px-4 py-3">Shelf life</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {sorted.map((row, index) => (
              <tr key={row.id ?? index} className={index === 0 ? "bg-emerald-50/60" : ""}>
                <td className="px-4 py-3 font-bold text-slate-500">{index + 1}</td>
                <td className="px-4 py-3">
                  <p className="font-semibold">{row.name}{index === 0 ? <span className="ml-2 rounded-full bg-emerald-600 px-2 py-0.5 text-xs font-medium text-white">Best</span> : null}</p>
                  <p className="text-xs text-slate-500">{[row.type, row.structure].filter(Boolean).join(" · ")}</p>
                </td>
                <td className="px-4 py-3">{fmt(row.quality)}</td>
                <td className="px-4 py-3">{fmt(row.cost)}</td>
                <td className="px-4 py-3">{fmt(row.sustainability)}</td>
                <td className="px-4 py-3 font-bold text-emerald-700">{fmt(row.overall)}</td>
                <td className="px-4 py-3">{row.shelfDays !== undefined ? `${fmt(row.shelfDays)} days` : "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="mt-3 text-xs text-amber-700">Scores and shelf-life values are model estimates and need scientific validation.</p>
      <RawData data={result} label="Show raw comparison data" />
    </section>
  );
}

export default App;
