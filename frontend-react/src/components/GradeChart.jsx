/**
 * GradeChart – lazy loaded wrapper for Chart.js graphs.
 */
import React, { useEffect, useRef } from 'react';
import { Chart } from 'chart.js/auto';

function GradeChart({ config }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current) return;
    const chart = new Chart(canvasRef.current, config);
    return () => chart.destroy();
  }, [config]);

  return <canvas ref={canvasRef} role="img" aria-label="Chart" />;
}

export default GradeChart;
