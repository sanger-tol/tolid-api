import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders home page link', () => {
  render(<App />);
  const linkElement = screen.getByText(/ToLID/i);
  expect(linkElement).toBeInTheDocument();
});
