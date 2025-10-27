import { useState, useEffect } from 'react';
import { useAdminAuth } from '@/context/AdminAuthContext';
import axios from 'axios';
import { Calendar as CalendarIcon, User, Mail, Phone, Users, MessageSquare } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminReservations = () => {
  const { token } = useAdminAuth();
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReservations();
  }, []);

  const fetchReservations = async () => {
    try {
      const response = await axios.get(`${API}/admin/reservations`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setReservations(response.data);
    } catch (error) {
      console.error('Error fetching reservations:', error);
    }
    setLoading(false);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Table Reservations</h1>

      <div className="grid grid-cols-1 gap-6">
        {reservations.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-8 text-center text-gray-500">
            <CalendarIcon className="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <p>No reservations yet</p>
          </div>
        ) : (
          reservations.map((reservation) => (
            <div key={reservation.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Customer Info */}
                <div>
                  <h3 className="font-bold text-lg text-gray-800 mb-4">Customer Information</h3>
                  <div className="space-y-3">
                    <div className="flex items-center">
                      <User className="w-5 h-5 mr-3 text-gray-400" />
                      <span className="font-medium text-gray-800">{reservation.name}</span>
                    </div>
                    <div className="flex items-center">
                      <Mail className="w-5 h-5 mr-3 text-gray-400" />
                      <a href={`mailto:${reservation.email}`} className="text-gray-600 hover:text-red-600">
                        {reservation.email}
                      </a>
                    </div>
                    <div className="flex items-center">
                      <Phone className="w-5 h-5 mr-3 text-gray-400" />
                      <a href={`tel:${reservation.phone}`} className="text-gray-600 hover:text-red-600">
                        {reservation.phone}
                      </a>
                    </div>
                  </div>
                </div>

                {/* Reservation Details */}
                <div>
                  <h3 className="font-bold text-lg text-gray-800 mb-4">Reservation Details</h3>
                  <div className="space-y-3">
                    <div className="flex items-center">
                      <CalendarIcon className="w-5 h-5 mr-3 text-gray-400" />
                      <span className="text-gray-600">{reservation.date}</span>
                    </div>
                    <div className="flex items-center">
                      <CalendarIcon className="w-5 h-5 mr-3 text-gray-400" />
                      <span className="text-gray-600">{reservation.time}</span>
                    </div>
                    <div className="flex items-center">
                      <Users className="w-5 h-5 mr-3 text-gray-400" />
                      <span className="text-gray-600">{reservation.guests} guests</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Special Requests */}
              {reservation.special_requests && (
                <div className="mt-6 pt-6 border-t border-gray-200">
                  <div className="flex items-start">
                    <MessageSquare className="w-5 h-5 mr-3 text-gray-400 mt-1" />
                    <div>
                      <h4 className="font-semibold text-gray-800 mb-1">Special Requests</h4>
                      <p className="text-gray-600">{reservation.special_requests}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Submitted Date */}
              <div className="mt-4 text-sm text-gray-500">
                Submitted: {new Date(reservation.created_at).toLocaleString()}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default AdminReservations;
