import { useState, useEffect } from 'react';
import { useAdminAuth } from '@/context/AdminAuthContext';
import axios from 'axios';
import { Mail, Phone, User, MessageSquare, Calendar } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminContacts = () => {
  const { token } = useAdminAuth();
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchContacts();
  }, []);

  const fetchContacts = async () => {
    try {
      const response = await axios.get(`${API}/admin/contacts`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setContacts(response.data);
    } catch (error) {
      console.error('Error fetching contacts:', error);
    }
    setLoading(false);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Contact Form Submissions</h1>

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        {contacts.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <MessageSquare className="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <p>No contact submissions yet</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Date</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Name</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Email</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Phone</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Message</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {contacts.map((contact) => (
                  <tr key={contact.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {new Date(contact.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center">
                        <User className="w-4 h-4 mr-2 text-gray-400" />
                        <span className="font-medium text-gray-800">{contact.name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center text-sm text-gray-600">
                        <Mail className="w-4 h-4 mr-2 text-gray-400" />
                        <a href={`mailto:${contact.email}`} className="hover:text-red-600">
                          {contact.email}
                        </a>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center text-sm text-gray-600">
                        <Phone className="w-4 h-4 mr-2 text-gray-400" />
                        <a href={`tel:${contact.phone}`} className="hover:text-red-600">
                          {contact.phone}
                        </a>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600 max-w-md">
                      <div className="line-clamp-2">{contact.message}</div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminContacts;
