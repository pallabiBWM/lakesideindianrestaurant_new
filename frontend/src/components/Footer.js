import { Link } from 'react-router-dom';
import { Facebook, Instagram, Phone, Mail, MapPin } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-black text-white pt-12 pb-6" data-testid="footer">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* Logo & Description */}
          <div>
            <h3 className="text-2xl font-bold mb-4">
              <span className="text-red-600">Lakeside</span> Indian Restaurant
            </h3>
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
              <li><Link to="/menu" className="text-gray-400 hover:text-red-600 transition-colors">Menu</Link></li>
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
                <span>123 Lakeside Drive, Waterfront District, City Name, State 12345</span>
              </li>
              <li className="flex items-center text-gray-400">
                <Phone className="w-5 h-5 mr-2 text-red-600" />
                <a href="tel:+15551234567" className="hover:text-red-600 transition-colors">+1 (555) 123-4567</a>
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
        </div>
      </div>
    </footer>
  );
};

export default Footer;
