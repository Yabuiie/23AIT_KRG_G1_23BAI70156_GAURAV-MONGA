import React from "react";

const Counter = React.memo(({ count, goal }) => {
  console.log("CounterDisplay Rendered");

  return (
    <div>
      <h2>{count} / {goal} glasses completed</h2>
    </div>
  );
});

export default Counter;