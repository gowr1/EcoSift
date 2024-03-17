import { Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage'
import VideoUpload from './components/VideoUpload';
import Layout from './components/Layout';

function App() {

  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="video-upload" element={<VideoUpload />} />
      </Route>
    </Routes>
  )
}

export default App
