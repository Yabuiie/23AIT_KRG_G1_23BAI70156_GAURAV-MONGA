import { useEffect, useCallback } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchLogs } from "../store/logSlice";
import LoadingSpinner from "../components/Loading";
import CarbonCard from "../components/CarbonCard";
import { calculateTotalCarbon } from "../utils/carbon";

const Logs = () => {
  const dispatch = useDispatch();
  const { data, status, error } = useSelector((state) => state.logs);

  const handleRefresh = useCallback(() => {
    dispatch(fetchLogs());
  }, [dispatch]);

  useEffect(() => {
    if (status === "idle") {
      dispatch(fetchLogs());
    }
  }, [status, dispatch]);

  if(status === "loading"){
    return <LoadingSpinner />;
  }
  if(status === "failed"){
    return <p>Error: {error}</p>;
  }
  const totalCarbon = calculateTotalCarbon(data);

  return (
    <div>
      <h1>Logs</h1>

      {data.map((log) => (
        <CarbonCard
          key={log.id}
          activity={log.activity}
          carbon={log.carbon}
        />
      ))}

      <h3 data-testid="total-carbon">
        Total Carbon: {totalCarbon} kg CO2
      </h3>

      <button onClick={handleRefresh}>Refresh</button>
    </div>
  );
};

export default Logs;