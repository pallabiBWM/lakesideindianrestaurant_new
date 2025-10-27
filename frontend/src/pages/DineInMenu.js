import { useState, useEffect } from 'react';
import axios from 'axios';
import { ShoppingCart, Heart } from 'lucide-react';
import { useCart } from '@/context/CartContext';
import { useWishlist } from '@/context/WishlistContext';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const DineInMenu = () => {
  const [menuItems, setMenuItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [loading, setLoading] = useState(true);
  const { addToCart } = useCart();
  const { addToWishlist, isInWishlist, removeFromWishlist } = useWishlist();

  useEffect(() => {
    fetchMenuItems();
    fetchCategories();
  }, []);

  const fetchMenuItems = async () => {
    try {
      const response = await axios.get(`${API}/menu?menu_type=dine-in`);
      setMenuItems(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching menu items:', error);
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API}/categories?menu_type=dine-in`);
      setCategories(['All', ...response.data.categories]);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const filteredItems = selectedCategory === 'All'
    ? menuItems
    : menuItems.filter(item => item.category === selectedCategory);

  const handleAddToCart = (itemId) => {
    addToCart(itemId, 1);
  };

  const handleWishlistToggle = (itemId) => {
    if (isInWishlist(itemId)) {
      removeFromWishlist(itemId);
    } else {
      addToWishlist(itemId);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-2xl font-semibold">Loading menu...</div>
      </div>
    );
  }

  return (
    <div className="bg-white min-h-screen">
      {/* Banner */}
      <section
        className="relative h-96 bg-cover bg-center"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1589302168068-964664d93dc0)'
        }}
        data-testid="dinein-menu-banner"
      >
        <div className="absolute inset-0 bg-black bg-opacity-60"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-4" data-testid="dinein-menu-title">
              Dine-in <span className="text-red-600">Menu</span>
            </h1>
            <p className="text-xl text-white">Experience our authentic Indian cuisine in-house</p>
          </div>
        </div>
      </section>

      {/* Category Filter */}
      <section className="py-8 px-4 bg-gray-50 sticky top-20 z-40 shadow-md" data-testid="category-filter">
        <div className="container mx-auto">
          <div className="flex flex-wrap justify-center gap-4">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-6 py-2 rounded-lg font-semibold transition-colors ${
                  selectedCategory === category
                    ? 'bg-red-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-200'
                }`}
                data-testid={`category-${category.toLowerCase().replace(/ /g, '-')}`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Menu Items Grid */}
      <section className="py-16 px-4">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
            {filteredItems.map((item) => (
              <div
                key={item.id}
                className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
                data-testid={`menu-item-${item.id}`}
              >
                <div className="p-6">
                  <div className="mb-2 flex items-center justify-between">
                    <span className="text-xs font-semibold text-red-600 bg-red-50 px-2 py-1 rounded">
                      {item.category}
                    </span>
                    <button
                      onClick={() => handleWishlistToggle(item.id)}
                      className="text-gray-400 hover:text-red-600 transition-colors"
                      data-testid={`wishlist-toggle-${item.id}`}
                    >
                      <Heart
                        className={`w-5 h-5 ${
                          isInWishlist(item.id) ? 'fill-red-600 text-red-600' : ''
                        }`}
                      />
                    </button>
                  </div>
                  <h3 className="text-xl font-bold mb-2">{item.name}</h3>
                  <p className="text-gray-600 mb-4 text-sm">{item.description}</p>
                  <div className="flex items-center justify-between">
                    <p className="text-2xl font-bold text-red-600">${item.price.toFixed(2)}</p>
                    <button
                      onClick={() => handleAddToCart(item.id)}
                      className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
                      data-testid={`add-to-cart-${item.id}`}
                    >
                      <ShoppingCart className="w-4 h-4" />
                      <span>Add</span>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredItems.length === 0 && (
            <div className="text-center py-12">
              <p className="text-xl text-gray-600">No items found in this category.</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default DineInMenu;
