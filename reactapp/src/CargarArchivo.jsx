import React, { useState } from 'react';
import axios from 'axios';

const FileUploadComponent = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Limpiar el archivo seleccionado después de subirlo
      setSelectedFile(null);
    } catch (error) {
      console.error('Error al cargar el archivo:', error);
    }
  };

  return (
    <div>
      <h2>Cargar archivo</h2>
      <input type="file" onChange={handleFileChange} />
      <button className="btn btn-lg" onClick={handleFileUpload} disabled={!selectedFile}>
        Cargar
      </button>
    </div>
  );
};

export default FileUploadComponent;
