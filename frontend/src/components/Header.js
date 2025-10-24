import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ShoppingCart, Heart, Menu, X } from 'lucide-react';
import { useCart } from '@/context/CartContext';
import { useWishlist } from '@/context/WishlistContext';

const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();
  const isHomePage = location.pathname === '/';
  const { getCartItemCount } = useCart();
  const { wishlist } = useWishlist();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const headerBg = isHomePage && !isScrolled ? 'bg-transparent' : 'bg-black';
  const headerShadow = isScrolled ? 'shadow-lg' : '';

  return (
    <header className={`sticky top-0 z-50 transition-all duration-300 ${headerBg} ${headerShadow}`}>
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <Link to="/" className="text-2xl md:text-3xl font-bold text-white hover:text-red-600 transition-colors">
            <span className="text-red-600">Lakeside</span> Indian Restaurant
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center space-x-8">
            <NavLink to="/" active={location.pathname === '/'}>Home</NavLink>
            <NavLink to="/about" active={location.pathname === '/about'}>About Us</NavLink>
            <NavLink to="/menu" active={location.pathname === '/menu'}>Menu</NavLink>
            <NavLink to="/gallery" active={location.pathname === '/gallery'}>Gallery</NavLink>
            <NavLink to="/contact" active={location.pathname === '/contact'}>Contact Us</NavLink>
            <NavLink to="/reservation" active={location.pathname === '/reservation'}>Reservation</NavLink>
          </nav>

          {/* Cart & Wishlist Icons */}
          <div className="hidden lg:flex items-center space-x-6">
            <Link to="/wishlist" className="relative text-white hover:text-red-600 transition-colors" data-testid="wishlist-icon">
              <Heart className="w-6 h-6" />
              {wishlist.menu_item_ids.length > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center" data-testid="wishlist-count">
                  {wishlist.menu_item_ids.length}
                </span>
              )}
            </Link>
            <Link to="/cart" className="relative text-white hover:text-red-600 transition-colors" data-testid="cart-icon">
              <ShoppingCart className="w-6 h-6" />
              {getCartItemCount() > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center" data-testid="cart-count">
                  {getCartItemCount()}
                </span>
              )}
            </Link>
          </div>

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
              <MobileNavLink to="/menu" onClick={() => setIsMobileMenuOpen(false)}>Menu</MobileNavLink>
              <MobileNavLink to="/gallery" onClick={() => setIsMobileMenuOpen(false)}>Gallery</MobileNavLink>
              <MobileNavLink to="/contact" onClick={() => setIsMobileMenuOpen(false)}>Contact Us</MobileNavLink>
              <MobileNavLink to="/reservation" onClick={() => setIsMobileMenuOpen(false)}>Reservation</MobileNavLink>
              <div className="flex space-x-6 pt-4">
                <Link to="/wishlist" className="flex items-center text-white hover:text-red-600 transition-colors" onClick={() => setIsMobileMenuOpen(false)}>
                  <Heart className="w-5 h-5 mr-2" />
                  Wishlist ({wishlist.menu_item_ids.length})
                </Link>
                <Link to="/cart" className="flex items-center text-white hover:text-red-600 transition-colors" onClick={() => setIsMobileMenuOpen(false)}>
                  <ShoppingCart className="w-5 h-5 mr-2" />
                  Cart ({getCartItemCount()})
                </Link>
              </div>
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
