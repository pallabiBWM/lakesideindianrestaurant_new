const About = () => {
  return (
    <div className="bg-white">
      {/* Banner */}
      <section
        className="relative h-96 bg-cover bg-center"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1712488067128-080974f6ab73)'
        }}
        data-testid="about-banner"
      >
        <div className="absolute inset-0 bg-black bg-opacity-60"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white" data-testid="about-title">About <span className="text-red-600">Us</span></h1>
        </div>
      </section>

      {/* Our Story */}
      <section className="py-16 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold mb-6">Our <span className="text-red-600">Story</span></h2>
              <p className="text-gray-700 mb-4">
                Lakeside Indian Restaurant was founded in 2009 with a vision to bring authentic Indian flavors to our beautiful lakeside community. What started as a small family-owned establishment has grown into a beloved dining destination, known for its warm hospitality and exceptional cuisine.
              </p>
              <p className="text-gray-700 mb-4">
                Our recipes are passed down through generations, each dish crafted with love and traditional cooking methods. We take pride in using only the finest ingredients and authentic spices imported directly from India.
              </p>
              <p className="text-gray-700">
                The stunning lakeside location provides the perfect backdrop for memorable dining experiences, whether you're celebrating a special occasion or simply enjoying a meal with loved ones.
              </p>
            </div>
            <div>
              <img
                src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4"
                alt="Restaurant interior"
                className="rounded-lg shadow-xl w-full h-96 object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Philosophy */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="container mx-auto max-w-6xl">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div className="order-2 md:order-1">
              <img
                src="https://images.unsplash.com/photo-1585937421612-70a008356fbe"
                alt="Indian cuisine"
                className="rounded-lg shadow-xl w-full h-96 object-cover"
              />
            </div>
            <div className="order-1 md:order-2">
              <h2 className="text-4xl font-bold mb-6">Our <span className="text-red-600">Philosophy</span></h2>
              <p className="text-gray-700 mb-4">
                At Lakeside, we believe that great food brings people together. Our philosophy is simple: use the finest ingredients, honor traditional recipes, and serve every dish with genuine warmth and care.
              </p>
              <p className="text-gray-700 mb-4">
                We are committed to providing an authentic Indian dining experience that respects the rich culinary heritage of India while embracing contemporary presentation and service standards.
              </p>
              <p className="text-gray-700">
                Every member of our team is dedicated to making your visit memorable, from our skilled chefs in the kitchen to our attentive service staff.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;
