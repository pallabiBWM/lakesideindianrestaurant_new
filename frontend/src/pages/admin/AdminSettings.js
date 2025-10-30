import { useState, useEffect } from 'react';
import { useAdminAuth } from '@/context/AdminAuthContext';
import axios from 'axios';
import { Save, Mail, Phone, MapPin, Clock, Upload } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminSettings = () => {
  const { token } = useAdminAuth();
  const [settings, setSettings] = useState({
    admin_email: '',
    restaurant_name: '',
    restaurant_phone: '',
    restaurant_address: '',
    header_logo: '',
    footer_logo: '',
    opening_hours: {
      monday_thursday: '',
      friday_saturday: '',
      sunday: ''
    }
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [uploading, setUploading] = useState({ header: false, footer: false });
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get(`${API}/admin/settings`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSettings(response.data);
    } catch (error) {
      console.error('Error fetching settings:', error);
    }
    setLoading(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');

    try {
      await axios.put(`${API}/admin/settings`, settings, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessage('Settings saved successfully!');
    } catch (error) {
      setMessage('Error saving settings. Please try again.');
      console.error('Error saving settings:', error);
    }
    setSaving(false);
  };

  const handleChange = (field, value) => {
    setSettings(prev => ({ ...prev, [field]: value }));
  };

  const handleHoursChange = (day, value) => {
    setSettings(prev => ({
      ...prev,
      opening_hours: { ...prev.opening_hours, [day]: value }
    }));
  };

  const handleLogoUpload = async (e, logoType) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(prev => ({ ...prev, [logoType]: true }));
    setMessage('');

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('logo_type', logoType);

      const response = await axios.post(`${API}/admin/settings/upload-logo?logo_type=${logoType}`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      // Update settings with new logo URL
      const logoField = `${logoType}_logo`;
      setSettings(prev => ({ ...prev, [logoField]: response.data.url }));
      setMessage(`${logoType.charAt(0).toUpperCase() + logoType.slice(1)} logo uploaded successfully!`);
    } catch (error) {
      setMessage(`Error uploading ${logoType} logo. Please try again.`);
      console.error(`Error uploading ${logoType} logo:`, error);
    } finally {
      setUploading(prev => ({ ...prev, [logoType]: false }));
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Restaurant Settings</h1>

      {message && (
        <div className={`mb-6 p-4 rounded-lg ${
          message.includes('successfully') 
            ? 'bg-green-100 text-green-700 border border-green-400' 
            : 'bg-red-100 text-red-700 border border-red-400'
        }`}>
          {message}
        </div>
      )}

      <div className="bg-white rounded-lg shadow-md p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Admin Email */}
          <div>
            <label className="flex items-center text-sm font-semibold text-gray-700 mb-2">
              <Mail className="w-4 h-4 mr-2" />
              Admin Email (for notifications)
            </label>
            <input
              type="email"
              value={settings.admin_email}
              onChange={(e) => handleChange('admin_email', e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
              required
            />
            <p className="text-xs text-gray-500 mt-1">Contact forms and reservations will be sent to this email</p>
          </div>

          {/* Restaurant Name */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Restaurant Name
            </label>
            <input
              type="text"
              value={settings.restaurant_name}
              onChange={(e) => handleChange('restaurant_name', e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
              required
            />
          </div>

          {/* Phone */}
          <div>
            <label className="flex items-center text-sm font-semibold text-gray-700 mb-2">
              <Phone className="w-4 h-4 mr-2" />
              Phone Number
            </label>
            <input
              type="tel"
              value={settings.restaurant_phone}
              onChange={(e) => handleChange('restaurant_phone', e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
              required
            />
          </div>

          {/* Address */}
          <div>
            <label className="flex items-center text-sm font-semibold text-gray-700 mb-2">
              <MapPin className="w-4 h-4 mr-2" />
              Address
            </label>
            <textarea
              value={settings.restaurant_address}
              onChange={(e) => handleChange('restaurant_address', e.target.value)}
              rows="2"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
              required
            ></textarea>
          </div>

          {/* Opening Hours */}
          <div>
            <label className="flex items-center text-sm font-semibold text-gray-700 mb-4">
              <Clock className="w-4 h-4 mr-2" />
              Opening Hours
            </label>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-600 mb-1">Monday - Thursday</label>
                <input
                  type="text"
                  value={settings.opening_hours.monday_thursday}
                  onChange={(e) => handleHoursChange('monday_thursday', e.target.value)}
                  placeholder="e.g., 5:00 PM - 10:00 PM"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Friday - Saturday</label>
                <input
                  type="text"
                  value={settings.opening_hours.friday_saturday}
                  onChange={(e) => handleHoursChange('friday_saturday', e.target.value)}
                  placeholder="e.g., 5:00 PM - 10:30 PM"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-1">Sunday</label>
                <input
                  type="text"
                  value={settings.opening_hours.sunday}
                  onChange={(e) => handleHoursChange('sunday', e.target.value)}
                  placeholder="e.g., 5:00 PM - 10:00 PM"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-600"
                />
              </div>
            </div>
          </div>

          {/* Save Button */}
          <div className="flex justify-end pt-6 border-t">
            <button
              type="submit"
              disabled={saving}
              className="flex items-center bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors disabled:opacity-50"
            >
              <Save className="w-5 h-5 mr-2" />
              {saving ? 'Saving...' : 'Save Settings'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AdminSettings;
