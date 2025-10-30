import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ShoppingCart, Heart, Menu, X } from 'lucide-react';
import { useCart } from '@/context/CartContext';
import { useWishlist } from '@/context/WishlistContext';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const DEFAULT_LOGO = 'https://customer-assets.emergentagent.com/job_spice-harbor-1/artifacts/j7td7vej_WhatsApp_Image_2025-10-21_at_11.56.02__1_-removebg-preview.png';

const Header = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [headerLogo, setHeaderLogo] = useState(DEFAULT_LOGO);
  const location = useLocation();
  const { getCartItemCount } = useCart();
  const { wishlist } = useWishlist();

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get(`${API}/settings`);
      if (response.data.header_logo) {
        const logoUrl = response.data.header_logo.startsWith('http') 
          ? response.data.header_logo 
          : `${BACKEND_URL}${response.data.header_logo.startsWith('/api/') ? response.data.header_logo : '/api' + response.data.header_logo}`;
        setHeaderLogo(logoUrl);
      }
    } catch (error) {
      console.error('Error fetching settings:', error);
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-black shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center">
            <img 
              src={headerLogo} 
              alt="Lakeside Indian Restaurant" 
              className="h-16 w-auto"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = DEFAULT_LOGO;
              }}
            />
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center space-x-6">
            <NavLink to="/" active={location.pathname === '/'}>Home</NavLink>
            <NavLink to="/about" active={location.pathname === '/about'}>About Us</NavLink>
            <NavLink to="/menu/dine-in" active={location.pathname === '/menu/dine-in'}>Our Menu</NavLink>
            <NavLink to="/gallery" active={location.pathname === '/gallery'}>Gallery</NavLink>
            <NavLink to="/contact" active={location.pathname === '/contact'}>Contact Us</NavLink>
            <NavLink to="/reservation" active={location.pathname === '/reservation'}>Reservation</NavLink>
          </nav>

          {/* Order Online Button - Hidden on takeaway page */}
          {location.pathname !== '/menu/takeaway' && (
            <div className="hidden lg:flex items-center">
              <Link 
                to="/menu/takeaway" 
                className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors"
              >
                Order Online
              </Link>
            </div>
          )}

          {/* Mobile Menu Button */}
          <button
            className="lg:hidden text-white"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            data-testid="mobile-menu-button"
          >
            {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="lg:hidden py-4 border-t border-gray-700" data-testid="mobile-menu">
            <nav className="flex flex-col space-y-4">
              <MobileNavLink to="/" onClick={() => setIsMobileMenuOpen(false)}>Home</MobileNavLink>
              <MobileNavLink to="/about" onClick={() => setIsMobileMenuOpen(false)}>About Us</MobileNavLink>
              <MobileNavLink to="/menu/dine-in" onClick={() => setIsMobileMenuOpen(false)}>Our Menu</MobileNavLink>
              <MobileNavLink to="/gallery" onClick={() => setIsMobileMenuOpen(false)}>Gallery</MobileNavLink>
              <MobileNavLink to="/contact" onClick={() => setIsMobileMenuOpen(false)}>Contact Us</MobileNavLink>
              <MobileNavLink to="/reservation" onClick={() => setIsMobileMenuOpen(false)}>Reservation</MobileNavLink>
              
              <Link 
                to="/menu/takeaway" 
                className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors text-center mt-4"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Order Online
              </Link>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

const NavLink = ({ to, children, active }) => (
  <Link
    to={to}
    className={`text-white hover:text-red-600 transition-colors font-medium ${
      active ? 'text-red-600' : ''
    }`}
  >
    {children}
  </Link>
);

const MobileNavLink = ({ to, children, onClick }) => (
  <Link
    to={to}
    onClick={onClick}
    className="text-white hover:text-red-600 transition-colors font-medium"
  >
    {children}
  </Link>
);

export default Header;
