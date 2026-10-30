import React from 'react';

export function Button({ children, variant = 'primary', className = '', ...props }) {
  const baseStyle = "btn-primary"; // Defined in index.css
  const variantStyle = variant === 'secondary' ? 'btn-secondary' : baseStyle;
  
  return (
    <button className={`${variantStyle} ${className}`} {...props}>
      {children}
    </button>
  );
}
