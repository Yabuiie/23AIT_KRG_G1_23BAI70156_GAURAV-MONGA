import { useState, useEffect, useCallback } from "react";
import Counter from "../components/Counter.jsx";

function Tracker() {
  const [count, setCount] = useState(() => {
    const saved = localStorage.getItem("waterCount");
    return saved !== null ? Number(saved) : 0;
  });

  const [goal, setGoal] = useState(8);
  const [tip, setTip] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Save count to localStorage
  useEffect(() => {
    localStorage.setItem("waterCount", count);
  }, [count]);

  // ✅ Reusable Fetch Function
  const fetchTip = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch("https://api.adviceslip.com/advice");
      const data = await response.json();

      setTip(data.slip.advice);
    } catch (err) {
      setError("Failed to fetch tip.");
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch once on mount
  useEffect(() => {
    fetchTip();
  }, [fetchTip]);

  // Optimized counter functions
  const increment = useCallback(() => {
    setCount((prev) => prev + 1);
  }, []);

  const decrement = useCallback(() => {
    setCount((prev) => (prev > 0 ? prev - 1 : 0));
  }, []);

  const reset = useCallback(() => {
    setCount(0);
  }, []);

  return (
    <div className="container">
      <h2>Water Tracker</h2>

      <div className="card">
        <Counter count={count} goal={goal} />

        {count >= goal && (
          <p className="success">🎉 Goal Reached!</p>
        )}

        <div className="buttons">
          <button onClick={increment}>+</button>
          <button onClick={decrement}>-</button>
          <button onClick={reset}>Reset</button>
        </div>

        <div>
          <label>Set Daily Goal: </label>
          <input
            type="number"
            value={goal}
            onChange={(e) => setGoal(Number(e.target.value))}
          />
        </div>

        <div className="tip">
          <h3>Today's Health Tip:</h3>

          {loading && <p>Loading...</p>}
          {error && <p>{error}</p>}
          {!loading && !error && <p>{tip}</p>}

          <button onClick={fetchTip} disabled={loading}>
            {loading ? "Fetching..." : "Get New Tip"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Tracker;