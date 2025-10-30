import { Link } from 'react-router-dom';
import { Facebook, Instagram, Phone, Mail, MapPin } from 'lucide-react';

const LOGO_URL = 'https://customer-assets.emergentagent.com/job_spice-harbor-1/artifacts/j7td7vej_WhatsApp_Image_2025-10-21_at_11.56.02__1_-removebg-preview.png';

const Footer = () => {
  return (
    <footer className="bg-black text-white pt-12 pb-6" data-testid="footer">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* Logo & Description */}
          <div>
            <Link to="/" className="inline-block mb-4">
              <img 
                src={LOGO_URL} 
                alt="Lakeside Indian Restaurant" 
                className="h-16 w-auto"
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60"%3E%3Ctext x="10" y="40" font-family="Arial" font-size="24" fill="%23DC2626" font-weight="bold"%3ELakeside%3C/text%3E%3C/svg%3E';
                }}
              />
            </Link>
            <p className="text-gray-400">
              Experience authentic Indian cuisine with a modern twist. Located by the beautiful lakeside, we serve traditional recipes passed down through generations.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-xl font-bold mb-4 text-red-600">Quick Links</h4>
            <ul className="space-y-2">
              <li><Link to="/" className="text-gray-400 hover:text-red-600 transition-colors">Home</Link></li>
              <li><Link to="/about" className="text-gray-400 hover:text-red-600 transition-colors">About Us</Link></li>
              <li><Link to="/menu/dine-in" className="text-gray-400 hover:text-red-600 transition-colors">Dine-in Menu</Link></li>
              <li><Link to="/menu/takeaway" className="text-gray-400 hover:text-red-600 transition-colors">Takeaway Menu</Link></li>
              <li><Link to="/gallery" className="text-gray-400 hover:text-red-600 transition-colors">Gallery</Link></li>
              <li><Link to="/contact" className="text-gray-400 hover:text-red-600 transition-colors">Contact Us</Link></li>
              <li><Link to="/reservation" className="text-gray-400 hover:text-red-600 transition-colors">Reservation</Link></li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-xl font-bold mb-4 text-red-600">Contact Info</h4>
            <ul className="space-y-3">
              <li className="flex items-start text-gray-400">
                <MapPin className="w-5 h-5 mr-2 text-red-600 flex-shrink-0 mt-1" />
                <span>94 Belmore Street Yarrawonga 3730</span>
              </li>
              <li className="flex items-center text-gray-400">
                <Phone className="w-5 h-5 mr-2 text-red-600" />
                <a href="tel:+61397493400" className="hover:text-red-600 transition-colors">+61 3 9749 3400</a>
              </li>
              <li className="flex items-center text-gray-400">
                <Mail className="w-5 h-5 mr-2 text-red-600" />
                <a href="mailto:info@lakesiderestaurant.com" className="hover:text-red-600 transition-colors">info@lakesiderestaurant.com</a>
              </li>
            </ul>
            <div className="flex space-x-4 mt-4">
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-red-600 transition-colors">
                <Facebook className="w-6 h-6" />
              </a>
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-red-600 transition-colors">
                <Instagram className="w-6 h-6" />
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 pt-6 text-center text-gray-400">
          <p>&copy; {new Date().getFullYear()} Lakeside Indian Restaurant. All rights reserved.</p>
          <p className="mt-2 text-sm">
            Designed and Developed by{' '}
            <a 
              href="https://www.businesswebmedia.com/" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-red-600 hover:text-red-500 transition-colors"
            >
              Business Web Media
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
