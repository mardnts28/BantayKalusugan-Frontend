import React from 'react';
import { renderToString } from 'react-dom/server';
import Dashboard from './src/Dashboard.jsx';

try {
  const output = renderToString(React.createElement(Dashboard));
  console.log('Render succeeded. Output length:', output.length);
} catch (err) {
  console.error('Render error:', err);
  process.exit(1);
}
