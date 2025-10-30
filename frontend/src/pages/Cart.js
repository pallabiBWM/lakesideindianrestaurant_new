import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Trash2, ShoppingBag, Plus, Minus } from 'lucide-react';
import axios from 'axios';
import { useCart } from '@/context/CartContext';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Cart = () => {
  const { cart, removeFromCart, clearCart, updateQuantity } = useCart();
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMenuItems();
  }, [cart.items.length]); // Re-fetch when cart items change

  const fetchMenuItems = async () => {
    if (cart.items.length === 0) {
      setLoading(false);
      return;
    }

    try {
      const response = await axios.get(`${API}/menu`);
      const allItems = response.data;
      const cartItemIds = cart.items.map(item => item.menu_item_id);
      const cartMenuItems = allItems.filter(item => cartItemIds.includes(item.id));
      setMenuItems(cartMenuItems);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching menu items:', error);
      setLoading(false);
    }
  };

  const getItemQuantity = (itemId) => {
    const cartItem = cart.items.find(item => item.menu_item_id === itemId);
    return cartItem ? cartItem.quantity : 0;
  };

  const calculateSubtotal = (item) => {
    return item.price * getItemQuantity(item.id);
  };

  const calculateTotal = () => {
    return menuItems.reduce((total, item) => total + calculateSubtotal(item), 0);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-2xl font-semibold">Loading cart...</div>
      </div>
    );
  }

  return (
    <div className="bg-gray-50 min-h-screen py-8 px-4">
      <div className="container mx-auto max-w-6xl">
        <h1 className="text-4xl font-bold mb-8" data-testid="cart-title">
          Shopping <span className="text-red-600">Cart</span>
        </h1>

        {cart.items.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center" data-testid="empty-cart">
            <ShoppingBag className="w-24 h-24 text-gray-300 mx-auto mb-6" />
            <h2 className="text-2xl font-bold mb-4">Your cart is empty</h2>
            <p className="text-gray-600 mb-6">Add some delicious dishes to your cart!</p>
            <Link
              to="/menu/takeaway"
              className="bg-red-600 hover:bg-red-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors inline-block"
              data-testid="browse-menu-link"
            >
              Browse Menu
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Cart Items */}
            <div className="lg:col-span-2 space-y-4">
              {menuItems.map((item) => (
                <div
                  key={item.id}
                  className="bg-white rounded-lg shadow-md p-6 flex items-center space-x-6"
                  data-testid={`cart-item-${item.id}`}
                >
                  <div className="flex-grow">
                    <h3 className="text-xl font-bold mb-2">{item.name}</h3>
                    <p className="text-gray-600 text-sm mb-2">{item.category}</p>
                    <p className="text-lg font-semibold text-red-600">${item.price.toFixed(2)}</p>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <button
                      onClick={() => updateQuantity(item.id, getItemQuantity(item.id) - 1)}
                      className="bg-gray-200 hover:bg-gray-300 p-2 rounded-lg transition-colors"
                      data-testid={`decrease-quantity-${item.id}`}
                    >
                      <Minus className="w-4 h-4" />
                    </button>
                    <span className="text-2xl font-bold w-12 text-center">{getItemQuantity(item.id)}</span>
                    <button
                      onClick={() => updateQuantity(item.id, getItemQuantity(item.id) + 1)}
                      className="bg-gray-200 hover:bg-gray-300 p-2 rounded-lg transition-colors"
                      data-testid={`increase-quantity-${item.id}`}
                    >
                      <Plus className="w-4 h-4" />
                    </button>
                  </div>
                  
                  <div className="text-right">
                    <p className="text-sm text-gray-600 mb-2">Subtotal</p>
                    <p className="text-2xl font-bold text-red-600">${calculateSubtotal(item).toFixed(2)}</p>
                  </div>
                  
                  <button
                    onClick={() => removeFromCart(item.id)}
                    className="text-red-600 hover:text-red-700 transition-colors"
                    data-testid={`remove-item-${item.id}`}
                  >
                    <Trash2 className="w-6 h-6" />
                  </button>
                </div>
              ))}

              <button
                onClick={clearCart}
                className="text-red-600 hover:text-red-700 font-semibold transition-colors"
                data-testid="clear-cart-button"
              >
                Clear Cart
              </button>
            </div>

            {/* Order Summary */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-md p-6 sticky top-24" data-testid="order-summary">
                <h2 className="text-2xl font-bold mb-6">Order Summary</h2>
                <div className="space-y-4 mb-6">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Subtotal</span>
                    <span className="font-semibold">${calculateTotal().toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Tax (8%)</span>
                    <span className="font-semibold">${(calculateTotal() * 0.08).toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Delivery Fee</span>
                    <span className="font-semibold">$5.00</span>
                  </div>
                  <div className="border-t pt-4">
                    <div className="flex justify-between text-xl font-bold">
                      <span>Total</span>
                      <span className="text-red-600">${(calculateTotal() * 1.08 + 5).toFixed(2)}</span>
                    </div>
                  </div>
                </div>
                <div className="space-y-3">
                  <button
                    onClick={() => navigate('/checkout')}
                    className="w-full bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
                    data-testid="checkout-button"
                  >
                    Proceed to Checkout
                  </button>
                  <p className="text-center text-sm text-gray-500">
                    Payment integration coming soon!
                  </p>
                  <Link
                    to="/menu/takeaway"
                    className="block w-full text-center border-2 border-red-600 text-red-600 hover:bg-red-50 px-6 py-3 rounded-lg font-semibold transition-colors"
                    data-testid="continue-shopping-link"
                  >
                    Continue Shopping
                  </Link>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Cart;
