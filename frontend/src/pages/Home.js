import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ChevronLeft, ChevronRight, Star } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Carousel images
const carouselImages = [
  'https://images.unsplash.com/photo-1712488067128-080974f6ab73',
  'https://images.unsplash.com/photo-1712488070215-d22e012314ae',
  'https://images.pexels.com/photos/9316209/pexels-photo-9316209.jpeg',
  'https://images.pexels.com/photos/9316937/pexels-photo-9316937.jpeg'
];

const Home = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [banners, setBanners] = useState([]);
  const [featuredItems, setFeaturedItems] = useState([]);
  const [testimonials, setTestimonials] = useState([]);
  const [galleryImages, setGalleryImages] = useState([]);
  const [statistics, setStatistics] = useState({});
  const [currentTestimonial, setCurrentTestimonial] = useState(0);

  useEffect(() => {
    fetchFeaturedItems();
    fetchTestimonials();
    fetchGalleryImages();
    fetchStatistics();
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % carouselImages.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 6000);
    return () => clearInterval(timer);
  }, [testimonials.length]);

  const fetchFeaturedItems = async () => {
    try {
      const response = await axios.get(`${API}/menu?featured=true`);
      setFeaturedItems(response.data.slice(0, 6));
    } catch (error) {
      console.error('Error fetching featured items:', error);
    }
  };

  const fetchTestimonials = async () => {
    try {
      const response = await axios.get(`${API}/testimonials`);
      setTestimonials(response.data);
    } catch (error) {
      console.error('Error fetching testimonials:', error);
    }
  };

  const fetchGalleryImages = async () => {
    try {
      const response = await axios.get(`${API}/gallery`);
      setGalleryImages(response.data.slice(0, 6));
    } catch (error) {
      console.error('Error fetching gallery images:', error);
    }
  };

  const fetchStatistics = async () => {
    try {
      const response = await axios.get(`${API}/statistics`);
      setStatistics(response.data);
    } catch (error) {
      console.error('Error fetching statistics:', error);
    }
  };

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % carouselImages.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + carouselImages.length) % carouselImages.length);
  };

  return (
    <div className="bg-white">
      {/* Carousel Banner Section */}
      <section className="relative h-[600px] overflow-hidden" data-testid="hero-carousel">
        {carouselImages.map((img, index) => (
          <div
            key={index}
            className={`absolute inset-0 transition-opacity duration-1000 ${
              index === currentSlide ? 'opacity-100' : 'opacity-0'
            }`}
          >
            <img src={img} alt={`Slide ${index + 1}`} className="w-full h-full object-cover" />
            <div className="absolute inset-0 bg-black bg-opacity-50"></div>
          </div>
        ))}

        <div className="absolute inset-0 flex items-center justify-center text-center z-10">
          <div className="text-white px-4">
            <h1 className="text-5xl md:text-7xl font-bold mb-4" data-testid="hero-title">
              <span className="text-red-600">Lakeside</span> Indian Restaurant
            </h1>
            <p className="text-xl md:text-2xl mb-8">Authentic Indian Cuisine by the Lakeside</p>
            <Link
              to="/reservation"
              className="bg-red-600 hover:bg-red-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-colors inline-block"
              data-testid="reserve-table-button"
            >
              Reserve Table
            </Link>
          </div>
        </div>

        <button
          onClick={prevSlide}
          className="absolute left-4 top-1/2 -translate-y-1/2 bg-black bg-opacity-50 hover:bg-opacity-75 text-white p-2 rounded-full z-10 transition-colors"
          data-testid="carousel-prev"
        >
          <ChevronLeft className="w-8 h-8" />
        </button>
        <button
          onClick={nextSlide}
          className="absolute right-4 top-1/2 -translate-y-1/2 bg-black bg-opacity-50 hover:bg-opacity-75 text-white p-2 rounded-full z-10 transition-colors"
          data-testid="carousel-next"
        >
          <ChevronRight className="w-8 h-8" />
        </button>
      </section>

      {/* About Us Preview Section */}
      <section className="py-16 px-4" data-testid="about-preview">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold mb-6">Welcome to <span className="text-red-600">Lakeside</span></h2>
              <p className="text-gray-700 text-lg mb-6">
                Experience the rich flavors of authentic Indian cuisine in a stunning lakeside setting. Our restaurant combines traditional recipes passed down through generations with modern culinary techniques to create an unforgettable dining experience. Each dish is prepared with fresh ingredients and aromatic spices that transport you to the heart of India.
              </p>
              <Link
                to="/about"
                className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors inline-block"
                data-testid="read-more-about"
              >
                Read More
              </Link>
            </div>
            <div>
              <img 
                src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4" 
                alt="Restaurant Interior" 
                className="rounded-lg shadow-xl w-full h-96 object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="bg-black text-white py-16 px-4" data-testid="statistics-section">
        <div className="container mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <StatCard number={statistics.happy_customers || 0} label="Happy Customers" />
            <StatCard number={statistics.dishes_served || 0} label="Dishes Served" />
            <StatCard number={statistics.years_experience || 0} label="Years of Experience" />
            <StatCard number={statistics.team_members || 0} label="Team Members" />
          </div>
        </div>
      </section>

      {/* Mini Menu Section */}
      <section className="py-16 px-4 bg-gray-50" data-testid="featured-menu">
        <div className="container mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">Featured <span className="text-red-600">Dishes</span></h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredItems.map((item) => (
              <div key={item.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow p-6" data-testid={`featured-dish-${item.id}`}>
                <div className="mb-2">
                  <span className="text-xs font-semibold text-red-600 bg-red-50 px-2 py-1 rounded">
                    {item.category}
                  </span>
                </div>
                <h3 className="text-xl font-bold mb-2">{item.name}</h3>
                <p className="text-gray-600 mb-4 text-sm">{item.description}</p>
                <p className="text-2xl font-bold text-red-600">${item.price.toFixed(2)}</p>
              </div>
            ))}
          </div>
          <div className="text-center mt-12 flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/menu/dine-in"
              className="bg-red-600 hover:bg-red-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors inline-block"
              data-testid="view-dinein-menu"
            >
              View Dine-in Menu
            </Link>
            <Link
              to="/menu/takeaway"
              className="bg-black hover:bg-gray-900 text-white px-8 py-3 rounded-lg font-semibold transition-colors inline-block"
              data-testid="view-takeaway-menu"
            >
              View Takeaway Menu
            </Link>
          </div>
        </div>
      </section>

      {/* Gallery Preview Section */}
      <section className="py-16 px-4" data-testid="gallery-preview">
        <div className="container mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">Our <span className="text-red-600">Gallery</span></h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {galleryImages.map((img) => (
              <div key={img.id} className="relative h-64 overflow-hidden rounded-lg hover:scale-105 transition-transform" data-testid={`gallery-preview-${img.id}`}>
                <img src={img.url} alt={img.title} className="w-full h-full object-cover" />
              </div>
            ))}
          </div>
          <div className="text-center mt-12">
            <Link
              to="/gallery"
              className="bg-red-600 hover:bg-red-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors inline-block"
              data-testid="view-gallery"
            >
              View Gallery
            </Link>
          </div>
        </div>
      </section>

      {/* Contact & Reservation Section */}
      <section className="py-16 px-4 bg-gray-50" data-testid="contact-reservation-section">
        <div className="container mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">Get In <span className="text-red-600">Touch</span></h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <Link
              to="/contact"
              className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition-shadow text-center group"
              data-testid="contact-us-link"
            >
              <h3 className="text-2xl font-bold mb-4 group-hover:text-red-600 transition-colors">Contact Us</h3>
              <p className="text-gray-600 mb-6">Have questions or feedback? We'd love to hear from you!</p>
              <span className="text-red-600 font-semibold">Send Message →</span>
            </Link>
            <Link
              to="/reservation"
              className="bg-black text-white p-8 rounded-lg shadow-lg hover:shadow-xl transition-shadow text-center group"
              data-testid="make-reservation-link"
            >
              <h3 className="text-2xl font-bold mb-4 group-hover:text-red-600 transition-colors">Reserve a Table</h3>
              <p className="text-gray-300 mb-6">Book your table now and enjoy an unforgettable dining experience!</p>
              <span className="text-red-600 font-semibold">Book Now →</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Testimonials Slider */}
      {testimonials.length > 0 && (
        <section className="py-16 px-4 bg-black text-white" data-testid="testimonials-section">
          <div className="container mx-auto max-w-4xl">
            <h2 className="text-4xl font-bold text-center mb-12">What Our <span className="text-red-600">Customers</span> Say</h2>
            <div className="relative">
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  {[...Array(testimonials[currentTestimonial]?.rating || 5)].map((_, i) => (
                    <Star key={i} className="w-6 h-6 fill-red-600 text-red-600" />
                  ))}
                </div>
                <p className="text-xl mb-6 italic">"{testimonials[currentTestimonial]?.comment}"</p>
                <p className="font-bold text-red-600">{testimonials[currentTestimonial]?.name}</p>
              </div>
              <div className="flex justify-center mt-8 space-x-2">
                {testimonials.map((_, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentTestimonial(index)}
                    className={`w-3 h-3 rounded-full transition-colors ${
                      index === currentTestimonial ? 'bg-red-600' : 'bg-gray-600'
                    }`}
                    data-testid={`testimonial-dot-${index}`}
                  />
                ))}
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

const StatCard = ({ number, label }) => (
  <div className="p-6">
    <div className="text-5xl font-bold text-red-600 mb-2">{number.toLocaleString()}+</div>
    <div className="text-lg">{label}</div>
  </div>
);

export default Home;
