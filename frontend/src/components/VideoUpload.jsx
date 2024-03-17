import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import Updates from './Updates';
import OptionsTable from './OptionsTable';

const url = 'http://127.0.0.1:5000';

const VideoUpload = () => {
  const [videoUrl, setVideoUrl] = useState('');
  const [uploadStatus, setUploadStatus] = useState(null);
  const [isUploaded, setIsUploaded] = useState(false);
  const [clsList, setClsList] = useState([]);
  const [optionsSelected, setOptionsSelected] = useState(false);

  const videoRef = useRef(null);
  const socket = useRef(null);

  useEffect(() => {
    socket.current = io.connect(url);

    socket.current.on('update_frame', (data) => {
      const imageUrl = URL.createObjectURL(new Blob([data.frame], { type: 'image/jpeg' }));
      videoRef.current.src = imageUrl;

      const clsList = JSON.parse(data.cls);
      setClsList(clsList);
    });

    socket.current.on('connect', () => {
      console.log('Connected to server');
    });

    socket.current.on('disconnect', () => {
      console.log('Disconnected from server');
    });

    return () => {
      socket.current.disconnect();
    };
  }, []);

  const handleRequestFrames = () => {
    socket.current.emit('request_frames', 'uploads\\uploaded-video.mp4');
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      const videoObjectUrl = URL.createObjectURL(file);
      setVideoUrl(videoObjectUrl);
    }
  };


  const handleUpload = async () => {
    try {
      const file = await fetch(videoUrl).then((res) => res.blob());
      const formData = new FormData();
      formData.append('file', file, 'uploaded-video.mp4');

      const response = await fetch(url.concat('/upload_video'), {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setUploadStatus('Video uploaded successfully!');
      } else {
        setUploadStatus('Failed to upload video.');
      }
    } catch (error) {
      document.getElementById("upload-video-label").style.display = "none";
      setIsUploaded(true);
      console.error('Error uploading video:', error);
      setUploadStatus('An error occurred during upload.');
    }
  };

  return (
      <div className='flex flex-row justify-between'>
        <div className="w-3/4 m-4 px-4 bg-gray-100 rounded-lg shadow-md h-[40rem]">
          <label id="upload-video-label" className="block text-lg font-semibold mb-2">Upload Video</label>
          <input
            type="file"
            accept="video/*"
            onChange={handleFileChange}
            className="border rounded p-2 w-full"
            hidden={isUploaded}
          />

          {uploadStatus && (
            <div className="mt-4">
              <div className="flex flex-row">
                <p className="text-lg font-semibold mb-2">Uploaded Video:</p>
                <button
                  className='bg-blue-500 text-white mx-4 mb-2 py-1 px-4 rounded hover:bg-blue-600 focus:outline-none focus:shadow-outline-blue active:bg-blue-800'
                  onClick={handleRequestFrames}
                >
                  Request Frames
                </button>
              </div>
              <div className='w-full'>
                <img ref={videoRef} width={1200} height={600} />
              </div>
            </div>
          )}
          {!uploadStatus && (
            <button
              onClick={handleUpload}
              className="mt-4 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none focus:shadow-outline-blue active:bg-blue-800"
            >
              Upload Video
            </button>
          )}
          {uploadStatus && <p className="mt-2">{uploadStatus}</p>}
        </div>
        {optionsSelected ? <Updates clsList={clsList} /> :
                          <OptionsTable setClsList={setClsList} setOptionsSelected={setOptionsSelected} />
        }
      </div>
  );
};

export default VideoUpload;