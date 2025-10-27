import '@/App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
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

// Admin imports
import { AdminAuthProvider } from '@/context/AdminAuthContext';
import AdminLogin from '@/pages/admin/AdminLogin';
import AdminDashboard from '@/pages/admin/AdminDashboard';
import AdminContacts from '@/pages/admin/AdminContacts';
import AdminReservations from '@/pages/admin/AdminReservations';
import AdminSettings from '@/pages/admin/AdminSettings';
import AdminLayout from '@/components/AdminLayout';
import ProtectedRoute from '@/components/ProtectedRoute';

function App() {
  return (
    <div className="App">
      <AdminAuthProvider>
        <CartProvider>
          <WishlistProvider>
            <BrowserRouter>
              <Routes>
                {/* Public Routes */}
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

                {/* Admin Routes */}
                <Route path="/admin/login" element={<AdminLogin />} />
                <Route
                  path="/admin/*"
                  element={
                    <ProtectedRoute>
                      <AdminLayout>
                        <Routes>
                          <Route path="dashboard" element={<AdminDashboard />} />
                          <Route path="contacts" element={<AdminContacts />} />
                          <Route path="reservations" element={<AdminReservations />} />
                          <Route path="settings" element={<AdminSettings />} />
                          <Route path="*" element={<Navigate to="/admin/dashboard" replace />} />
                        </Routes>
                      </AdminLayout>
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </BrowserRouter>
          </WishlistProvider>
        </CartProvider>
      </AdminAuthProvider>
    </div>
  );
}

export default App;
