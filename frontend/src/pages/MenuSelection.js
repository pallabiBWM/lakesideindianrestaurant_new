import { Link } from 'react-router-dom';
import { UtensilsCrossed, ShoppingBag } from 'lucide-react';

const MenuSelection = () => {
  return (
    <div className="bg-white min-h-screen">
      {/* Banner */}
      <section
        className="relative h-96 bg-cover bg-center"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1589302168068-964664d93dc0)'
        }}
      >
        <div className="absolute inset-0 bg-black bg-opacity-60"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-4">
              Choose Your <span className="text-red-600">Menu</span>
            </h1>
            <p className="text-xl text-white">Select from our Dine-in or Takeaway options</p>
          </div>
        </div>
      </section>

      {/* Menu Options */}
      <section className="py-16 px-4">
        <div className="container mx-auto max-w-4xl">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Dine-in Menu */}
            <Link
              to="/menu/dine-in"
              className="group bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2"
              data-testid="dinein-menu-card"
            >
              <div className="relative h-64 bg-gradient-to-br from-red-600 to-red-800 flex items-center justify-center">
                <UtensilsCrossed className="w-24 h-24 text-white" />
              </div>
              <div className="p-8">
                <h2 className="text-3xl font-bold text-gray-800 mb-4 group-hover:text-red-600 transition-colors">
                  Dine-in Menu
                </h2>
                <p className="text-gray-600 mb-6">
                  Experience our authentic Indian cuisine in our beautiful restaurant setting. 
                  Enjoy the full dining experience with our complete menu.
                </p>
                <div className="flex items-center text-red-600 font-semibold group-hover:translate-x-2 transition-transform">
                  View Dine-in Menu
                  <span className="ml-2">→</span>
                </div>
              </div>
            </Link>

            {/* Takeaway Menu */}
            <Link
              to="/menu/takeaway"
              className="group bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2"
              data-testid="takeaway-menu-card"
            >
              <div className="relative h-64 bg-gradient-to-br from-black to-gray-800 flex items-center justify-center">
                <ShoppingBag className="w-24 h-24 text-white" />
              </div>
              <div className="p-8">
                <h2 className="text-3xl font-bold text-gray-800 mb-4 group-hover:text-red-600 transition-colors">
                  Takeaway Menu
                </h2>
                <p className="text-gray-600 mb-6">
                  Order your favorite dishes to enjoy at home. All the same great flavors, 
                  packaged perfectly for takeaway.
                </p>
                <div className="flex items-center text-red-600 font-semibold group-hover:translate-x-2 transition-transform">
                  View Takeaway Menu
                  <span className="ml-2">→</span>
                </div>
              </div>
            </Link>
          </div>
        </div>
      </section>

      {/* Additional Info */}
      <section className="py-12 px-4 bg-gray-50">
        <div className="container mx-auto max-w-4xl text-center">
          <h3 className="text-2xl font-bold text-gray-800 mb-4">
            Both Menus Feature Our Complete Range
          </h3>
          <p className="text-gray-600 mb-8">
            Enjoy the same delicious dishes whether dining in or taking away. 
            All items are prepared fresh with authentic spices and ingredients.
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="bg-white p-4 rounded-lg shadow">
              <p className="font-semibold text-red-600">121+</p>
              <p className="text-gray-600">Menu Items</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <p className="font-semibold text-red-600">14</p>
              <p className="text-gray-600">Categories</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <p className="font-semibold text-red-600">Fresh</p>
              <p className="text-gray-600">Ingredients</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow">
              <p className="font-semibold text-red-600">Authentic</p>
              <p className="text-gray-600">Recipes</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default MenuSelection;
