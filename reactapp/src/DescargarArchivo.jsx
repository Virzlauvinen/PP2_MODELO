import React from 'react';
import axios from 'axios';

const FileDownloadComponent = ({ fileName }) => {
  const handleFileDownload = async () => {
    try {
      const respuesta = await axios.get(`http://localhost:5000/download/${fileName}`, {
        responseType: 'blob',
      })

      const urlArchivo = window.URL.createObjectURL(new Blob([respuesta.data]));
      const link = document.createElement('a');
      link.href = urlArchivo;
      link.setAttribute('download', fileName);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      console.log()
    } catch (error) {
      console.error('Error al descargar el archivo:', error);
    }
  };

  return (
    <div>
      <h2>Descargar archivo</h2>
      <button onClick={handleFileDownload}>Descargar</button>
    </div>
  );
};

export default FileDownloadComponent;
