import { useState, useEffect } from 'react';
import { useAdminAuth } from '@/context/AdminAuthContext';
import axios from 'axios';
import { Users, MessageSquare, Calendar, ShoppingBag } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminDashboard = () => {
  const { token } = useAdminAuth();
  const [stats, setStats] = useState({
    contacts: 0,
    reservations: 0,
    menuItems: 0,
    testimonials: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      
      const [contacts, reservations, menu, testimonials] = await Promise.all([
        axios.get(`${API}/admin/contacts`, { headers }),
        axios.get(`${API}/admin/reservations`, { headers }),
        axios.get(`${API}/menu`),
        axios.get(`${API}/testimonials`)
      ]);

      setStats({
        contacts: contacts.data.length,
        reservations: reservations.data.length,
        menuItems: menu.data.length,
        testimonials: testimonials.data.length
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
    setLoading(false);
  };

  const statCards = [
    { label: 'Contact Forms', value: stats.contacts, icon: MessageSquare, color: 'bg-blue-500' },
    { label: 'Reservations', value: stats.reservations, icon: Calendar, color: 'bg-green-500' },
    { label: 'Menu Items', value: stats.menuItems, icon: ShoppingBag, color: 'bg-purple-500' },
    { label: 'Testimonials', value: stats.testimonials, icon: Users, color: 'bg-orange-500' },
  ];

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm mb-1">{stat.label}</p>
                  <p className="text-3xl font-bold text-gray-800">{stat.value}</p>
                </div>
                <div className={`${stat.color} p-4 rounded-lg`}>
                  <Icon className="w-8 h-8 text-white" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Welcome Message */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Welcome to Admin Panel</h2>
        <p className="text-gray-600 mb-4">
          Manage your restaurant's content, view customer inquiries, and update menu items all from this dashboard.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="border-l-4 border-red-600 pl-4">
            <h3 className="font-semibold text-gray-800 mb-2">Quick Actions</h3>
            <ul className="space-y-1 text-sm text-gray-600">
              <li>• View and respond to customer contacts</li>
              <li>• Manage table reservations</li>
              <li>• Add or update menu items</li>
              <li>• Update restaurant settings</li>
            </ul>
          </div>
          <div className="border-l-4 border-red-600 pl-4">
            <h3 className="font-semibold text-gray-800 mb-2">Current Status</h3>
            <ul className="space-y-1 text-sm text-gray-600">
              <li>• Total Menu Items: {stats.menuItems}</li>
              <li>• Pending Contacts: {stats.contacts}</li>
              <li>• Reservations: {stats.reservations}</li>
              <li>• Customer Reviews: {stats.testimonials}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
