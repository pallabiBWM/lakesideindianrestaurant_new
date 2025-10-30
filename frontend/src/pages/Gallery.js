import { useState, useEffect } from 'react';
import axios from 'axios';
import { X } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Gallery = () => {
  const [images, setImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGalleryImages();
  }, []);

  const fetchGalleryImages = async () => {
    try {
      const response = await axios.get(`${API}/gallery`);
      setImages(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching gallery images:', error);
      setLoading(false);
    }
  };

  const openLightbox = (image) => {
    setSelectedImage(image);
  };

  const closeLightbox = () => {
    setSelectedImage(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-2xl font-semibold">Loading gallery...</div>
      </div>
    );
  }

  return (
    <div className="bg-white min-h-screen">
      {/* Banner */}
      <section
        className="relative h-96 bg-cover bg-center"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1667388969250-1c7220bf3f37)'
        }}
        data-testid="gallery-banner"
      >
        <div className="absolute inset-0 bg-black bg-opacity-60"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white" data-testid="gallery-title">Our <span className="text-red-600">Gallery</span></h1>
        </div>
      </section>

      {/* Gallery Grid */}
      <section className="py-16 px-4">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {images.map((image) => (
              <div
                key={image.id}
                className="relative h-80 overflow-hidden rounded-lg cursor-pointer group"
                onClick={() => openLightbox(image)}
                data-testid={`gallery-image-${image.id}`}
              >
                <img
                  src={image.url.startsWith('http') ? image.url : `${BACKEND_URL}${image.url}?t=${Date.now()}`}
                  alt={image.title}
                  className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-60 transition-opacity flex items-center justify-center">
                  <div className="text-white text-center opacity-0 group-hover:opacity-100 transition-opacity p-4">
                    <h3 className="text-xl font-bold mb-2">{image.title}</h3>
                    {image.description && <p className="text-sm">{image.description}</p>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Lightbox */}
      {selectedImage && (
        <div
          className="fixed inset-0 bg-black bg-opacity-90 z-50 flex items-center justify-center p-4"
          onClick={closeLightbox}
          data-testid="lightbox-overlay"
        >
          <div className="relative max-w-6xl max-h-full" onClick={(e) => e.stopPropagation()}>
            <button
              onClick={closeLightbox}
              className="absolute -top-12 right-0 text-white hover:text-red-600 transition-colors"
              data-testid="lightbox-close"
            >
              <X className="w-10 h-10" />
            </button>
            <img
              src={selectedImage.url.startsWith('http') ? selectedImage.url : `${BACKEND_URL}${selectedImage.url}`}
              alt={selectedImage.title}
              className="max-w-full max-h-[80vh] object-contain rounded-lg"
              data-testid="lightbox-image"
            />
            <div className="text-white text-center mt-4">
              <h3 className="text-2xl font-bold mb-2">{selectedImage.title}</h3>
              {selectedImage.description && <p>{selectedImage.description}</p>}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Gallery;
