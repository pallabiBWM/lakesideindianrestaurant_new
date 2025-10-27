import '@/App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from '@/pages/Home';
import About from '@/pages/About';
import DineInMenu from '@/pages/DineInMenu';
import TakeawayMenu from '@/pages/TakeawayMenu';
import Gallery from '@/pages/Gallery';
import Contact from '@/pages/Contact';
import Reservation from '@/pages/Reservation';
import Cart from '@/pages/Cart';
import Wishlist from '@/pages/Wishlist';
import Layout from '@/components/Layout';
import { CartProvider } from '@/context/CartContext';
import { WishlistProvider } from '@/context/WishlistContext';

function App() {
  return (
    <div className="App">
      <CartProvider>
        <WishlistProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Layout />}>
                <Route index element={<Home />} />
                <Route path="about" element={<About />} />
                <Route path="menu/dine-in" element={<DineInMenu />} />
                <Route path="menu/takeaway" element={<TakeawayMenu />} />
                <Route path="gallery" element={<Gallery />} />
                <Route path="contact" element={<Contact />} />
                <Route path="reservation" element={<Reservation />} />
                <Route path="cart" element={<Cart />} />
                <Route path="wishlist" element={<Wishlist />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </WishlistProvider>
      </CartProvider>
    </div>
  );
}

export default App;
