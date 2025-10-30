import { useState, useEffect } from 'react';
import { useAdminAuth } from '@/context/AdminAuthContext';
import axios from 'axios';
import { Plus, Edit, Trash2, Save, X, Eye, EyeOff } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminBanners = () => {
  const { token } = useAdminAuth();
  const [banners, setBanners] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingBanner, setEditingBanner] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [formData, setFormData] = useState({
    image: '',
    title: '',
    description: '',
    button_text: '',
    button_link: '',
    order: 0,
    active: true
  });

  useEffect(() => {
    fetchBanners();
  }, []);

  const fetchBanners = async () => {
    try {
      const response = await axios.get(`${API}/admin/banners`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setBanners(response.data);
    } catch (error) {
      console.error('Error fetching banners:', error);
    }
    setLoading(false);
  };

  const handleAdd = () => {
    setEditingBanner(null);
    setSelectedFile(null);
    setPreviewUrl('');
    setFormData({
      image: '',
      title: '',
      description: '',
      button_text: '',
      button_link: '',
      order: banners.length,
      active: true
    });
    setShowModal(true);
  };

  const handleEdit = (banner) => {
    setEditingBanner(banner);
    setSelectedFile(null);
    // Handle different URL formats
    let imageUrl;
    if (banner.image.startsWith('http')) {
      imageUrl = banner.image;
    } else if (banner.image.startsWith('/api/')) {
      imageUrl = `${BACKEND_URL}${banner.image}`;
    } else if (banner.image.startsWith('/uploads/')) {
      imageUrl = `${BACKEND_URL}/api${banner.image}`;
    } else {
      imageUrl = `${BACKEND_URL}${banner.image}`;
    }
    setPreviewUrl(imageUrl);
    setFormData(banner);
    setShowModal(true);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      // Create preview URL
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUploadImage = async () => {
    if (!selectedFile) return null;
    
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      
      const response = await axios.post(`${API}/admin/banners/upload`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      
      return response.data.url;
    } catch (error) {
      console.error('Error uploading image:', error);
      throw error;
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this banner?')) return;
    
    try {
      await axios.delete(`${API}/admin/banners/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchBanners();
    } catch (error) {
      console.error('Error deleting banner:', error);
      alert('Failed to delete banner');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      let imageUrl = formData.image;
      
      // Upload new image if selected
      if (selectedFile) {
        imageUrl = await handleUploadImage();
        if (!imageUrl) {
          alert('Failed to upload image');
          return;
        }
      }
      
      // Ensure we have an image URL
      if (!imageUrl) {
        alert('Please select an image');
        return;
      }
      
      const submissionData = {
        ...formData,
        image: imageUrl
      };
      
      if (editingBanner) {
        await axios.put(`${API}/admin/banners/${editingBanner.id}`, submissionData, {
          headers: { Authorization: `Bearer ${token}` }
        });
      } else {
        await axios.post(`${API}/admin/banners`, submissionData, {
          headers: { Authorization: `Bearer ${token}` }
        });
      }
      setShowModal(false);
      fetchBanners();
    } catch (error) {
      console.error('Error saving banner:', error);
      alert('Failed to save banner');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Banner Management</h1>
        <button
          onClick={handleAdd}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Add Banner</span>
        </button>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {banners.map((banner) => {
          // Handle different URL formats
          let imageUrl;
          if (banner.image.startsWith('http')) {
            imageUrl = banner.image;
          } else if (banner.image.startsWith('/api/')) {
            imageUrl = `${BACKEND_URL}${banner.image}`;
          } else if (banner.image.startsWith('/uploads/')) {
            imageUrl = `${BACKEND_URL}/api${banner.image}`;
          } else {
            imageUrl = `${BACKEND_URL}${banner.image}`;
          }
          
          return (
          <div key={banner.id} className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-6">
              {/* Banner Image */}
              <div className="relative">
                <img 
                  src={imageUrl}
                  alt={banner.title} 
                  className="w-full h-48 object-cover rounded-lg"
                />
                {!banner.active && (
                  <div className="absolute top-2 right-2 bg-red-600 text-white px-2 py-1 rounded text-xs">
                    Inactive
                  </div>
                )}
              </div>

              {/* Banner Details */}
              <div className="md:col-span-2">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-bold mb-2">{banner.title}</h3>
                    <p className="text-gray-600 mb-4">{banner.description}</p>
                    <div className="flex items-center space-x-4 text-sm">
                      <span className="bg-gray-100 px-3 py-1 rounded">
                        Button: {banner.button_text}
                      </span>
                      <span className="text-gray-500">
                        Link: {banner.button_link}
                      </span>
                      <span className="text-gray-500">
                        Order: {banner.order}
                      </span>
                    </div>
                  </div>
                  
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleEdit(banner)}
                      className="p-2 text-blue-600 hover:bg-blue-50 rounded"
                      title="Edit"
                    >
                      <Edit className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(banner.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded"
                      title="Delete"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          );
        })}

        {banners.length === 0 && (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <p className="text-gray-500">No banners yet. Add your first banner!</p>
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold">{editingBanner ? 'Edit' : 'Add'} Banner</h2>
                <button onClick={() => setShowModal(false)}>
                  <X className="w-6 h-6" />
                </button>
              </div>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold mb-1">Banner Image *</label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="w-full px-3 py-2 border rounded-lg"
                    required={!editingBanner}
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Upload an image (JPG, PNG, GIF, or WebP)
                  </p>
                  {previewUrl && (
                    <div className="mt-3">
                      <img 
                        src={previewUrl} 
                        alt="Preview" 
                        className="w-full h-48 object-cover rounded-lg border"
                      />
                    </div>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-1">Title *</label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg"
                    placeholder="Welcome to Our Restaurant"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-1">Description *</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg"
                    rows="3"
                    placeholder="Experience authentic Indian cuisine..."
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold mb-1">Button Text *</label>
                    <input
                      type="text"
                      value={formData.button_text}
                      onChange={(e) => setFormData({...formData, button_text: e.target.value})}
                      className="w-full px-3 py-2 border rounded-lg"
                      placeholder="Reserve Table"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold mb-1">Button Link *</label>
                    <input
                      type="text"
                      value={formData.button_link}
                      onChange={(e) => setFormData({...formData, button_link: e.target.value})}
                      className="w-full px-3 py-2 border rounded-lg"
                      placeholder="/reservation"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold mb-1">Order</label>
                    <input
                      type="number"
                      value={formData.order}
                      onChange={(e) => setFormData({...formData, order: parseInt(e.target.value)})}
                      className="w-full px-3 py-2 border rounded-lg"
                      min="0"
                    />
                    <p className="text-xs text-gray-500 mt-1">Lower numbers appear first</p>
                  </div>

                  <div className="flex items-center pt-6">
                    <input
                      type="checkbox"
                      checked={formData.active}
                      onChange={(e) => setFormData({...formData, active: e.target.checked})}
                      className="w-4 h-4 text-red-600"
                    />
                    <label className="ml-2 text-sm font-semibold">Active (Show on homepage)</label>
                  </div>
                </div>

                <div className="flex justify-end space-x-3 pt-4 border-t">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="px-4 py-2 border rounded-lg hover:bg-gray-50"
                    disabled={uploading}
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={uploading}
                  >
                    <Save className="w-5 h-5" />
                    <span>{uploading ? 'Uploading...' : 'Save Banner'}</span>
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminBanners;
