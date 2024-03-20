import React from 'react';

const Navbar = () => {
  return (
    <nav className="bg-gray-100 p-2 flex justify-between items-center">
      <div className="flex items-center">
        <img src="/path/to/your/logo.png" alt="Logo" className="h-8 mr-2" />
        <span className="text-green-600 text-lg font-bold">Your Logo</span>
      </div>
      <div className="flex items-center space-x-4">
        <a href="#about" className="text-green-600 hover:text-white hover:bg-green-800 px-4 py-2 rounded-lg">About Us</a>
        <a href="#yolo" className="text-green-600 hover:text-white hover:bg-green-800 px-4 py-2 rounded-lg">YOLO Model</a>
        <a href="#test-run" className="text-green-600 hover:text-white hover:bg-green-800 px-4 py-2 rounded-lg">Test Run</a>
        <a href="#control-panel" className="text-green-600 hover:text-white hover:bg-green-800 px-4 py-2 rounded-lg">Control Panel</a>
      </div>
    </nav>
  );
};

export default Navbar;
