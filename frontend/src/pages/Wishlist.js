import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Heart, ShoppingCart, Trash2 } from 'lucide-react';
import axios from 'axios';
import { useWishlist } from '@/context/WishlistContext';
import { useCart } from '@/context/CartContext';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Wishlist = () => {
  const { wishlist, removeFromWishlist } = useWishlist();
  const { addToCart } = useCart();
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMenuItems();
  }, [wishlist]);

  const fetchMenuItems = async () => {
    if (wishlist.menu_item_ids.length === 0) {
      setLoading(false);
      return;
    }

    try {
      const response = await axios.get(`${API}/menu`);
      const allItems = response.data;
      const wishlistItems = allItems.filter(item => wishlist.menu_item_ids.includes(item.id));
      setMenuItems(wishlistItems);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching menu items:', error);
      setLoading(false);
    }
  };

  const handleAddToCart = (itemId) => {
    addToCart(itemId, 1);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-2xl font-semibold">Loading wishlist...</div>
      </div>
    );
  }

  return (
    <div className="bg-gray-50 min-h-screen py-8 px-4">
      <div className="container mx-auto max-w-6xl">
        <h1 className="text-4xl font-bold mb-8" data-testid="wishlist-title">
          My <span className="text-red-600">Wishlist</span>
        </h1>

        {wishlist.menu_item_ids.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center" data-testid="empty-wishlist">
            <Heart className="w-24 h-24 text-gray-300 mx-auto mb-6" />
            <h2 className="text-2xl font-bold mb-4">Your wishlist is empty</h2>
            <p className="text-gray-600 mb-6">Save your favorite dishes for later!</p>
            <Link
              to="/menu"
              className="bg-red-600 hover:bg-red-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors inline-block"
              data-testid="browse-menu-wishlist-link"
            >
              Browse Menu
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {menuItems.map((item) => (
              <div
                key={item.id}
                className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
                data-testid={`wishlist-item-${item.id}`}
              >
                <div className="relative">
                  <img src={item.image} alt={item.name} className="w-full h-48 object-cover" />
                  <button
                    onClick={() => removeFromWishlist(item.id)}
                    className="absolute top-2 right-2 bg-white rounded-full p-2 hover:bg-gray-100 transition-colors"
                    data-testid={`remove-wishlist-${item.id}`}
                  >
                    <Trash2 className="w-5 h-5 text-red-600" />
                  </button>
                </div>
                <div className="p-6">
                  <div className="mb-2">
                    <span className="text-xs font-semibold text-red-600 bg-red-50 px-2 py-1 rounded">
                      {item.category}
                    </span>
                  </div>
                  <h3 className="text-xl font-bold mb-2">{item.name}</h3>
                  <p className="text-gray-600 mb-4 text-sm line-clamp-2">{item.description}</p>
                  <div className="flex items-center justify-between">
                    <p className="text-2xl font-bold text-red-600">${item.price.toFixed(2)}</p>
                    <button
                      onClick={() => handleAddToCart(item.id)}
                      className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
                      data-testid={`add-to-cart-wishlist-${item.id}`}
                    >
                      <ShoppingCart className="w-4 h-4" />
                      <span>Add to Cart</span>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Wishlist;
