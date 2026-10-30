import React from 'react';

export function ProgressBar({ label, score, colorClass = '' }) {
  return (
    <div className="stat-bar">
      <div className="stat-bar-header">
        <span>{label}</span>
        <span>{score}%</span>
      </div>
      <div className="bar-bg">
        <div className={`bar-fill ${colorClass}`} style={{ width: `${score}%` }}></div>
      </div>
    </div>
  );
}
