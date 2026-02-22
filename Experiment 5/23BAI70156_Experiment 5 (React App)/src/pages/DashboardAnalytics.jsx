import { useSelector } from "react-redux";
import { calculateTotalCarbon, classifyCarbon } from "../utils/carbon";

const DashboardAnalytics = () => {
  const logs = useSelector((state) => state.logs.data);

  const total = calculateTotalCarbon(logs);
  const category = classifyCarbon(total);

  return (
    <div>
      <h3>Analytics</h3>
      <p>Total Carbon: {total} kg CO2</p>
      <p>Impact Level: {category}</p>
    </div>
  );
};

export default DashboardAnalytics;