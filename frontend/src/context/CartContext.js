import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const CartContext = createContext();

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Generate a simple user ID for demo purposes
const USER_ID = 'demo-user-' + (localStorage.getItem('userId') || Date.now());
localStorage.setItem('userId', USER_ID);

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState({ items: [] });
  const [loading, setLoading] = useState(false);

  const fetchCart = async () => {
    try {
      const response = await axios.get(`${API}/cart/${USER_ID}`);
      setCart(response.data);
    } catch (error) {
      console.error('Error fetching cart:', error);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const addToCart = async (menuItemId, quantity = 1) => {
    setLoading(true);
    try {
      await axios.post(`${API}/cart/${USER_ID}/add`, {
        menu_item_id: menuItemId,
        quantity: quantity
      });
      await fetchCart();
    } catch (error) {
      console.error('Error adding to cart:', error);
    }
    setLoading(false);
  };

  const removeFromCart = async (menuItemId) => {
    setLoading(true);
    try {
      await axios.delete(`${API}/cart/${USER_ID}/remove/${menuItemId}`);
      await fetchCart();
    } catch (error) {
      console.error('Error removing from cart:', error);
    }
    setLoading(false);
  };

  const clearCart = async () => {
    setLoading(true);
    try {
      await axios.delete(`${API}/cart/${USER_ID}/clear`);
      await fetchCart();
    } catch (error) {
      console.error('Error clearing cart:', error);
    }
    setLoading(false);
  };

  const getCartItemCount = () => {
    return cart.items.reduce((sum, item) => sum + item.quantity, 0);
  };

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart, clearCart, getCartItemCount, loading }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within CartProvider');
  }
  return context;
};
