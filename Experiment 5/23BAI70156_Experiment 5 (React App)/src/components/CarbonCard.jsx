const CarbonCard = ({ activity, carbon }) => {
  return (
    <div>
      <h4>{activity}</h4>
      <p>{carbon} kg CO2</p>
    </div>
  );
};

export default CarbonCard;