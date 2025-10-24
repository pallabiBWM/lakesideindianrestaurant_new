import { useState } from 'react';
import axios from 'axios';
import { Calendar, Clock, Users } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Reservation = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    date: '',
    time: '',
    guests: 2,
    special_requests: ''
  });
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    try {
      await axios.post(`${API}/reservation`, formData);
      setSubmitted(true);
      setFormData({
        name: '',
        email: '',
        phone: '',
        date: '',
        time: '',
        guests: 2,
        special_requests: ''
      });
    } catch (err) {
      setError('Failed to submit the reservation. Please try again.');
      console.error('Error submitting reservation:', err);
    }
    setSubmitting(false);
  };

  return (
    <div className="bg-white min-h-screen">
      {/* Banner */}
      <section
        className="relative h-96 bg-cover bg-center"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1712488070215-d22e012314ae)'
        }}
        data-testid="reservation-banner"
      >
        <div className="absolute inset-0 bg-black bg-opacity-60"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white" data-testid="reservation-title">Reserve a <span className="text-red-600">Table</span></h1>
        </div>
      </section>

      {/* Reservation Form */}
      <section className="py-16 px-4">
        <div className="container mx-auto max-w-2xl">
          {submitted && (
            <div className="bg-green-100 border border-green-400 text-green-700 px-6 py-4 rounded-lg mb-8" data-testid="reservation-success">
              <h3 className="font-bold text-lg mb-2">Reservation Confirmed!</h3>
              <p>Thank you for your reservation. We'll send you a confirmation email shortly.</p>
            </div>
          )}
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-6 py-4 rounded-lg mb-8" data-testid="reservation-error">
              {error}
            </div>
          )}

          <div className="bg-white shadow-xl rounded-lg p-8">
            <h2 className="text-3xl font-bold mb-6 text-center">Book Your <span className="text-red-600">Table</span></h2>
            <form onSubmit={handleSubmit} className="space-y-6" data-testid="reservation-form">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="name" className="block text-gray-700 font-semibold mb-2">
                    Name *
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
                    data-testid="reservation-name-input"
                  />
                </div>
                <div>
                  <label htmlFor="email" className="block text-gray-700 font-semibold mb-2">
                    Email *
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
                    data-testid="reservation-email-input"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="phone" className="block text-gray-700 font-semibold mb-2">
                  Phone *
                </label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
                  data-testid="reservation-phone-input"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <label htmlFor="date" className="block text-gray-700 font-semibold mb-2">
                    <Calendar className="w-4 h-4 inline mr-2" />
                    Date *
                  </label>
                  <input
                    type="date"
                    id="date"
                    name="date"
                    value={formData.date}
                    onChange={handleChange}
                    required
                    min={new Date().toISOString().split('T')[0]}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
                    data-testid="reservation-date-input"
                  />
                </div>
                <div>
                  <label htmlFor="time" className="block text-gray-700 font-semibold mb-2">
                    <Clock className="w-4 h-4 inline mr-2" />
                    Time *
                  </label>
                  <select
                    id="time"
                    name="time"
                    value={formData.time}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
                    data-testid="reservation-time-input"
                  >
                    <option value="">Select time</option>
                    <option value="11:00 AM">11:00 AM</option>
                    <option value="11:30 AM">11:30 AM</option>
                    <option value="12:00 PM">12:00 PM</option>
                    <option value="12:30 PM">12:30 PM</option>
                    <option value="1:00 PM">1:00 PM</option>
                    <option value="1:30 PM">1:30 PM</option>
                    <option value="2:00 PM">2:00 PM</option>
                    <option value="5:00 PM">5:00 PM</option>
                    <option value="5:30 PM">5:30 PM</option>
                    <option value="6:00 PM">6:00 PM</option>
                    <option value="6:30 PM">6:30 PM</option>
                    <option value="7:00 PM">7:00 PM</option>
                    <option value="7:30 PM">7:30 PM</option>
                    <option value="8:00 PM">8:00 PM</option>
                    <option value="8:30 PM">8:30 PM</option>
                    <option value="9:00 PM">9:00 PM</option>
                    <option value="9:30 PM">9:30 PM</option>
                    <option value="10:00 PM">10:00 PM</option>
                  </select>
                </div>
                <div>
                  <label htmlFor="guests" className="block text-gray-700 font-semibold mb-2">
                    <Users className="w-4 h-4 inline mr-2" />
                    Guests *
                  </label>
                  <select
                    id="guests"
                    name="guests"
                    value={formData.guests}
                    onChange={handleChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
                    data-testid="reservation-guests-input"
                  >
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
                      <option key={num} value={num}>{num} {num === 1 ? 'Guest' : 'Guests'}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label htmlFor="special_requests" className="block text-gray-700 font-semibold mb-2">
                  Special Requests (Optional)
                </label>
                <textarea
                  id="special_requests"
                  name="special_requests"
                  value={formData.special_requests}
                  onChange={handleChange}
                  rows="4"
                  placeholder="Any dietary restrictions, allergies, or special occasions?"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
                  data-testid="reservation-requests-input"
                ></textarea>
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full bg-red-600 hover:bg-red-700 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-colors disabled:opacity-50"
                data-testid="reservation-submit-button"
              >
                {submitting ? 'Reserving...' : 'Reserve Table'}
              </button>
            </form>
          </div>

          {/* Information Box */}
          <div className="mt-8 bg-gray-50 p-6 rounded-lg">
            <h3 className="font-bold text-lg mb-4">Reservation Policy</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• Reservations are confirmed upon receipt of confirmation email</li>
              <li>• Please arrive within 15 minutes of your reservation time</li>
              <li>• For groups larger than 10, please call us directly</li>
              <li>• Cancellations should be made at least 2 hours in advance</li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Reservation;
