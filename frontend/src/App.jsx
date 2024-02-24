import { Route, Routes } from 'react-router-dom';
import HomePage from '../components/HomePage'
import VideoUpload from '../components/VideoUpload';

function App() {

  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/video-upload" element={<VideoUpload />} />
    </Routes>
  )
}

export default App
