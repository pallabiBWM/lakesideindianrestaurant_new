import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const WishlistContext = createContext();

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const USER_ID = 'demo-user-' + (localStorage.getItem('userId') || Date.now());

export const WishlistProvider = ({ children }) => {
  const [wishlist, setWishlist] = useState({ menu_item_ids: [] });
  const [loading, setLoading] = useState(false);

  const fetchWishlist = async () => {
    try {
      const response = await axios.get(`${API}/wishlist/${USER_ID}`);
      setWishlist(response.data);
    } catch (error) {
      console.error('Error fetching wishlist:', error);
    }
  };

  useEffect(() => {
    fetchWishlist();
  }, []);

  const addToWishlist = async (menuItemId) => {
    setLoading(true);
    try {
      await axios.post(`${API}/wishlist/${USER_ID}/add/${menuItemId}`);
      await fetchWishlist();
    } catch (error) {
      console.error('Error adding to wishlist:', error);
    }
    setLoading(false);
  };

  const removeFromWishlist = async (menuItemId) => {
    setLoading(true);
    try {
      await axios.delete(`${API}/wishlist/${USER_ID}/remove/${menuItemId}`);
      await fetchWishlist();
    } catch (error) {
      console.error('Error removing from wishlist:', error);
    }
    setLoading(false);
  };

  const isInWishlist = (menuItemId) => {
    return wishlist.menu_item_ids.includes(menuItemId);
  };

  return (
    <WishlistContext.Provider value={{ wishlist, addToWishlist, removeFromWishlist, isInWishlist, loading }}>
      {children}
    </WishlistContext.Provider>
  );
};

export const useWishlist = () => {
  const context = useContext(WishlistContext);
  if (!context) {
    throw new Error('useWishlist must be used within WishlistProvider');
  }
  return context;
};
